# 19 — Folder, Naming and Artifact Specification

## 1. Repository Layout

```text
repo/
├─ CLAUDE.md
├─ docs/
├─ .claude/
├─ config/
├─ schemas/
├─ src/
├─ tests/
├─ scripts/
├─ templates/
├─ episodes/
├─ library/
└─ runtime/
```

## 2. Episode Layout

```text
episodes/PD-2026-001-example/
├─ manifest.json
├─ events.jsonl
├─ approvals/
├─ 00_topic/
├─ 01_research/
├─ 02_story/
├─ 03_script/
├─ 04_scenes/
├─ 05_visuals/
├─ 06_voice/
├─ 07_music/
├─ 08_edit/
├─ 09_publish/
├─ 10_analytics/
└─ logs/
```

## 3. Detailed Layout

```text
01_research/
├─ plan.v001.json
├─ sources.v001.json
├─ claims.v001.json
├─ chronology.v001.json
├─ contradictions.v001.json
└─ qc.v001.json

03_script/
├─ thesis.v001.json
├─ outline.v001.json
├─ script.en.v001.md
├─ script.annotated.v001.json
├─ pronunciation.v001.json
├─ qc.v001.json
└─ diffs/

04_scenes/
├─ scene_plan.v001.json
├─ shot_plan.v001.json
├─ visual_bible.v001.json
├─ motion_plan.v001.json
└─ qc.v001.json

05_visuals/
├─ requests/
├─ raw/
├─ candidates/
├─ approved/
├─ rejected/
├─ contact_sheets/
└─ qc/

06_voice/
├─ chunks/
├─ draft/
├─ master/
├─ alignment/
└─ qc/

08_edit/
├─ plans/
├─ timelines/
├─ projects/
├─ renders/
├─ markers/
└─ qc/
```

## 4. File Naming

推奨：

`{entity_id}.{artifact_type}.{revision}.{extension}`

例：

- `S013.visual_spec.v003.json`
- `PD-2026-001-S013-IMG-002.candidate.v001.png`
- `VO-014.master.v002.wav`
- `timeline.review.v004.json`

禁止：

- final
- final2
- new
- latest
- use_this
- fixed
- aaa

## 5. Hashing

- content hash
- generation input hash
- file checksum
- config revision hash
- source snapshot hash where permitted

## 6. Artifact Registry

- artifact_id
- entity_type
- entity_id
- revision
- artifact_type
- logical_uri
- local_cache_paths
- mime_type
- size
- checksum
- created_at
- created_by
- provenance
- rights_status
- QC status
- active/superseded

## 7. Temporary Files

runtime/tempへ置き、episode正式成果物と混ぜない。

- automatic cleanup policy
- job owner
- expiration
- incomplete marker
- never treated as approved

## 8. Retention Policy

永久保存候補：

- manifest
- events
- approvals
- research metadata
- final claims
- final script
- approved assets
- master audio
- final project/timeline
- final renders
- rights evidence
- publish package
- analytics

期間後削除候補：

- rejected raw candidates
- temporary previews
- duplicate caches
- failed partial files
- low-quality draft voice

削除前に参照関係を確認する。
