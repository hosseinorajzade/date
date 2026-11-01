# Machine silhouette for 01_intro frames 80-185 (S2 "Charisma behind the machine").
# Left corners follow the panel's optical-flow track; right-side corners use the same track plus an
# offset interpolated from hand-measured keyframes (perspective makes the similarity fit drift on the far side).
import json, numpy as np, cv2
B='/home/user/date/daewoo_teaser'; H=1920
tr=np.array(json.load(open(f'{B}/work/intro_logo_track.json')),np.float32)
KF={90:{'L':164,'A':(167,553),'B':(237,457),'C':(910,483),'R':918},
    120:{'L':182,'A':(182,553),'B':(220,457),'C':(878,480),'R':887},
    150:{'L':172,'A':(172,417),'B':(178,410),'C':(897,430),'R':905},
    180:{'L':113,'A':(117,345),'B':(117,337),'C':(953,347),'R':962}}
ks=sorted(KF)
def M(a,b): return cv2.estimateAffinePartial2D(tr[a],tr[b])[0]
def mp(p,m): return cv2.transform(np.array(p,np.float32)[None,None],m)[0,0]
# per-keyframe residuals of the tracked prediction from frame 90
res={k:{} for k in ks}
for k in ks:
    m=M(90,k)
    for c in 'ABC': res[k][c]=np.array(KF[k][c],np.float32)-mp(KF[90][c],m)
    res[k]['L']=KF[k]['L']-mp((KF[90]['L'],600),m)[0]
    res[k]['R']=KF[k]['R']-mp((KF[90]['R'],600),m)[0]
def interp(n,c):
    n=min(max(n,ks[0]),ks[-1]); 
    for a,b in zip(ks,ks[1:]):
        if a<=n<=b:
            t=(n-a)/(b-a); return res[a][c]*(1-t)+res[b][c]*t
polys={}
for n in range(80,186):
    m=M(90,min(n,189))
    A=mp(KF[90]['A'],m)+interp(n,'A'); Bp=mp(KF[90]['B'],m)+interp(n,'B'); C=mp(KF[90]['C'],m)+interp(n,'C')
    L=mp((KF[90]['L'],600),m)[0]+interp(n,'L'); R=mp((KF[90]['R'],600),m)[0]+interp(n,'R')
    polys[n]=[[round(float(L),1),H],[round(float(A[0]),1),round(float(A[1]),1)],[round(float(Bp[0]),1),round(float(Bp[1]),1)],
              [round(float(C[0]),1),round(float(C[1]),1)],[round(float(R),1),H]]
json.dump(polys,open(f'{B}/remotion/src/machinePolys.json','w'))
import subprocess
for n in (95,135,165):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f'{B}/work/01_intro_fixed.mp4','-vf',f'select=eq(n\\,{n})','-vsync','0','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    f=np.frombuffer(raw,np.uint8).reshape(1920,1080,3).copy(); f=cv2.convertScaleAbs(f,alpha=1.0,beta=40)
    cv2.polylines(f,[np.array(polys[n],np.int32)],True,(0,255,0),3); cv2.imwrite(f'{B}/work/mask_{n}.png',cv2.resize(f[150:1150],None,fx=0.45,fy=0.45))
print('ok')
