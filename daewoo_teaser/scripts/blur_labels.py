# Soften the AI-generated fake words on the control panel (03_panel) so they read as shallow depth of field.
# Rects are measured on a reference frame and carried to every frame with an LK similarity track of the panel.
import cv2, numpy as np, subprocess, sys, json
W,H=1080,1920
def read(path):
    raw=subprocess.run(['ffmpeg','-v','error','-i',path,'-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    return [np.frombuffer(raw[i:i+W*H*3],np.uint8).reshape(H,W,3).copy() for i in range(0,len(raw),W*H*3)]
def chain(frames):
    g=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in frames]
    mask=np.zeros((H,W),np.uint8); mask[560:1100]=255
    C=[np.eye(3)]
    for i in range(1,len(g)):
        p=cv2.goodFeaturesToTrack(g[i-1],600,0.004,6,mask=mask,blockSize=5)
        q,st,_=cv2.calcOpticalFlowPyrLK(g[i-1],g[i],p,None,winSize=(31,31),maxLevel=4)
        M,_=cv2.estimateAffinePartial2D(p[st[:,0]==1],q[st[:,0]==1],method=cv2.RANSAC,ransacReprojThreshold=1.5)
        C.append(np.vstack([M,[0,0,1]])@C[-1])
    return C
def apply(src,dst,rects):
    fr=read(src); C=chain(fr)
    log={}
    for n,f in enumerate(fr):
        acc=np.zeros((H,W),np.float32)
        for (ref,x0,y0,x1,y1) in rects:
            T=C[n]@np.linalg.inv(C[ref])
            pts=np.array([[x0,y0,1],[x1,y0,1],[x1,y1,1],[x0,y1,1]],np.float32)@T.T
            poly=pts[:,:2].astype(np.int32)
            if poly[:,0].max()<0 or poly[:,0].min()>W: continue
            m=np.zeros((H,W),np.uint8); cv2.fillPoly(m,[poly],255); acc=np.maximum(acc,m.astype(np.float32)/255)
            log.setdefault(n,[]).append(poly.tolist())
        if acc.max()==0: continue
        acc=cv2.GaussianBlur(acc,(0,0),9)
        bl=cv2.GaussianBlur(f,(0,0),7.5)
        f[:]=np.clip(f*(1-acc[...,None])+bl*acc[...,None],0,255).astype(np.uint8)
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',dst],stdin=subprocess.PIPE)
    for f in fr: p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    return log
B='/home/user/date/daewoo_teaser'
l3=apply(f'{B}/work/s3_raw.mp4',f'{B}/remotion/public/clips/s3.mp4',[(119,685,580,835,1068)])
l4=apply(f'{B}/work/s4_raw.mp4',f'{B}/remotion/public/clips/s4.mp4',[(0,510,580,655,1068),(40,445,580,595,1055),(80,700,982,825,1038)])
print('s3 blurred frames',min(l3),'-',max(l3),' s4 blurred frames',min(l4),'-',max(l4))
