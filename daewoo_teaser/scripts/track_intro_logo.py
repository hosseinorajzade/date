# Track the (AI-garbled) panel logo in 01_intro with LK optical flow on panel features,
# fitting a similarity transform per frame relative to frame 0. Writes work/intro_logo_track.json.
import cv2, numpy as np, json, subprocess, sys
B='/home/user/date/daewoo_teaser'
W,H=1080,1920; N=int(sys.argv[1]) if len(sys.argv)>1 else 190
p=subprocess.Popen(['ffmpeg','-v','error','-i',f'{B}/prep/01_intro.mp4','-frames:v',str(N),'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
frames=[]
for i in range(N):
    buf=p.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    frames.append(np.frombuffer(buf,np.uint8).reshape(H,W,3))
logo0=np.array([[286,420],[360,420],[360,433],[286,433]],np.float32)
# feature region: the panel around the logo (left half of the control panel)
def feats(g, quad):
    m=np.zeros_like(g); c=quad.mean(0); w=(quad[:,0].max()-quad[:,0].min())
    x0,x1=int(c[0]-1.6*w),int(c[0]+2.6*w); y0,y1=int(c[1]-1.4*w),int(c[1]+2.6*w)
    m[max(0,y0):y1,max(0,x0):x1]=255
    return cv2.goodFeaturesToTrack(g,400,0.005,5,mask=m,blockSize=5)
gray=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in frames]
track=[logo0.tolist()]
quad=logo0.copy(); prev=gray[0]; pts=feats(prev,quad)
for i in range(1,len(frames)):
    nxt,st,err=cv2.calcOpticalFlowPyrLK(prev,gray[i],pts,None,winSize=(31,31),maxLevel=4)
    good0=pts[st[:,0]==1]; good1=nxt[st[:,0]==1]
    M,inl=cv2.estimateAffinePartial2D(good0,good1,method=cv2.RANSAC,ransacReprojThreshold=1.5)
    quad=cv2.transform(quad[None],M)[0]
    track.append(quad.tolist())
    prev=gray[i]; pts=feats(prev,quad)
json.dump(track,open(f'{B}/work/intro_logo_track.json','w'))
# debug overlay
for i in [0,45,90,135,175]:
    if i>=len(frames): continue
    f=frames[i].copy(); q=np.array(track[i]).astype(np.int32)
    cv2.polylines(f,[q],True,(0,255,0),1)
    c=q.mean(0).astype(int); x0,y0=max(0,c[0]-200),max(0,c[1]-120)
    cv2.imwrite(f'{B}/work/trk_{i:03d}.png',cv2.resize(f[y0:y0+240,x0:x0+400],None,fx=2,fy=2,interpolation=cv2.INTER_NEAREST))
print(len(track), track[0], track[-1])
