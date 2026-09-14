#!/usr/bin/env python3
from __future__ import annotations
import json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

EP = 'PD-2026-005-madoff'
EPDIR = ROOT / 'episodes' / EP
META = EPDIR / '09_package' / 'youtube_meta.final.v010.polished.json'
UPLOAD = EPDIR / '09_package' / 'upload_result.final.v009.json'
OUT = EPDIR / '09_package' / 'youtube_update_result.final.v010.json'

def req_json(url: str, token: str, *, method='GET', body=None):
    data = None if body is None else json.dumps(body).encode('utf-8')
    headers = {'Authorization': f'Bearer {token}'}
    if data is not None:
        headers['Content-Type'] = 'application/json; charset=UTF-8'
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    meta = json.loads(META.read_text('utf-8'))
    upload = json.loads(UPLOAD.read_text('utf-8'))
    video_id = upload['video_id']
    token = _access_token(load_env())

    get_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={video_id}'
    current = req_json(get_url, token)
    if not current.get('items'):
        raise RuntimeError(f'video not found: {video_id}')
    cur = current['items'][0]
    status = cur.get('status', {})
    snippet = cur.get('snippet', {})

    new_snippet = {
        'categoryId': meta.get('categoryId', snippet.get('categoryId', '27')),
        'title': meta['title'],
        'description': meta['description'],
        'tags': meta.get('tags', []),
        'defaultLanguage': meta.get('defaultLanguage', 'en'),
        'defaultAudioLanguage': meta.get('defaultAudioLanguage', 'en'),
    }
    new_status = {
        'privacyStatus': status.get('privacyStatus', 'private'),
        'selfDeclaredMadeForKids': False,
        'containsSyntheticMedia': True,
        'license': status.get('license', 'youtube'),
        'embeddable': status.get('embeddable', True),
        'publicStatsViewable': status.get('publicStatsViewable', True),
    }
    # Stay private unless an explicit publish step changes it.
    new_status['privacyStatus'] = 'private'

    body = {'id': video_id, 'snippet': new_snippet, 'status': new_status}
    update_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,status'
    updated = req_json(update_url, token, method='PUT', body=body)
    verified = req_json(get_url, token)
    result = {
        'episode_id': EP,
        'video_id': video_id,
        'watch': f'https://youtu.be/{video_id}',
        'studio': f'https://studio.youtube.com/video/{video_id}/edit',
        'meta_revision': meta['revision'],
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'updated': updated,
        'verified': verified,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    item = verified['items'][0]
    print('UPDATED_OK')
    print('title=' + item['snippet'].get('title',''))
    print('privacy=' + item['status'].get('privacyStatus',''))
    print('madeForKids=' + str(item['status'].get('selfDeclaredMadeForKids')))
    print('containsSyntheticMedia=' + str(item['status'].get('containsSyntheticMedia')))
    print('result=' + str(OUT))

if __name__ == '__main__':
    main()
