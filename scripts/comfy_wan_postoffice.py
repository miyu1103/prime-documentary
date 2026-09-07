#!/usr/bin/env python
"""EP56 Post Office Wan i2v entrypoint placeholder.

The EP56 contract requires the real Wan 2.2 A14B driver before --run/--run-all.
This entrypoint fails closed so a deterministic placeholder is never mistaken for
accepted motion.
"""
from __future__ import annotations

import argparse


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--run-all", action="store_true")
    ap.add_argument("--shot")
    args = ap.parse_args()
    if args.build:
        print("EP56 Wan driver is not wired yet; do not run motion generation from this placeholder.")
        return 1
    print("EP56 Wan motion generation is blocked until the real Wan driver is wired.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
