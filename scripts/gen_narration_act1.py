"""Generate narration for ACT I scenes S003-S007 via ElevenLabs TTS."""
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
    "vc_s003_v001": (
        "It begins in Phoenix, Arizona, in 1963. "
        "A man named Ernesto Miranda is arrested and taken in for questioning. "
        "What happens next is, on the surface, completely ordinary — "
        "and that is exactly why it matters."
    ),
    "vc_s004_v001": (
        "He is placed in a room with police and questioned. "
        "And during that questioning, he confesses. "
        "He is never told that he does not have to say anything. "
        "He is never told that he could have a lawyer sitting beside him."
    ),
    "vc_s005_v001": (
        "Think about what that room actually is. "
        "On one side: trained investigators who do this every day, "
        "who control the door, the clock, and the questions. "
        "On the other side: one person, alone, who may have no idea where the limits are — "
        "whether he can stop, whether he can wait, whether anyone is coming to help. "
        "Nothing dramatic has to happen for that imbalance to do its work. "
        "The room is quiet. The pressure is patient. "
        "And the longer it lasts, the more natural it feels to fill the silence — "
        "to explain, to correct, to try to talk your way out. "
        "That instinct, to keep talking, is exactly what the room is built to use."
    ),
    "vc_s006_v001": (
        "And at the end of it, the most powerful piece of evidence in the entire case "
        "is something the suspect produced himself: his own words. "
        "A confession feels like proof beyond argument. "
        "Who would admit to something they did not do? "
        "But the law had started to ask a harder question — "
        "not did he say it, but did he know he had a choice? "
        "Because a confession only means what we think it means "
        "if the person giving it understood that silence was an option. "
        "In that Phoenix interrogation room, no one had told Ernesto Miranda that it was."
    ),
    "vc_s007_v001": (
        "That confession does not stay in the room. "
        "It becomes evidence in court, and on the strength of it, Miranda is convicted. "
        "For most defendants, that would be the end of the road. "
        "A confession is admitted, a jury hears it, a verdict follows."
    ),
}

def tts(api_key, voice_id, text, out_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    body = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.50, "similarity_boost": 0.75,
                           "style": 0.0, "use_speaker_boost": True},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST")
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
