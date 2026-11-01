import subprocess
from PIL import Image, ImageDraw, ImageFont
B='/home/user/date/daewoo_teaser'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',17)
FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
shots=[
 ('S1 0-3s','01_intro',1.0,'flash + RGB glitch, push-in'),
 ('S2 3-6s','01_intro',4.2,'"Charisma" behind machine'),
 ('S3 6-10s','03_panel',0.4,'logo, neon trace, slow-mo'),
 ('S4 10-14s','03_panel',4.4,'7 Mode, labels blurred'),
 ('S5 14-17s','04_dial',6.0,'dial red ring, no text'),
 ('S6 17-22s','05_door',2.0,'door opens - A+++'),
 ('S7 22-26s','05_door',6.6,'into drum - Jet Shower*'),
 ('S8 26-29s','08_fabric',4.5,'fabric swirl - Add Item'),
 ('S9 29-33s','07_towels',6.5,'towels - 9Kg'),
 ('S10 33-38s','09_drum',5.0,'drum - "Charisma 9Kg" typed'),
 ('S11 38-43s',None,0,'logo reveal + www.Daewoo.ir'),
]
W,H=240,427
sb=Image.new('RGB',(len(shots)*(W+6)+6, H+80),(14,14,14)); d=ImageDraw.Draw(sb)
for i,(lab,clip,t,desc) in enumerate(shots):
    x=6+i*(W+6)
    if clip:
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{B}/prep/{clip}.mp4','-frames:v','1','-vf',f'scale={W}:{H}',f'{B}/work/sb.png'],check=True)
        im=Image.open(f'{B}/work/sb.png').convert('RGB')
    else:
        im=Image.new('RGB',(W,H),(0,0,0)); lg=Image.open(f'{B}/assets/daewoo_logo.png'); lg=lg.resize((200,int(200*lg.size[1]/lg.size[0])),Image.LANCZOS)
        im.paste(lg,(20,190),lg); ImageDraw.Draw(im).text((62,240),'www.Daewoo.ir',font=FS,fill=(200,200,200))
    sb.paste(im,(x,6))
    d.text((x+2,H+12),lab,font=F,fill=(255,230,0)); d.text((x+2,H+38),desc[:31],font=FS,fill=(230,230,230))
sb.save(f'{B}/review/storyboard.png'); print(sb.size)
