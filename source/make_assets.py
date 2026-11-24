import sys, json, base64, io
from PIL import Image, ImageFilter
import numpy as np
im=Image.open(sys.argv[1]).convert('RGB'); a=np.array(im).astype(np.int16)
H,W=a.shape[:2]
R,G,B=a[...,0],a[...,1],a[...,2]
grass=(G>185)&(R<150)&(B<90)&(G-R>70)
yy,xx=np.mgrid[0:H,0:W]
sky=(B>215)&(G>140)&(R<140)&(yy<100)
cloud=(R>235)&(G>235)&(B>235)&(yy<100)
road=np.zeros((H,W),bool)
for y0,y1,x0,x1 in [(250,322,10,1014),(888,966,10,1014),(1139,1217,10,1014),(1436,1501,274,853)]: road[y0:y1,x0:x1]=True
for x0,x1,y0,y1 in [(274,347,95,1501),(778,851,95,1501),(509,589,320,430),(601,653,1215,1440)]:road[y0:y1,x0:x1]=True
d=np.hypot(xx-550,yy-596); road|=(d<174)&(d>108)
for x0,y0,x1,y1 in [(340,545,400,652),(700,555,782,652)]: road[y0:y1,x0:x1]=True
island=(d<108)
roadish=road&((np.abs(R-G)<14)&(np.abs(G-B)<14)&(R>70))  # gray or white marking
RECTS={
 'windmill':(35,68,272,246),'bank':(412,118,610,246),'yellowshop':(678,92,778,246),'farm':(832,28,1012,246),
 'market':(78,332,234,420),'tower':(350,312,432,472),'office':(622,328,782,478),'glass':(865,372,1012,496),
 'apts':(62,538,252,716),'hospital':(865,512,1013,688),'yellowbig':(356,672,548,872),'garage':(566,732,748,852),
 'shopleft':(90,736,222,852),'hotdog':(852,686,1013,852),'police':(48,932,234,1062),'school':(356,928,598,1128),
 'house':(616,1016,762,1118),'fire':(860,962,1013,1108),'redbldg':(56,1232,248,1422),'clothes':(356,1212,534,1412),
 'cafe':(646,1222,792,1334),'brcorner':(858,1222,1003,1484)}
ga=a.copy()
out={'sprites':[]}
for k,(x0,y0,x1,y1) in RECTS.items():
  s=np.s_[y0:y1,x0:x1]
  m=~(grass[s]|sky[s]|cloud[s]|roadish[s]|island[s])
  alpha=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))
  rgba=Image.fromarray(a[s].astype(np.uint8)).convert('RGBA'); rgba.putalpha(alpha)
  bio=io.BytesIO(); rgba.save(bio,'PNG',optimize=True); rgba.save(f'spr_{k}.png')
  out['sprites'].append({'n':k,'r':[x0,y0,x1,y1],'d':'data:image/png;base64,'+base64.b64encode(bio.getvalue()).decode()})
  sub=ga[s]; rs=road[s]; top=(yy[s]<100)|island[s]
  sub[(~rs)&(~top)]=(104,222,20)
  sub[rs&(~roadish[s])&(~top)]=(140,140,140)
Image.fromarray(ga.astype(np.uint8)).save('ground.jpg',quality=88)
bio=io.BytesIO(); Image.fromarray(ga.astype(np.uint8)).save(bio,'JPEG',quality=88)
out['ground']='data:image/jpeg;base64,'+base64.b64encode(bio.getvalue()).decode()
json.dump(out,open('assets.json','w'))
print(len(json.dumps(out))/1e6,'MB')
