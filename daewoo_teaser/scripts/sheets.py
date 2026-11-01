import os, sys
from PIL import Image, ImageDraw, ImageFont
B='/home/user/date/daewoo_teaser'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
# problem ranges (seconds, end exclusive)
BAD={
 '01_intro':[(0,8.5,'BROKEN LOGO "DACIVOO" -> patch')],
 '03_panel':[(1.0,4.5,'FAKE PANEL WORDS -> blur'),(4.5,6.0,'small "Connel" label')],
 '04_dial':[(0,4.5,'FAKE LABELS "Dryst/Synt"')],
 '08_fabric':[(2.0,3.5,'GRID TEXTURE GLITCH')],
 '09_drum':[(0,2.5,'BROKEN LOGO "OAeWOO"')],
}
USE={
 '01_intro':[(0,3,'S1'),(3,6,'S2')],
 '03_panel':[(0,1.6,'S3 slow-mo'),(2,6,'S4')],
 '04_dial':[(4.5,7.5,'S5')],
 '05_door':[(0,4.5,'S6'),(4.6,8,'S7')],
 '08_fabric':[(3.5,6.5,'S8')],
 '07_towels':[(4,8,'S9')],
 '09_drum':[(2.6,7.6,'S10')],
}
W,H=216,384; COLS=8; PAD=6; TOP=40
for n in sorted(os.listdir(f'{B}/work/frames')):
    fr=sorted(os.listdir(f'{B}/work/frames/{n}'))
    rows=(len(fr)+COLS-1)//COLS
    sheet=Image.new('RGB',(COLS*(W+PAD)+PAD, TOP+rows*(H+PAD+40)+PAD),(14,14,14))
    d=ImageDraw.Draw(sheet)
    d.text((PAD,8),f'{n}  (graded, 1080x1920 30fps)  - one frame / 0.5s',font=FT,fill=(255,255,255))
    for i,f in enumerate(fr):
        t=i*0.5
        x=PAD+(i%COLS)*(W+PAD); y=TOP+(i//COLS)*(H+PAD+40)
        im=Image.open(f'{B}/work/frames/{n}/{f}'); sheet.paste(im,(x,y))
        d.rectangle([x,y,x+64,y+20],fill=(0,0,0)); d.text((x+4,y+2),f'{t:.1f}s',font=F,fill=(255,230,0))
        bad=[lab for a,b,lab in BAD.get(n,[]) if a<=t<b]
        use=[lab for a,b,lab in USE.get(n,[]) if a<=t+0.001<b]
        if bad:
            for k in range(4): d.rectangle([x+k,y+k,x+W-1-k,y+H-1-k],outline=(235,20,40))
            d.rectangle([x,y+H-22,x+W,y+H],fill=(200,0,25)); d.text((x+4,y+H-19),bad[0][:28],font=FS,fill=(255,255,255))
        if use:
            d.rectangle([x,y+H+4,x+W,y+H+30],fill=(20,150,70)); d.text((x+6,y+H+8),'USE '+use[0],font=F,fill=(255,255,255))
        else:
            d.rectangle([x,y+H+4,x+W,y+H+30],fill=(50,50,50)); d.text((x+6,y+H+8),'unused',font=F,fill=(150,150,150))
    sheet.save(f'{B}/review/contact_{n}.png')
    print(n, sheet.size)
