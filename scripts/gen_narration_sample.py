"""Generate narration audio for the HOOK section via ElevenLabs TTS."""
import os
import sys
import pathlib
import urllib.request
import urllib.error
import json

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"

def load_env(path: pathlib.Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env

HOOK_TEXT = (
    '"You have the right to remain silent." '
    "You have heard it in a thousand movies, and maybe once in real life. "
    "But that sentence was not written by a screenwriter. "
    "It comes from a single confession that the Supreme Court of the United States refused to allow "
    "— given by a man who won his case at the highest court in the land and still ended up back in prison. "
    "This is how four sentences rewrote every arrest in America."
)

def main() -> None:
    env = load_env(ENV_FILE)
    api_key = env.get("ELEVENLABS_API_KEY", "")
    voice_id = env.get("ELEVENLABS_VOICE_ID", "")

    if not api_key or not voice_id:
        print("ERROR: ELEVENLABS_API_KEY または ELEVENLABS_VOICE_ID が .env にありません")
        sys.exit(1)

    out_dir = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_audio\narration")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "vc_hook_v001.mp3"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": HOOK_TEXT,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )

    print(f"ElevenLabs へ送信中... voice_id={voice_id[:6]}***")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio = resp.read()
    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        print(f"ERROR HTTP {e.code}: {body_err}")
        sys.exit(1)

    out_path.write_bytes(audio)
    kb = len(audio) // 1024
    print(f"OK: {out_path}  ({kb} KB)")
    print(f"テキスト: {len(HOOK_TEXT.split())} 語 / 約30秒")

if __name__ == "__main__":
    main()
