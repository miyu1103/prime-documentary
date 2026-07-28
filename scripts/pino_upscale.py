import os, base64, requests, cv2, numpy as np
SRC = r"H:\pd-media\assets\characters\pino\expressions"
DST = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino\hires"
os.makedirs(DST, exist_ok=True)
API = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"
USED = ["neutral_v001.png","waving_v001.png","happy_v002.png","talking_v001.png",
        "idea_v003.png","pointing_v001.png","thinking_v002.png"]
for fn in USED:
    bgr = cv2.imread(os.path.join(SRC, fn))
    ok, buf = cv2.imencode(".png", bgr)
    r = requests.post(API, json={"image": base64.b64encode(buf).decode(),
        "upscaling_resize": 4, "upscaler_1": "R-ESRGAN 4x+", "upscaler_2": "None"}, timeout=300)
    out = cv2.imdecode(np.frombuffer(base64.b64decode(r.json()["image"]), np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite(os.path.join(DST, fn), out)
    print(fn, out.shape, flush=True)
print("DONE")
