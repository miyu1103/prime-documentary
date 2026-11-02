#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

PHASES = [f'P{i:02d}' for i in range(13)]
STATUSES = {'not_started', 'in_progress', 'blocked', 'candidate_complete'}


def state_path(root: Path) -> Path:
    return root / 'docs' / 'pd-visual-system' / 'PHASE_STATE.json'


def load_state(root: Path) -> dict:
    path = state_path(root)
    if not path.exists():
        raise SystemExit(f'Phase state not found: {path}')
    state = json.loads(path.read_text(encoding='utf-8'))
    if state.get('current_phase') not in PHASES or state.get('phase_status') not in STATUSES:
        raise SystemExit('PHASE_STATE contains an invalid phase or status.')
    return state


def save_state(root: Path, state: dict) -> None:
    path = state_path(root)
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def append(state: dict, event: str, **fields: object) -> None:
    state.setdefault('history', []).append({'phase': state['current_phase'], 'event': event, 'at': now(), **fields})
    state['last_updated'] = state['history'][-1]['at']


def cmd_assert(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit(f"Phase mismatch: state={state['current_phase']} requested={args.phase}. Do not skip phases.")
    if state['phase_status'] == 'blocked':
        raise SystemExit('Current phase is blocked. Resume it with documented resolution before continuing.')
    print(f"OK: {args.phase} is current; status={state['phase_status']}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit('Cannot start a non-current phase.')
    if state['phase_status'] not in {'not_started', 'in_progress'}:
        raise SystemExit(f"Cannot start from status {state['phase_status']}")
    state['phase_status'] = 'in_progress'
    state['updated_by'] = args.by
    append(state, 'started')
    save_state(args.project_root, state)
    print(f'Started {args.phase}')
    return 0


def cmd_block(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase or state['phase_status'] != 'in_progress':
        raise SystemExit('Only the current in-progress phase can be blocked.')
    state['phase_status'] = 'blocked'
    state.setdefault('blockers', []).append({'phase': args.phase, 'reason': args.reason, 'at': now(), 'resolved': False})
    state['updated_by'] = args.by
    append(state, 'blocked', reason=args.reason)
    save_state(args.project_root, state)
    print(f'Blocked {args.phase}')
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase or state['phase_status'] != 'blocked':
        raise SystemExit('Only the current blocked phase can be resumed.')
    unresolved = [b for b in state.get('blockers', []) if b.get('phase') == args.phase and not b.get('resolved')]
    if not unresolved:
        raise SystemExit('No unresolved blocker record exists.')
    for blocker in unresolved:
        blocker['resolved'] = True; blocker['resolution'] = args.resolution; blocker['resolved_at'] = now()
    state['phase_status'] = 'in_progress'
    state['updated_by'] = args.by
    append(state, 'resumed', resolution=args.resolution)
    save_state(args.project_root, state)
    print(f'Resumed {args.phase}')
    return 0


def cmd_candidate_complete(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit('Cannot complete a non-current phase.')
    if state['phase_status'] != 'in_progress':
        raise SystemExit(f"candidate_complete requires in_progress, not {state['phase_status']}")
    evidence = args.evidence.resolve()
    try:
        evidence.relative_to(args.project_root)
    except ValueError:
        raise SystemExit('Evidence report must be inside the project repository.')
    if not evidence.is_file() or evidence.stat().st_size == 0:
        raise SystemExit(f'Evidence report is missing or empty: {evidence}')
    state['phase_status'] = 'candidate_complete'
    state['updated_by'] = args.by
    append(state, 'candidate_complete', evidence=str(evidence))
    save_state(args.project_root, state)
    print(f'Marked {args.phase} candidate_complete')
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    if not args.human_approved:
        raise SystemExit('Explicit --human-approved is required.')
    state = load_state(args.project_root)
    if state['phase_status'] != 'candidate_complete':
        raise SystemExit('Current phase must be candidate_complete before advancing.')
    current_index = PHASES.index(state['current_phase'])
    if current_index + 1 >= len(PHASES):
        raise SystemExit('Already at final phase.')
    expected = PHASES[current_index + 1]
    if args.to != expected:
        raise SystemExit(f'Next phase must be {expected}; requested {args.to}.')
    previous = state['current_phase']
    append(state, 'completed_and_advanced', next=args.to, approved_by=args.by)
    state['current_phase'] = args.to
    state['phase_status'] = 'not_started'
    state['human_approved_next_phase'] = args.to
    state['updated_by'] = args.by
    save_state(args.project_root, state)
    print(f'Advanced {previous} -> {args.to}')
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument('--project-root', type=Path, default=Path('.'))
    sub = p.add_subparsers(dest='command', required=True)
    q=sub.add_parser('assert'); q.add_argument('--phase',choices=PHASES,required=True); q.set_defaults(func=cmd_assert)
    q=sub.add_parser('start'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_start)
    q=sub.add_parser('block'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--reason',required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_block)
    q=sub.add_parser('resume'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--resolution',required=True); q.add_argument('--by',default='human-via-claude-code'); q.set_defaults(func=cmd_resume)
    q=sub.add_parser('candidate-complete'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--evidence',type=Path,required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_candidate_complete)
    q=sub.add_parser('advance'); q.add_argument('--to',choices=PHASES,required=True); q.add_argument('--human-approved',action='store_true'); q.add_argument('--by',default='human-via-claude-code'); q.set_defaults(func=cmd_advance)
    return p


if __name__ == '__main__':
    args=parser().parse_args(); args.project_root=args.project_root.resolve(); raise SystemExit(args.func(args))
