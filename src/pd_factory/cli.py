from __future__ import annotations
import argparse
import json
from pathlib import Path
from .domain import EpisodeState
from .episode_repo import EpisodeRepo
from .pipeline import STAGES, run_pipeline
from .state_machine import EpisodeStateMachine
from .schema_validation import validate_json

def cmd_transitions(args: argparse.Namespace) -> int:
    state = EpisodeState(args.state)
    print(json.dumps([x.value for x in EpisodeStateMachine.allowed_targets(state)], indent=2))
    return 0

def cmd_validate(args: argparse.Namespace) -> int:
    validate_json(Path(args.instance), Path(args.schema))
    print("valid")
    return 0

def cmd_run(args: argparse.Namespace) -> int:
    repo = EpisodeRepo(Path(args.episode_dir))
    result = run_pipeline(repo, from_stage=args.from_stage, force=args.force)
    print(f"episode: {result.episode_id}")
    print(f"final_state: {result.final_state}")
    for r in result.results:
        suffix = f" {r.checksum[:19]}" if r.checksum else ""
        print(f"  {r.action:8} {r.name:14} {r.revision}{suffix}")
    print(f"produced: {len(result.by_action('produced'))}  skipped: {len(result.by_action('skipped'))}")
    return 0

def cmd_status(args: argparse.Namespace) -> int:
    repo = EpisodeRepo(Path(args.episode_dir))
    manifest = repo.read_manifest()
    active = manifest["active_revisions"]
    print(f"episode: {manifest['episode_id']}")
    print(f"state: {manifest['state']}")
    print(f"actual_cost: {manifest['costs']['actual']['amount']} {manifest['costs']['actual']['currency']}")
    print("stages:")
    print(f"  {'topic':14} {active.get('topic', '-')}")
    for spec in STAGES:
        print(f"  {spec.name:14} {active.get(spec.name, '-')}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pd-blueprint")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("transitions")
    p.add_argument("state", choices=[x.value for x in EpisodeState])
    p.set_defaults(func=cmd_transitions)
    p = sub.add_parser("validate")
    p.add_argument("instance")
    p.add_argument("schema")
    p.set_defaults(func=cmd_validate)
    p = sub.add_parser("run", help="run the vertical-slice pipeline on an episode dir")
    p.add_argument("episode_dir")
    p.add_argument("--from", dest="from_stage", default=None,
                   choices=[s.name for s in STAGES], help="rerun from this stage onward")
    p.add_argument("--force", action="store_true", help="regenerate every stage")
    p.set_defaults(func=cmd_run)
    p = sub.add_parser("status", help="show episode state and active revisions")
    p.add_argument("episode_dir")
    p.set_defaults(func=cmd_status)
    return parser

def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))

if __name__ == "__main__":
    raise SystemExit(main())
