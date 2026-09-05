# Relaunch PD archive-ingest lanes, detached, appending to the ledger logs.
# All lanes resume from the ledgers (see _ledger\CONTRACT.md section 8) — no state is passed in.
#
# Two things this script exists to get right:
#  1. Redirection runs through cmd.exe, NOT PowerShell. PowerShell buffers a native
#     command's stdout, so `python ... >> lane.log` leaves the log frozen at its old
#     mtime for the whole run — no progress, and nothing left behind if the lane dies.
#     cmd's `>>` writes through, so python's flush=True lands on disk immediately.
#  2. One process per source: nypl runs on its own and is excluded from the sci lane
#     (CONTRACT.md 6-4 — parallelism WITHIN a source double-downloads and races on
#     the output filename).
#
#   .\scripts\launch_ingest_lanes.ps1              # all five lanes
#   .\scripts\launch_ingest_lanes.ps1 ia,web       # only the named lanes
#
# Take the lane names as ONE bag of leftover arguments. Declaring [string[]]$Only bound
# only the first name when the script was invoked through `powershell -File`, so asking
# for three lanes launched one and said nothing about the other two. Accepting everything
# and splitting on both comma and space makes `ia sci web_audio` and `ia,sci,web_audio`
# behave the same, and an unmatched name is now reported instead of silently dropped.
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Only)
if ($Only) { $Only = @($Only -split '[,\s]+' | Where-Object { $_ }) }

$py   = "C:\Users\aab15\AppData\Local\Programs\Python\Python310\python.exe"
$repo = "C:\Users\aab15\Documents\prime-documentary"
$led  = "E:\pd-media\assets\archive\_ledger"

# Lane set as of 2026-08-01. Owner directive: fetch material that is actually usable.
# What the contact-sheet review measured, and what each exclusion below costs nothing:
#   nypl      DROPPED — 26,914 of its 27,120 items are New York City directory PAGES.
#             10 of 10 sampled tiles were printed name/address listings. Zero b-roll.
#   ukna      DROPPED — the Discovery API is metadata-only ("0 media" on every call).
#             It cannot download anything; it had banked 3,336 catalogue records and 0 files.
#   rawpixel  DROPPED — search endpoint returns 403 behind Cloudflare, 0 items ever.
#   noaa      KEPT, but weather_disasters is skipped: that slice is ~360 GB of top-down
#             flood-survey plates graded 85-90% unusable, while the same source's
#             ocean_nature and wildlife_animals slices graded good.
#   ia        FINISHED 2026-07-31 05:15 ("sources exhausted at current queries") — not relaunched.
$lanes = @(
  @{ id = 'ia'      ; lane = 'ia' ; script = 'scripts\ingest_archive_sources.py'; opts = '--source ia'
     log = 'ingest_run1.log'       ; err = 'ingest_run1.err.log' },
  @{ id = 'gov'     ; lane = 'gov'; script = 'scripts\ingest_gov_archives.py'
     opts = "--source nara,loc --log-file ""$led\ingest_gov.log"""
     log = 'ingest_gov.console.log'; err = 'ingest_gov.err.log' },
  @{ id = 'sci'     ; lane = 'sci'; script = 'scripts\ingest_science_museum.py'
     opts = '--source nasa,noaa,met,smithsonian --skip-theme weather_disasters'
     log = 'ingest_sci.log'        ; err = 'ingest_sci.err.log' },
  # Split by source, not by theme. The single web lane walked its sources in order and
  # freesound comes first, so hours of audio ran before it ever reached a video source —
  # and moving footage is the scarce resource (6,089 clips against 60,081 stills).
  # Splitting is safe here precisely because the two sets share no source: parallelism
  # ACROSS sources is fine, within a source it double-downloads and races (CONTRACT 6-4).
  @{ id = 'web_video'; lane = 'web'; script = 'scripts\ingest_modern_web.py'
     opts = '--source mixkit,coverr,unsplash,pixabay_extra'
     log = 'ingest_web.log'        ; err = 'ingest_web.err.log' },
  @{ id = 'web_audio'; lane = 'web'; script = 'scripts\ingest_modern_web.py'
     opts = '--source freesound'
     log = 'ingest_web_audio.log'  ; err = 'ingest_web_audio.err.log' }
)

if ($Only) {
  $unknown = @($Only | Where-Object { $_ -notin $lanes.id })
  if ($unknown) { Write-Warning "unknown lane(s): $($unknown -join ', '); known: $($lanes.id -join ', ')" }
}

foreach ($l in $lanes) {
  if ($Only -and ($l.id -notin $Only)) { continue }
  $cmd = "set PD_INGEST_LANE=$($l.lane) && cd /d ""$repo"" && " +
         """$py"" $($l.script) $($l.opts) >> ""$led\$($l.log)"" 2>> ""$led\$($l.err)"""
  Start-Process cmd.exe -ArgumentList '/c', $cmd -WindowStyle Hidden
  Write-Output "launched [$($l.id)]: $($l.script) $($l.opts)"
  Start-Sleep -Seconds 3
}
