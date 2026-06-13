from __future__ import annotations


from pd_factory.studio import EpisodeView
from pd_factory.web import handle_run, render_index, render_result


def test_render_index_has_form_and_disclaimer():
    html = render_index()
    assert "<form method=post action='/run'>" in html
    assert "name=theme" in html
    assert "公開不可" in html  # safety disclaimer is shown


def test_render_index_shows_error():
    assert "bad theme" in render_index(error="bad theme")


def test_render_result_escapes_user_content():
    view = EpisodeView(
        episode_id="PD-2026-001-x",
        theme="<script>alert(1)</script>",
        final_state="script_draft",
        produced=["script"],
        qc={"result": "pass_with_warnings", "findings": []},
        script={"spans": [{"narrative_function": "hook", "text": "Hello <b>"}]},
        scene_plan={"scenes": [{"scene_id": "S001", "purpose": "p", "visual_mode": "object", "duration_seconds": 2}]},
        thesis={"final_thesis": "T"},
    )
    html = render_result(view)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
    assert "pass_with_warnings" in html
    assert "S001" in html


def test_handle_run_rejects_short_theme(tmp_path):
    status, html = handle_run({"theme": ["ab"]}, tmp_path)
    assert status == 400
    assert "<form" in html  # falls back to the index with an error


def test_handle_run_full_flow(tmp_path):
    status, html = handle_run({"theme": ["How paper is recycled"]}, tmp_path)
    assert status == 200
    assert "How paper is recycled" in html
    assert "QC" in html
