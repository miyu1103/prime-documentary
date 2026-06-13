from __future__ import annotations
import argparse
import json
from pathlib import Path
from .domain import EpisodeState
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
    return parser

def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))

if __name__ == "__main__":
    raise SystemExit(main())
