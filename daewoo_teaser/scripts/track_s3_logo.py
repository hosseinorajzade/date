# Track the DAEWOO logo in shot S3 (bright, low-saturation text) so the neon outline can follow it.
import cv2, numpy as np, subprocess, json
W,H=1080,1920
raw=subprocess.run(['ffmpeg','-v','error','-i','remotion/public/clips/s3.mp4','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
fr=[np.frombuffer(raw[i:i+W*H*3],np.uint8).reshape(H,W,3) for i in range(0,len(raw),W*H*3)]
Y0,Y1=560,820
boxes=[]; prev=None; wid=None
for n,f in enumerate(fr):
    roi=f[Y0:Y1]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    m=((hsv[...,2]>135)&(hsv[...,1]<70)).astype(np.uint8)
    m=cv2.dilate(m,np.ones((9,25),np.uint8))
    k,lab,st,_=cv2.connectedComponentsWithStats(m)
    cands=[i for i in range(1,k) if st[i,cv2.CC_STAT_AREA]>300]
    if prev is not None:
        cands=[i for i in cands if st[i,0]<prev[2]+40 and st[i,0]+st[i,2]>prev[0]-40]
    if not cands:
        boxes.append(None); continue
    i=max(cands,key=lambda i:st[i,cv2.CC_STAT_AREA])
    x,y,w,h=st[i,:4]; x0,y0,x1,y1=x+12,Y0+y+4,x+w-12,Y0+y+h-4   # undo dilation
    if x0>8 and wid is None: wid=x1-x0
    if x0<=8 and wid is not None: x0=x1-wid*(1+0.0005*n)
    prev=[x0,y0,x1,y1]; boxes.append(prev)
    if x1<40: break
valid=[b for b in boxes if b is not None]
print(len(fr),'frames; tracked',len(valid),'first',boxes[0],'last',valid[-1],'width',wid)
arr=np.array([b if b is not None else [np.nan]*4 for b in boxes],float)
# smooth (centered moving average, ignoring gaps)
k=5; sm=arr.copy()
for j in range(4):
    v=arr[:,j]
    for n in range(len(v)):
        w=v[max(0,n-k//2):n+k//2+1]; w=w[~np.isnan(w)]
        sm[n,j]=w.mean() if len(w) else np.nan
json.dump([None if np.isnan(r).any() else [round(float(x),1) for x in r] for r in sm],open('remotion/src/s3Logo.json','w'))
for n in (0,30,60,75):
    if n<len(sm) and not np.isnan(sm[n]).any():
        d=fr[n].copy(); x0,y0,x1,y1=sm[n].astype(int); cv2.rectangle(d,(x0-28,y0-24),(x1+28,y1+24),(0,255,0),3)
        cv2.imwrite(f'work/s3logo_{n}.png',cv2.resize(d[450:950],None,fx=0.5,fy=0.5))
