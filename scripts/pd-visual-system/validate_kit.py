#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None
try:
    import jsonschema
except ImportError:
    jsonschema = None

REQUIRED = [
    'CLAUDE.md','README_START_HERE.md','INSTALL.ps1','.claude/settings.json',
    '.claude/pd-safety-policy.json','.claude/hooks/pd_safety_gate.py',
    'docs/pd-visual-system/MASTER_REFERENCE.md','docs/pd-visual-system/PHASE_STATE.json',
    'docs/pd-visual-system/100_POINT_SCORECARD.md',
    'config/pd-visual-system/component-registry.json','config/pd-visual-system/phase-registry.json',
    'schemas/scene-plan.schema.json','schemas/asset-record.schema.json','schemas/phase-state.schema.json',
]
CORE=['EvidenceReveal','PenaltyVsProperty','CaseJourney','QuoteUnderExamination','VerdictReversal']
PHASES=[f'P{i:02d}' for i in range(13)]
SOURCE_TYPES={'verified_evidence','documentary_source_media','licensed_broll','illustrative_animation','three_d_reconstruction','ai_generated_broll','ai_reenactment'}


def fm(path: Path) -> dict:
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'): raise ValueError('missing YAML frontmatter')
    raw=text.split('---',2)[1]
    return (yaml.safe_load(raw) or {}) if yaml else {'raw':raw}


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',type=Path,default=Path('.')); args=ap.parse_args()
    root=args.project_root.resolve(); errors=[]; warnings=[]
    def err(x): errors.append(x)

    for rel in REQUIRED:
        if not (root/rel).exists(): err(f'missing required file: {rel}')

    json_paths=list(root.glob('schemas/*.json'))+list(root.glob('config/pd-visual-system/*.json'))+[
        root/'.claude/settings.json',root/'.claude/pd-safety-policy.json',root/'docs/pd-visual-system/PHASE_STATE.json']
    parsed={}
    for path in json_paths:
        if not path.exists(): continue
        try: parsed[path]=json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc: err(f'invalid JSON {path.relative_to(root)}: {exc}')

    settings=parsed.get(root/'.claude/settings.json',{})
    perms=settings.get('permissions',{})
    if perms.get('defaultMode')!='default': err('permissions.defaultMode must be default')
    if perms.get('disableBypassPermissionsMode')!='disable': err('bypassPermissions must be disabled')
    if not settings.get('hooks',{}).get('PreToolUse'): err('PreToolUse hook missing')

    reg=parsed.get(root/'config/pd-visual-system/component-registry.json',{})
    core=[x.get('name') for x in reg.get('core_components',[])]
    if core!=CORE: err(f'core component registry mismatch: {core}')
    if reg.get('rules',{}).get('initial_implementation_count')!=5: err('initial component count must be 5')
    canonical=set(core)|{x.get('name') for x in reg.get('expansion_components',[])}|{x.get('name') for x in reg.get('primitives',[])}
    for alias,target in reg.get('aliases',{}).items():
        if target.get('canonical') not in canonical: err(f'alias {alias} points to undefined {target.get("canonical")}')
        if alias==target.get('canonical'): err(f'alias loops to itself: {alias}')

    phase_reg=parsed.get(root/'config/pd-visual-system/phase-registry.json',{})
    ids=[x.get('id') for x in phase_reg.get('phases',[])]
    if ids!=PHASES: err(f'phase order mismatch: {ids}')
    if len({x.get('slug') for x in phase_reg.get('phases',[])})!=13: err('phase slugs must be unique')
    transition=phase_reg.get('transition_policy',{})
    if transition.get('automatic_phase_advance') is not False or transition.get('human_approval_required_to_advance') is not True:
        err('phase transition policy must prohibit auto advance')

    state=parsed.get(root/'docs/pd-visual-system/PHASE_STATE.json',{})
    schema_path=root/'schemas/phase-state.schema.json'
    if jsonschema and state and schema_path.exists():
        try: jsonschema.Draft202012Validator(json.loads(schema_path.read_text(encoding='utf-8'))).validate(state)
        except Exception as exc: err(f'PHASE_STATE schema failure: {exc}')
    elif not jsonschema: warnings.append('jsonschema not installed; instance validation skipped')

    for name in ['scene-plan.schema.json','asset-record.schema.json']:
        schema=parsed.get(root/'schemas'/name,{})
        values=set(schema.get('properties',{}).get('source_type',{}).get('enum',[]))
        if values!=SOURCE_TYPES: err(f'{name} source_type mismatch: {values}')

    # All examples must validate, and risky defaults must remain pending/unknown.
    if jsonschema:
        for example in (root/'templates/pd-visual-system').glob('*.example.json'):
            data=json.loads(example.read_text(encoding='utf-8'))
            schema_name=example.name.replace('.example.json','.schema.json')
            schema=root/'schemas'/schema_name
            if not schema.exists(): err(f'no schema for {example.name}'); continue
            try: jsonschema.Draft202012Validator(json.loads(schema.read_text(encoding='utf-8'))).validate(data)
            except Exception as exc: err(f'example validation failed {example.name}: {exc}')
    gen=root/'templates/pd-visual-system/generation-request.example.json'
    if gen.exists():
        g=json.loads(gen.read_text(encoding='utf-8'))
        if g.get('license_decision')!='review_required' or g.get('review_status')!='pending' or g.get('human_review_required') is not True:
            err('generation example has unsafe defaults')

    skills=sorted((root/'.claude/skills').glob('*/SKILL.md')); phase_skills=[]
    for path in skills:
        try: meta=fm(path)
        except Exception as exc: err(f'{path.relative_to(root)}: {exc}'); continue
        if yaml:
            if not meta.get('description'): err(f'{path.relative_to(root)} missing description')
            if path.parent.name.startswith('pd-phase-') and path.parent.name!='pd-phase-advance':
                phase_skills.append(path)
                if meta.get('disable-model-invocation') is not True: err(f'{path.relative_to(root)} must be manual only')
    if len(phase_skills)!=13: err(f'expected 13 phase skills, found {len(phase_skills)}')

    # Markdown and master integrity.
    md_files=list(root.rglob('*.md'))
    for path in md_files:
        text=path.read_text(encoding='utf-8')
        if sum(1 for line in text.splitlines() if line.startswith('```'))%2: err(f'unbalanced fences: {path.relative_to(root)}')
    master=root/'docs/pd-visual-system/MASTER_REFERENCE.md'
    if master.exists():
        text=master.read_text(encoding='utf-8')
        if len(text.splitlines())<5000: err('master reference unexpectedly small')
        forbidden=['最重要8部品','コア8部品のうち3部品','"license_decision": "approved"']
        for phrase in forbidden:
            if phrase in text: err(f'master contains legacy conflict: {phrase}')
        for name in CORE:
            if name not in text: err(f'master missing core component: {name}')

    installer=(root/'INSTALL.ps1').read_text(encoding='utf-8') if (root/'INSTALL.ps1').exists() else ''
    if 'param(' not in installer or '[string]$ProjectRoot' not in installer: err('installer ProjectRoot parameter missing')
    if '$TargetRepo' in installer: err('installer contains obsolete TargetRepo parameter')
    if 'Get-ChildItem -File -Recurse' not in installer: err('installer must merge at file granularity')

    # Python scripts compile syntactically.
    import py_compile
    for path in [root/'.claude/hooks/pd_safety_gate.py',root/'scripts/pd-visual-system/phase_gate.py',root/'scripts/pd-visual-system/validate_examples.py']:
        try: py_compile.compile(str(path),doraise=True)
        except Exception as exc: err(f'python compile failed {path.relative_to(root)}: {exc}')

    print(f'Validated root: {root}')
    for w in warnings: print(f'WARNING: {w}')
    if errors:
        for e in errors: print(f'ERROR: {e}')
        return 1
    print(f'OK: {len(json_paths)} JSON targets, {len(skills)} skills, {len(md_files)} markdown files, master={len(master.read_text(encoding="utf-8").splitlines())} lines')
    return 0


if __name__=='__main__': raise SystemExit(main())
