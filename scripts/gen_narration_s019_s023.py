"""Generate narration for scenes S019-S023 via ElevenLabs TTS."""
import sys, pathlib, urllib.request, json

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
    "vc_s019_v001": (
        "That is the quiet machinery underneath the phrase. "
        "The Miranda warning is not really about Ernesto Miranda at all. "
        "It is about the next person, and the next — "
        "the ones who will sit in that same kind of room long after his case is closed. "
        "By tying the warning to the Fifth Amendment and forcing it to be said before questioning, "
        "the Court took a principle that had always existed on paper "
        "and made it show up in the one place it had been easiest to ignore: "
        "the moment just before someone starts to talk."
    ),
    "vc_s020_v001": (
        "So a system that had quietly run on the gap between having a right and knowing it "
        "now had to close that gap, out loud, every single time."
    ),
    "vc_s021_v001": (
        "Step back and the shape of it is clear. "
        "We started with a sentence that sounds like set dressing from a crime drama. "
        "It is anything but. "
        "Strip away the television associations and what is left is structural — "
        "a line drawn around how the state is allowed to gather the most damning evidence of all: your own words. "
        "It is a repair the Supreme Court bolted onto the Fifth Amendment in 1966 — "
        "built out of four plain sentences — "
        "because the room where confessions are made was tilted against the person inside it."
    ),
    "vc_s022_v001": (
        "And the man who gave it its name never got the ending you would expect. "
        "He won at the highest court in the country and still went back to prison. "
        "The warning outlived his case, because it was never really his. "
        "It was a structural fix, written for everyone who would ever be questioned after him."
    ),
    "vc_s023_v001": (
        "That is the hidden system behind 'you have the right to remain silent': "
        "not a courtesy, but a rule that quietly rebalances every arrest in America. "
        "If you want to see how a single case can rewire the country's most ordinary moments, "
        "this channel is built for exactly that — "
        "and the next landmark we open changed who even gets a lawyer in the first place. "
        "Until then: now you know why they have to read you your rights."
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
    api_key  = env.get("ELEVENLABS_API_KEY", "")
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
