import sys, json, urllib.parse, urllib.request
sys.path.insert(0,'src'); sys.path.insert(0,'scripts')
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import get_channel_id
env=load_env(); tok=_access_token(env)
def rj(u):
    r=urllib.request.Request(u,headers={'Authorization':f'Bearer {tok}'})
    with urllib.request.urlopen(r,timeout=120) as resp: return json.loads(resp.read().decode())
ch=get_channel_id(tok)
c=rj('https://www.googleapis.com/youtube/v3/channels?'+urllib.parse.urlencode({'part':'contentDetails','id':ch}))
up=c['items'][0]['contentDetails']['relatedPlaylists']['uploads']
pl=rj('https://www.googleapis.com/youtube/v3/playlistItems?'+urllib.parse.urlencode({'part':'contentDetails','playlistId':up,'maxResults':40}))
ids=[i['contentDetails']['videoId'] for i in pl['items']]
out=[]
for i in range(0,len(ids),50):
    v=rj('https://www.googleapis.com/youtube/v3/videos?'+urllib.parse.urlencode({'part':'snippet,status,contentDetails','id':','.join(ids[i:i+50])}))
    out+=v['items']
print('COUNT',len(out))
for it in out:
    st=it['status']; sn=it['snippet']; cd=it['contentDetails']
    print(json.dumps({'id':it['id'],'privacy':st.get('privacyStatus'),'publishAt':st.get('publishAt'),'dur':cd.get('duration'),'uploadStatus':st.get('uploadStatus'),'title':sn['title']},ensure_ascii=False))
