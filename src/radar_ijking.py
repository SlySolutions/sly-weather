import json, math, sys
from PIL import Image
im=Image.open('radar_bg.png').convert('RGB'); W,H=im.size; px=im.load()
def isnl(p): return (abs(p[0]-0)<25 and abs(p[1]-122)<25 and abs(p[2]-0)<25) or (p[0]>150 and p[1]>150 and p[2]<80)  # NL green or yellow border lines
mask=[[1 if isnl(px[x,y]) else 0 for x in range(W)] for y in range(H)]
prov=json.load(open('mapdata/provincie_2024.geojson'))
rings=[]
for f in prov['features']:
    g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    for p in polys: rings.append(p[0])
def merc(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def lin(lat): return lat
def raster(west,east,north,south,fy,want=False):
    yn,ys=fy(north),fy(south)
    edges=[]
    for r in rings:
        pts=[((lon-west)/(east-west)*W,(yn-fy(lat))/(yn-ys)*H) for lon,lat in r]
        for i in range(len(pts)-1):
            (x1,y1),(x2,y2)=pts[i],pts[i+1]
            if y1!=y2: edges.append((min(y1,y2),max(y1,y2),x1,y1,x2,y2))
    inter=0;uni=0; out=Image.new('RGB',(W,H)) if want else None
    for y in range(H):
        yc=y+0.5; xs=[]
        for (ymin,ymax,x1,y1,x2,y2) in edges:
            if ymin<=yc<ymax: xs.append(x1+(yc-y1)*(x2-x1)/(y2-y1))
        xs.sort(); row=mask[y]; filled=[0]*W
        for i in range(0,len(xs)-1,2):
            a=max(0,int(xs[i]+0.5)); b=min(W,int(xs[i+1]+0.5))
            for x in range(a,b): filled[x]=1
        for x in range(W):
            f=filled[x]; m=row[x]
            if f and m: inter+=1
            if f or m: uni+=1
            if want: out.putpixel((x,y),(255*f,255*m,0))
    if want: out.save('calib_overlay.png')
    return inter/uni if uni else 0
for name,fy in (('mercator',merc),('linear',lin)):
    p=[0,10,54.75,49.4]; s=raster(*p,fy)
    for step in (0.5,0.25,0.1,0.05,0.02,0.01):
        for _ in range(12):
            improved=False
            for i in range(4):
                for d in (-step,step):
                    q=list(p); q[i]+=d; v=raster(*q,fy)
                    if v>s: s,p=v,q; improved=True
            if not improved: break
    print(name,round(s,4),p,flush=True)
    if name==sys.argv[1] if len(sys.argv)>1 else name=='mercator': raster(*p,fy,True)
