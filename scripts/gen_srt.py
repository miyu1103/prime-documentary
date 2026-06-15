"""Generate SRT subtitle file from narration MP3 segments.
Timing is based on actual audio duration (ffprobe), not visual scene duration.
"""
import subprocess, pathlib, sys, textwrap

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NARR_DIR = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_audio\narration")
OUT_SRT  = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\subs_s001_s007.srt")

WORDS_PER_CHUNK = 10

SEGMENTS = [
    ("vc_hook_v001.mp3",
     '"You have the right to remain silent." You have heard it in a thousand movies, '
     'and maybe once in real life. But that sentence was not written by a screenwriter. '
     'It comes from a single confession that the Supreme Court of the United States refused to allow '
     '— given by a man who won his case at the highest court in the land and still ended up back in prison. '
     'This is how four sentences rewrote every arrest in America.'),

    ("vc_opening_v001.mp3",
     'We treat the warning as a courtesy — a few words an officer mutters while the handcuffs go on. '
     'It is not a courtesy. It is a repair. '
     'In 1966, the Supreme Court decided that the real problem was not any single officer or any single suspect. '
     'The problem was the interrogation room itself: a closed space where steady pressure can turn silence into a confession. '
     'So the Court built a fix, and it anchored that fix in the Fifth Amendment — '
     'the promise that no person can be forced to be a witness against themselves. '
     'Over the next twelve minutes: the case that created the warning, the man whose name it carries, '
     'and why those few words quietly shape every arrest.'),

    ("vc_s003_v001.mp3",
     'It begins in Phoenix, Arizona, in 1963. '
     'A man named Ernesto Miranda is arrested and taken in for questioning. '
     'What happens next is, on the surface, completely ordinary — and that is exactly why it matters.'),

    ("vc_s004_v001.mp3",
     'He is placed in a room with police and questioned. '
     'And during that questioning, he confesses. '
     'He is never told that he does not have to say anything. '
     'He is never told that he could have a lawyer sitting beside him.'),

    ("vc_s005_v001.mp3",
     'Think about what that room actually is. '
     'On one side: trained investigators who do this every day, '
     'who control the door, the clock, and the questions. '
     'On the other side: one person, alone, who may have no idea where the limits are — '
     'whether he can stop, whether he can wait, whether anyone is coming to help. '
     'Nothing dramatic has to happen for that imbalance to do its work. '
     'The room is quiet. The pressure is patient. '
     'And the longer it lasts, the more natural it feels to fill the silence — '
     'to explain, to correct, to try to talk your way out. '
     'That instinct, to keep talking, is exactly what the room is built to use.'),

    ("vc_s006_v001.mp3",
     'And at the end of it, the most powerful piece of evidence in the entire case '
     'is something the suspect produced himself: his own words. '
     'A confession feels like proof beyond argument. '
     'Who would admit to something they did not do? '
     'But the law had started to ask a harder question — '
     'not did he say it, but did he know he had a choice? '
     'Because a confession only means what we think it means '
     'if the person giving it understood that silence was an option. '
     'In that Phoenix interrogation room, no one had told Ernesto Miranda that it was.'),

    ("vc_s007_v001.mp3",
     'That confession does not stay in the room. '
     'It becomes evidence in court, and on the strength of it, Miranda is convicted. '
     'For most defendants, that would be the end of the road. '
     'A confession is admitted, a jury hears it, a verdict follows.'),
]


FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

def get_duration(mp3: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(mp3)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def to_srt_ts(t: float) -> str:
    h  = int(t // 3600)
    m  = int((t % 3600) // 60)
    s  = int(t % 60)
    ms = int(round((t % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_chunks(text: str, size: int) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def main() -> None:
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    entries: list[str] = []
    idx     = 1
    cursor  = 0.0

    for filename, text in SEGMENTS:
        mp3  = NARR_DIR / filename
        dur  = get_duration(mp3)
        chunks = to_chunks(text, WORDS_PER_CHUNK)
        cpf    = dur / len(chunks) if chunks else 0
        print(f"{filename}: {dur:.2f}s → {len(chunks)} chunks @ {cpf:.2f}s each")

        for ci, chunk in enumerate(chunks):
            t_start = cursor + ci * cpf
            t_end   = cursor + (ci + 1) * cpf - 0.05
            entries.append(
                f"{idx}\n{to_srt_ts(t_start)} --> {to_srt_ts(t_end)}\n{chunk}"
            )
            idx += 1

        cursor += dur

    OUT_SRT.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    print(f"\nOK: {OUT_SRT}  ({idx-1} entries, total {cursor:.1f}s)")


if __name__ == "__main__":
    main()
