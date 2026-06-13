"""Deterministic auto-selection for the music and visual-motif libraries.

Goals (decision 0002 §C/§B):
- match a scene's need (category/function/mood/energy or motif/orientation),
- avoid reusing the same asset within the most recent N episodes,
- spread usage (prefer least-used) and stay fully deterministic — no randomness,
  so a given (registry, request, recent-history) always yields the same pick and
  reruns are idempotent.

If every match was used recently, the constraint is RELAXED (rather than failing):
the least-recently/least-used matching asset is returned and the caller can see it
was a forced reuse. Only a total absence of any category/motif match raises.
"""
from __future__ import annotations

from typing import Any

Track = dict[str, Any]
Motif = dict[str, Any]


class NoCandidateError(RuntimeError):
    """No asset in the registry matches the request at all (not merely 'used recently')."""


def _energy_distance(track: Track, energy: int | None) -> int:
    if energy is None or "energy" not in track:
        return 0
    return abs(int(track["energy"]) - int(energy))


def select_track(
    *,
    registry: list[Track],
    category: str,
    mood: str | None = None,
    energy: int | None = None,
    recent_track_ids: set[str] | frozenset[str] | None = None,
) -> Track:
    """Pick one music track for a scene.

    Selection order: category must match; if mood given it must match; then rank by
    (not-recently-used first, energy closeness, reuse_count asc, track_id asc).
    Raises NoCandidateError if nothing matches category(+mood).
    """
    recent = set(recent_track_ids or ())
    candidates = [t for t in registry if t.get("category") == category]
    if mood is not None:
        moody = [t for t in candidates if t.get("mood") == mood]
        candidates = moody or candidates  # mood is a preference, not a hard filter
    if not candidates:
        raise NoCandidateError(f"no music track for category={category!r}")

    def key(t: Track) -> tuple:
        return (
            t.get("track_id") in recent,          # False (fresh) sorts before True
            _energy_distance(t, energy),
            int(t.get("reuse_count", 0)),
            str(t.get("track_id", "")),
        )

    return sorted(candidates, key=key)[0]


def select_motif(
    *,
    registry: list[Motif],
    motif: str,
    mood: str | None = None,
    orientation: str | None = None,
    recent_motif_ids: set[str] | frozenset[str] | None = None,
) -> Motif:
    """Pick one reusable visual motif. Same rules as :func:`select_track`."""
    recent = set(recent_motif_ids or ())
    candidates = [m for m in registry if m.get("motif") == motif]
    if orientation is not None:
        oriented = [m for m in candidates if m.get("orientation") == orientation]
        candidates = oriented or candidates
    if mood is not None:
        moody = [m for m in candidates if m.get("mood") == mood]
        candidates = moody or candidates
    if not candidates:
        raise NoCandidateError(f"no visual motif for motif={motif!r}")

    def key(m: Motif) -> tuple:
        return (
            m.get("motif_id") in recent,
            int(m.get("reuse_count", 0)),
            str(m.get("motif_id", "")),
        )

    return sorted(candidates, key=key)[0]
