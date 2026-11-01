# Replace the AI-garbled "DACIVOO" panel logo in 01_intro with the real Daewoo wordmark.
# 1) start from the optical-flow track, 2) refine each frame to the bright text pixels,
# 3) smooth over time, 4) inpaint the old text, 5) draw the real wordmark (matched brightness/softness).
import cv2, numpy as np, json, subprocess
from PIL import Image
B='/home/user/date/daewoo_teaser'; W,H=1080,1920; N=190
track=np.array(json.load(open(f'{B}/work/intro_logo_track.json')),np.float32)
wm=np.asarray(Image.open(f'{B}/assets/logo_wordmark.png').convert('RGBA')).astype(np.float32)/255
a=wm[...,3]; ys,xs=np.where(a>0.1); wm=wm[ys.min():ys.max()+1, xs.min():xs.max()+1]
WM_ASPECT=wm.shape[1]/wm.shape[0]
print('wordmark aspect',WM_ASPECT)
rd=subprocess.Popen(['ffmpeg','-v','error','-i',f'{B}/prep/01_intro.mp4','-frames:v',str(N),'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
frames=[np.frombuffer(rd.stdout.read(W*H*3),np.uint8).reshape(H,W,3).copy() for _ in range(N)]
# --- refine
boxes=[]; angs=[]
for i,f in enumerate(frames):
    q=track[i]; x0,x1=q[:,0].min()-8,q[:,0].max()+8; y0,y1=q[:,1].min()-8,q[:,1].max()+8
    x0,y0,x1,y1=[int(round(v)) for v in (x0,y0,x1,y1)]
    g=cv2.cvtColor(f[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
    thr=max(55,0.5*np.percentile(g,99.5)); m=g>thr
    yy,xx=np.where(m)
    if len(xx)<20: boxes.append(boxes[-1]); angs.append(angs[-1]); continue
    boxes.append([x0+np.percentile(xx,0.5),y0+np.percentile(yy,1),x0+np.percentile(xx,99.5)+1,y0+np.percentile(yy,99)+1])
    v=q[1]-q[0]; angs.append(np.degrees(np.arctan2(v[1],v[0])))
boxes=np.array(boxes); angs=np.array(angs)
def smooth(x,k=9):
    pad=np.pad(x,((k//2,k//2),)+((0,0),)*(x.ndim-1),mode='edge'); ker=np.ones(k)/k
    return np.stack([np.convolve(pad[:,j],ker,'valid') for j in range(x.shape[1])],1) if x.ndim>1 else np.convolve(pad,ker,'valid')
boxes=smooth(boxes); angs=smooth(angs)
json.dump({'boxes':boxes.tolist(),'angles':angs.tolist()},open(f'{B}/work/intro_logo_boxes.json','w'))
# --- patch
wr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','30','-i','-',
    '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',f'{B}/work/01_intro_fixed.mp4'],stdin=subprocess.PIPE)
for i,f in enumerate(frames):
    x0,y0,x1,y1=boxes[i]; cx,cy=(x0+x1)/2,(y0+y1)/2; bw=x1-x0; bh=y1-y0
    # erase: bright text pixels in a padded box, dilated, then inpaint
    pad=6; X0,Y0,X1,Y1=int(x0-pad),int(y0-pad),int(x1+pad),int(y1+pad)
    roi=f[Y0:Y1,X0:X1]; g=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg=np.percentile(g,40); m=((g>bg+14)*255).astype(np.uint8)
    m=cv2.dilate(m,np.ones((3,3),np.uint8),iterations=2)
    bright=roi[g>np.percentile(g,97)].mean(0) if (g>np.percentile(g,97)).sum()>3 else np.array([200,200,200])
    f[Y0:Y1,X0:X1]=cv2.inpaint(roi,m,4,cv2.INPAINT_TELEA)
    # draw: wordmark width = 0.98 * old logo width; height from real aspect
    tw=bw*0.98; th=tw/WM_ASPECT
    S=4  # supersample
    big=cv2.resize(wm,(max(2,int(round(tw*S))),max(2,int(round(th*S)))),interpolation=cv2.INTER_AREA)
    M=cv2.getRotationMatrix2D((big.shape[1]/2,big.shape[0]/2),-angs[i],1.0)
    M[0,2]+=cx*S-big.shape[1]/2; M[1,2]+=cy*S-big.shape[0]/2
    # render into a local supersampled canvas
    lx0,ly0=int(cx-tw),int(cy-th*2); lw,lh=int(tw*2),int(th*4)
    M2=M.copy(); M2[0,2]-=lx0*S; M2[1,2]-=ly0*S
    lay=cv2.warpAffine(big,M2,(lw*S,lh*S),flags=cv2.INTER_LINEAR,borderValue=(0,0,0,0))
    lay=cv2.resize(lay,(lw,lh),interpolation=cv2.INTER_AREA)
    alpha=cv2.GaussianBlur(lay[...,3],(0,0),0.55)
    col=lay[...,:3][...,::-1]  # RGB->BGR; wordmark is white so tint to sampled panel-print colour
    tint=np.clip(bright,120,235)/255.0
    region=f[ly0:ly0+lh,lx0:lx0+lw].astype(np.float32)/255
    out=region*(1-alpha[...,None])+(col*tint)*alpha[...,None]
    f[ly0:ly0+lh,lx0:lx0+lw]=np.clip(out*255,0,255).astype(np.uint8)
    wr.stdin.write(f.tobytes())
    if i in (0,60,120,175):
        c=f[int(cy-60):int(cy+60),int(cx-130):int(cx+130)]
        cv2.imwrite(f'{B}/work/patch_{i:03d}.png',cv2.resize(c,None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC))
wr.stdin.close(); wr.wait(); print('done')
