# scripts/_attic — moved out of the way on 2026-08-23, not deleted

If you arrived here because a document or a code comment told you to run something and the file
was not in `scripts/`, it is in this directory. Nothing was thrown away.

## What is here

217 scripts that, on 2026-08-23, were called from nowhere: no other script, document, config,
scheduled task or external tool named them. Almost all are one-off builders written for a single
episode and already run (`build_<slug>_thumbnails_v001.py`, `gen_narration_<slug>.py`,
`upload_schedule_<slug>_v001.py`). `root/` holds ten `run_*.sh` launchers that were sitting at the
repository root.

`scripts/` went from 1,046 files to 832, which is the point: a session could not tell what was
live from what was finished.

## How the list was built, and what it deliberately excluded

The candidate list came from searching for each filename across the repository. **That method has
a blind spot and it was measured before anything moved**: Python imports without an extension, so
`import sdxl_quality_profiles` was invisible to a search for `sdxl_quality_profiles.py`. Six
scripts were found that way and kept in `scripts/`:
`gen_narration_terry.py`, `sdxl_quality_profiles.py`, `upload_private_kelo_v001.py`,
`upload_short07_youtube_public.py`, `assemble_gideon.py`, `upload_madoff.py`.

Also excluded: anything a running process or a `PD-*` scheduled task named, and anything touched
in the previous 21 days.

## Verified afterwards, by a different method than the one that built the list

12,096 text files were re-read — every extension, including the `.bat`, `.cmd`, `.txt`, `.ts`,
`.tsx` and `.toml` the first pass skipped, plus `runs/`, `episodes/` and `remotion/` — and every
moved name was searched for both with and without its extension. 105 references survive:

| kind | count | does it break? |
|---|---|---|
| prose and records (`.md`, `.json`, `.txt`) | 65 | no — a record of what was run |
| output targets (`> out_x.log`, `LOG=…`) | 23 | no — recreated on the next run |
| comments and docstrings ("modeled on …") | 17 | no |
| **imports of a moved module** | **0** | — |
| **executions of a moved script** | **0** | — |
| scheduled tasks and `C:\temp\studio_auto` | **0** | — |

All 775 remaining `scripts/*.py` compile except `gen_short25_images.py`, which has been
syntactically broken in git since commit `46e3c19d` and is unrelated to this move.

## Getting one back

```bash
git mv scripts/_attic/<name> scripts/<name>
```

Or put everything back at once — the move record is exact and the reverse was tested by
round-tripping a file before it was relied on:

```bash
py -3.11 scripts/tidy_repo_root.py --undo-from runs/_attic/UNDO_tidy_20260823.json
```

## Before adding to this directory

Do not move a script here because it *looks* finished. Run
`py -3.11 scripts/tidy_repo_root.py` (dry run) and read what it would take, then check the
import blind spot above by hand. A script that is imported by module name looks unused to every
filename search.
