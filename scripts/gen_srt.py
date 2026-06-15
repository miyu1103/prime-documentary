"""Generate SRT subtitle file from narration MP3 segments.
Timing is based on actual audio duration (ffprobe), not visual scene duration.
"""
import subprocess, pathlib, sys, textwrap

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NARR_DIR = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_audio\narration")
OUT_SRT  = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\subs_s001_s023.srt")

TARGET_WORDS = 4   # aim for ~4 words per subtitle line

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

    ("vc_s008_v001.mp3",
     'But his case keeps climbing. The argument on appeal is narrow and sharp: '
     'that the confession should never have counted, because Miranda was never told the rights '
     'that might have changed whether he spoke at all. '
     'It is not a claim that he was tortured or tricked in some movie-villain way. '
     'It is something quieter — that the ordinary machinery of interrogation '
     'can extract words from a person who does not understand the ground he is standing on.'),

    ("vc_s009_v001.mp3",
     "And here is the detail most people never learn. "
     "Miranda's case did not travel to the Supreme Court alone. "
     "By the time it arrived, it had been combined with three other cases "
     "asking the very same question: "
     "Vignera v. New York. Westover v. United States. California v. Stewart. "
     "Four defendants. Four different interrogation rooms. One shared problem."),

    ("vc_s010_v001.mp3",
     "That combination is a signal. "
     "When the Supreme Court pulls four separate cases together under a single name, "
     "it is not trying to fix one man's bad day. "
     "It is looking at a pattern — a recurring gap in how the country questions people in custody. "
     "The justices were asking: what should have to be true, every time, "
     "before any of these confessions can be used at all?"),

    ("vc_s011_v001.mp3",
     "So the stakes quietly expand. "
     "This stops being the story of Ernesto Miranda "
     "and becomes a question about every locked interrogation room in the United States — "
     "and about the distance between having a right and actually knowing you have it. "
     "The Court now has to decide whether the Constitution demands "
     "that someone close that distance out loud, before the questioning begins."),

    ("vc_s012_v001.mp3",
     "On June 13, 1966, the Court answers. "
     "By a narrow margin — five votes to four — "
     "with Chief Justice Earl Warren writing for the majority, "
     "it rules that the prosecution may not use statements from a custodial interrogation "
     "unless it can show the suspect was first protected by clear safeguards."),

    ("vc_s013_v001.mp3",
     "And then the Court does something unusual: it spells the safeguards out. "
     "Before questioning, a person in custody must be told four things. "
     "That they have the right to remain silent. "
     "That anything they say can be used against them in court. "
     "That they have the right to a lawyer. "
     "And that if they cannot afford one, a lawyer will be appointed for them. "
     "Those four points are the heart of the whole decision."),

    ("vc_s014_v001.mp3",
     "Notice where the Court grounds all of this. "
     "Not in sympathy for suspects, but in the Fifth Amendment — "
     "the long-standing rule that the government cannot force you "
     "to be a witness against yourself. "
     "The warning, in the Court's reasoning, is simply what that promise requires "
     "once you are alone in a room with people whose job is to get you to talk."),

    ("vc_s015_v001.mp3",
     "It was not a comfortable decision, and it was not a lopsided one. "
     "Justices Harlan and White each dissented, "
     "arguing that the majority had reached beyond what the Constitution required, "
     "and warning that the new rule would tie the hands of legitimate police work. "
     "That disagreement still echoes today."),

    ("vc_s016_v001.mp3",
     "What happens next is the part you already know — "
     "you just did not know where it came from. "
     "Almost at once, those four points harden into a fixed routine. "
     "They get printed on cards, taped to station walls, "
     "and recited at the moment of arrest until they are nearly automatic. "
     "The country starts calling them by the name of the case: the Miranda warning."),

    ("vc_s017_v001.mp3",
     "And this is where the warning reveals what it really is. "
     "It is not politeness. It is a small, deliberate transfer of power. "
     "For a few seconds, the closed room is forced to open — "
     "to admit, out loud, that the person being questioned has choices. "
     "The warning does not free anyone and does not end interrogation. "
     "It just refuses to let the room pretend that the person inside it has no options."),

    ("vc_s018_v001.mp3",
     "Now the twist promised at the start. "
     "The warning carries Ernesto Miranda's name — but the ruling did not set him free. "
     "The Supreme Court reversed his original conviction, yes. "
     "But the state put him on trial a second time, "
     "and at that new trial he was convicted again, on other evidence. "
     "Sit with that. The most famous name in American criminal procedure "
     "belongs to a man who, in the end, was still found guilty. "
     "He did not win his freedom. He won something stranger and, for everyone else, far more lasting: a rule."),

    ("vc_s019_v001.mp3",
     "That is the quiet machinery underneath the phrase. "
     "The Miranda warning is not really about Ernesto Miranda at all. "
     "It is about the next person, and the next — "
     "the ones who will sit in that same kind of room long after his case is closed. "
     "By tying the warning to the Fifth Amendment and forcing it to be said before questioning, "
     "the Court took a principle that had always existed on paper "
     "and made it show up in the one place it had been easiest to ignore: "
     "the moment just before someone starts to talk."),

    ("vc_s020_v001.mp3",
     "So a system that had quietly run on the gap between having a right and knowing it "
     "now had to close that gap, out loud, every single time."),

    ("vc_s021_v001.mp3",
     "Step back and the shape of it is clear. "
     "We started with a sentence that sounds like set dressing from a crime drama. "
     "It is anything but. "
     "Strip away the television associations and what is left is structural — "
     "a line drawn around how the state is allowed to gather the most damning evidence of all: your own words. "
     "It is a repair the Supreme Court bolted onto the Fifth Amendment in 1966 — "
     "built out of four plain sentences — "
     "because the room where confessions are made was tilted against the person inside it."),

    ("vc_s022_v001.mp3",
     "And the man who gave it his name never got the ending you would expect. "
     "He won at the highest court in the country and still went back to prison. "
     "The warning outlived his case, because it was never really his. "
     "It was a structural fix, written for everyone who would ever be questioned after him."),

    ("vc_s023_v001.mp3",
     "That is the hidden system behind you have the right to remain silent: "
     "not a courtesy, but a rule that quietly rebalances every arrest in America. "
     "If you want to see how a single case can rewire the country's most ordinary moments, "
     "this channel is built for exactly that — "
     "and the next landmark we open changed who even gets a lawyer in the first place. "
     "Until then: now you know why they have to read you your rights."),
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


