"""Reusable asset libraries: music tracks and visual motifs (decision 0002 §C, §B).

Music is not generated per episode; a tagged registry is built once (Suno) and
tracks are auto-selected per scene. Generic visual motifs are likewise reused
across episodes. Both selectors are deterministic and avoid reuse within the most
recent N episodes (no randomness — see selection.py).
"""
from __future__ import annotations

from .selection import (
    NoCandidateError,
    select_motif,
    select_track,
)

__all__ = ["NoCandidateError", "select_track", "select_motif"]
