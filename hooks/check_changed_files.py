#!/usr/bin/env python3
"""Post-edit guard: detect likely secrets and validate JSON changed files when paths are supplied."""
from __future__ import annotations
import json, pathlib, re, sys
PATTERNS=[
 re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}"),
 re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
def main(argv:list[str])->int:
 bad=[]
 for arg in argv[1:]:
  p=pathlib.Path(arg)
  if not p.is_file(): continue
  try: text=p.read_text(encoding='utf-8')
  except Exception: continue
  for pat in PATTERNS:
   if pat.search(text): bad.append(f'{p}: possible secret')
  if p.suffix.lower()=='.json':
   try: json.loads(text)
   except Exception as e: bad.append(f'{p}: invalid JSON: {e}')
 if bad:
  print('\n'.join(bad)); return 2
 return 0
if __name__=='__main__': raise SystemExit(main(sys.argv))
