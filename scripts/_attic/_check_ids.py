import sys, json, urllib.parse, urllib.request
sys.path.insert(0,'src'); sys.path.insert(0,'scripts')
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
env=load_env(); tok=_access_token(env)
ids="1FHZ5qA6pgA,lDpfSAuFMS8"
r=urllib.request.Request('https://www.googleapis.com/youtube/v3/videos?'+urllib.parse.urlencode({'part':'snippet,status,contentDetails','id':ids}),headers={'Authorization':f'Bearer {tok}'})
with urllib.request.urlopen(r,timeout=90) as resp: v=json.loads(resp.read().decode())
for it in v['items']:
    st=it['status']; sn=it['snippet']; cd=it['contentDetails']
    print(json.dumps({'id':it['id'],'privacy':st.get('privacyStatus'),'publishAt':st.get('publishAt'),'dur':cd.get('duration'),'uploadStatus':st.get('uploadStatus'),'title':sn['title']},ensure_ascii=False))
