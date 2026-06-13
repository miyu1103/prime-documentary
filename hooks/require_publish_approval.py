#!/usr/bin/env python3
"""Guard example for publish commands. Blocks public/schedule intents without approval evidence."""
from __future__ import annotations
import json, sys

def main()->int:
 raw=sys.stdin.read()
 try: data=json.loads(raw) if raw.strip() else {}
 except Exception: data={"raw":raw}
 text=json.dumps(data,ensure_ascii=False).lower()
 publish_intent=any(x in text for x in ['privacy_status":"public','schedule_publish','public_publish'])
 approval=('approval_status":"valid' in text or 'publish_approved' in text)
 if publish_intent and not approval:
  print(json.dumps({'decision':'block','reason':'Public publish requires exact-revision valid approval.'}))
  return 2
 return 0
if __name__=='__main__': raise SystemExit(main())