def to_chunks(text: str, target: int = TARGET_WORDS) -> list[str]:
    """Split at natural phrase boundaries (sentence > clause > word midpoint)."""
    import re
    # 1. Split at sentence endings
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks: list[str] = []
    for sent in sents:
        words = sent.split()
        if len(words) <= int(target * 1.6):
            chunks.append(sent.strip())
            continue
        # 2. Split at clause boundaries (—, :, ;, comma followed by space)
        clauses = re.split(r'\s*(?:—|–)\s*|(?<=[,;:])\s+', sent)
        buf: list[str] = []
        for clause in clauses:
            cw = clause.split()
            if len(buf) + len(cw) <= int(target * 1.6):
                buf.extend(cw)
            else:
                if buf:
                    chunks.append(" ".join(buf))
                buf = cw
        if buf:
            chunks.append(" ".join(buf))
    # 3. Split any remaining overlong chunk at word midpoint
    result: list[str] = []
    for ch in chunks:
        w = ch.split()
        if len(w) > int(target * 2):
            mid = len(w) // 2
            result.append(" ".join(w[:mid]))
            result.append(" ".join(w[mid:]))
        else:
            result.append(ch)
    return [r for r in result if r.strip()]


def main() -> None:
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    entries: list[str] = []
    idx     = 1
    cursor  = 0.0

    for filename, text in SEGMENTS:
        mp3  = NARR_DIR / filename
        dur  = get_duration(mp3)
        chunks = to_chunks(text, TARGET_WORDS)
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
