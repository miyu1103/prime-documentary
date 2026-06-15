"""Generate narration for scenes S008-S018 via ElevenLabs TTS."""
import sys, pathlib, urllib.request, urllib.error, json

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env

SCENES = {
    "vc_s008_v001": (
        "But his case keeps climbing. The argument on appeal is narrow and sharp: "
        "that the confession should never have counted, because Miranda was never told the rights "
        "that might have changed whether he spoke at all. "
        "It is not a claim that he was tortured or tricked in some movie-villain way. "
        "It is something quieter — that the ordinary machinery of interrogation "
        "can extract words from a person who does not understand the ground he is standing on."
    ),
    "vc_s009_v001": (
        "And here is the detail most people never learn. "
        "Miranda's case did not travel to the Supreme Court alone. "
        "By the time it arrived, it had been combined with three other cases "
        "asking the very same question: "
        "Vignera v. New York. Westover v. United States. California v. Stewart. "
        "Four defendants. Four different interrogation rooms. One shared problem."
    ),
    "vc_s010_v001": (
        "That combination is a signal. "
        "When the Supreme Court pulls four separate cases together under a single name, "
        "it is not trying to fix one man's bad day. "
        "It is looking at a pattern — a recurring gap in how the country questions people in custody. "
        "The justices were asking: what should have to be true, every time, "
        "before any of these confessions can be used at all?"
    ),
    "vc_s011_v001": (
        "So the stakes quietly expand. "
        "This stops being the story of Ernesto Miranda "
        "and becomes a question about every locked interrogation room in the United States — "
        "and about the distance between having a right and actually knowing you have it. "
        "The Court now has to decide whether the Constitution demands "
        "that someone close that distance out loud, before the questioning begins."
    ),
    "vc_s012_v001": (
        "On June 13, 1966, the Court answers. "
        "By a narrow margin — five votes to four — "
        "with Chief Justice Earl Warren writing for the majority, "
        "it rules that the prosecution may not use statements from a custodial interrogation "
        "unless it can show the suspect was first protected by clear safeguards."
    ),
    "vc_s013_v001": (
        "And then the Court does something unusual: it spells the safeguards out. "
        "Before questioning, a person in custody must be told four things. "
        "That they have the right to remain silent. "
        "That anything they say can be used against them in court. "
        "That they have the right to a lawyer. "
        "And that if they cannot afford one, a lawyer will be appointed for them. "
        "Those four points are the heart of the whole decision."
    ),
    "vc_s014_v001": (
        "Notice where the Court grounds all of this. "
        "Not in sympathy for suspects, but in the Fifth Amendment — "
        "the long-standing rule that the government cannot force you "
        "to be a witness against yourself. "
        "The warning, in the Court's reasoning, is simply what that promise requires "
        "once you are alone in a room with people whose job is to get you to talk."
    ),
    "vc_s015_v001": (
        "It was not a comfortable decision, and it was not a lopsided one. "
        "Justices Harlan and White each dissented, "
        "arguing that the majority had reached beyond what the Constitution required, "
        "and warning that the new rule would tie the hands of legitimate police work. "
        "That disagreement still echoes today."
    ),
    "vc_s016_v001": (
        "What happens next is the part you already know — "
        "you just did not know where it came from. "
        "Almost at once, those four points harden into a fixed routine. "
        "They get printed on cards, taped to station walls, "
        "and recited at the moment of arrest until they are nearly automatic. "
        "The country starts calling them by the name of the case: the Miranda warning."
    ),
    "vc_s017_v001": (
        "And this is where the warning reveals what it really is. "
        "It is not politeness. It is a small, deliberate transfer of power. "
        "For a few seconds, the closed room is forced to open — "
        "to admit, out loud, that the person being questioned has choices. "
        "The warning does not free anyone and does not end interrogation. "
        "It just refuses to let the room pretend that the person inside it has no options."
    ),
    "vc_s018_v001": (
        "Now the twist promised at the start. "
        "The warning carries Ernesto Miranda's name — but the ruling did not set him free. "
        "The Supreme Court reversed his original conviction, yes. "
        "But the state put him on trial a second time, "
        "and at that new trial he was convicted again, on other evidence. "
        "Sit with that. The most famous name in American criminal procedure "
        "belongs to a man who, in the end, was still found guilty. "
        "He did not win his freedom. He won something stranger and, for everyone else, far more lasting: a rule."
    ),
}

def tts(api_key, voice_id, text, out_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    body = json.dumps({
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.50, "similarity_boost": 0.75,
                           "style": 0.0, "use_speaker_boost": True},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
        headers={"xi-api-key": api_key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        audio = r.read()
    out_path.write_bytes(audio)
    return len(audio)

def main():
    env = load_env(ROOT / ".env")
    api_key = env.get("ELEVENLABS_API_KEY", "")
    voice_id = env.get("ELEVENLABS_VOICE_ID", "")
    if not api_key or not voice_id:
        print("ERROR: .env にキーがありません"); sys.exit(1)
    out_dir = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_audio\narration")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in SCENES.items():
        path = out_dir / f"{name}.mp3"
        kb = tts(api_key, voice_id, text, path) // 1024
        print(f"OK: {name}.mp3  ({kb} KB)")

if __name__ == "__main__":
    main()
