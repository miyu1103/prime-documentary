"""Shared SDXL presets used by local generation scripts.

The profiles intentionally stay explicit and conservative so scripts can switch
quality mode without changing scene prompts.
"""

from __future__ import annotations


SDXL_PRESETS: dict[str, dict[str, object]] = {
    "ultra": {
        "name": "ultra",
        "model": "juggernautXL_ragnarokBy.safetensors",
        "width": 1664,
        "height": 936,
        "steps": 72,
        "cfg_scale": 6.4,
        "sampler_name": "DPM++ 2M",
        "scheduler": "Karras",
        "enable_hr": True,
        "hr_scale": 1.8,
        "denoising_strength": 0.30,
        "hr_second_pass_steps": 50,
        "hr_upscaler": "R-ESRGAN 4x+",
    },
    "max": {
        "name": "max",
        "model": "juggernautXL_ragnarokBy.safetensors",
        "width": 1536,
        "height": 864,
        "steps": 60,
        "cfg_scale": 6.2,
        "sampler_name": "DPM++ 2M",
        "scheduler": "Karras",
        "enable_hr": True,
        "hr_scale": 1.6,
        "denoising_strength": 0.33,
        "hr_second_pass_steps": 35,
        "hr_upscaler": "R-ESRGAN 4x+",
    },
    "high": {
        "name": "high",
        "model": "juggernautXL_ragnarokBy.safetensors",
        "width": 1536,
        "height": 864,
        "steps": 48,
        "cfg_scale": 5.8,
        "sampler_name": "DPM++ 2M",
        "scheduler": "Karras",
        "enable_hr": True,
        "hr_scale": 1.45,
        "denoising_strength": 0.35,
        "hr_second_pass_steps": 28,
        "hr_upscaler": "Latent",
    },
    "preview": {
        "name": "preview",
        "model": "juggernautXL_ragnarokBy.safetensors",
        "width": 1216,
        "height": 684,
        "steps": 28,
        "cfg_scale": 5.0,
        "sampler_name": "DPM++ 2M",
        "scheduler": "Karras",
        "enable_hr": False,
    },
}


def get_sdxl_profile(name: str = "max") -> dict[str, object]:
    """Return the SDXL profile for generation.

    Args:
        name: one of "ultra", "max", "high", or "preview". Unrecognized values fall back
        to "max" to avoid silent failures in automated runs.
    """
    return SDXL_PRESETS.get(name, SDXL_PRESETS["max"]).copy()


def available_sdxl_profiles() -> list[str]:
    """Return the list of profile names in deterministic order."""
    return sorted(SDXL_PRESETS.keys())
