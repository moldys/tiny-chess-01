"""Readable source of the tiny-chess-01 engine (the packed main.py is generated from this).
Run: makefun compress src/main_golf.py --out main.py

Design notes (v2):
- Mailbox board: s.b[64]; pieces signed (white +, black -); s.t turn; s.c castle bits.
- Move generator emits pseudo-legal moves; legality is filtered in the search by
  making the move and checking the mover is not left in check (s.ck).
- Negamax with alpha-beta, iterative deepening (Engine.b), node budget via s.n
  vs s.bu, and a check extension that deepens when the side to move is in check.
- Evaluation is material-only (V) to stay inside the 4096-byte cap; no tablebase.
- En passant capture is handled via the s.e square; castle rights via s.c bits.
"""
import os,time,json,urllib.request as U
V=(0,100,320,330,500,900,20000);N=(-17,-15,-10,-6,6,10,15,17)
class B:
 def __init__(s,f=None):
  s.b=[0]*64;s.t=1;s.c=0;s.e=-1;s.st=[]
  s.sf(f if f else "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
 def sf(s,f):
  b=s.b;b[:]=[0]*64;p=f.split();r=p[0].split('/')
  I={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6}
  for y,row in enumerate(r):
   x=0
   for c in row:
    if c.isdigit():x+=int(c)
    else:b[(7-y)*8+x]=I.get(c,-I.get(c.upper(),0));x+=1
  s.t=1 if p[1]=='w' else -1
  s.c=('K'in p[2])|(('Q'in p[2])<<1)|(('k'in p[2])<<2)|(('q'in p[2])<<3)
  s.e=-1
  if p[3]!='-':s.e=(ord(p[3][0])-97)+(int(p[3][1])-1)*8
 def a(s,q,by):
  b=s.b
  for d in(-9,-8,-7,-1,1,7,8,9):
   p=q+d
   if 0<=p<64 and abs(p%8-q%8)<=1 and b[p]==6*by:return 1
  for d in(7,9):
   p=q-d*by
   if 0<=p<64 and abs(p%8-q%8)==1 and b[p]==by:return 1
  for d in N:
   p=q+d
   if 0<=p<64 and abs(p%8-q%8) in(1,2)and b[p]==2*by:return 1
  for dr,df in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
   rr=q//8+dr;ff=q%8+df
   while 0<=rr<8 and 0<=ff<8:
    p=rr*8+ff;v=b[p]
    if v:
     u=abs(v)
     if u==5 or(u==4 and dr*df==0)or(u==3 and abs(dr)==abs(df)):
      if v*by>0:return 1
     break
    rr+=dr;ff+=df
  return 0
 def ck(s,side=None):
  if side is None:side=s.t
  return s.a(s.b.index(6*side),-side)
 def g(s):
  b=s.b;me=s.t;o=[]
  for i in range(64):
   v=b[i]
   if v*me<=0:continue
   p=abs(v)
   if p==1:
    r=i//8;j=i+8*me
    if r==1 and me==1 and b[i+8]==0 and b[i+16]==0:o.append((i,i+16,0))
    if r==6 and me==-1 and b[i-8]==0 and b[i-16]==0:o.append((i,i-16,0))
    if 0<=j<64 and b[j]==0:o.append((i,j,5 if(me==1 and j//8==7)or(me==-1 and j//8==0) else 0))
    for d in(7,9):
     j=i+d*me
     if 0<=j<64 and abs(j%8-i%8)==1 and(j==s.e or(b[j]*me<0 and abs(b[j])!=6)):o.append((i,j,5 if(me==1 and j//8==7)or(me==-1 and j//8==0) else 0))
   elif p==2:
    for d in N:
     j=i+d
     if 0<=j<64 and abs(j%8-i%8) in(1,2)and(b[j]==0 or(b[j]*me<0 and abs(b[j])!=6)):o.append((i,j,0))
   elif p==6:
    if i==4 and me==1:
     if s.c&1 and not b[5] and not b[6] and b[7]==4 and not(s.a(4,-1)or s.a(5,-1)or s.a(6,-1)):o.append((4,6,0))
     if s.c&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not(s.a(4,-1)or s.a(3,-1)or s.a(2,-1)):o.append((4,2,0))
    if i==60 and me==-1:
     if s.c&4 and not b[61] and not b[62] and b[63]==-4 and not(s.a(60,1)or s.a(61,1)or s.a(62,1)):o.append((60,62,0))
     if s.c&8 and not b[59] and not b[58] and not b[57] and b[56]==-4 and not(s.a(60,1)or s.a(59,1)or s.a(58,1)):o.append((60,58,0))
    for d in(-9,-8,-7,-1,1,7,8,9):
     j=i+d
     if 0<=j<64 and abs(j%8-i%8)<=1 and(b[j]==0 or(b[j]*me<0 and abs(b[j])!=6)):o.append((i,j,0))
   else:
    for dr,df in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
     if (p==3 and abs(dr)!=abs(df))or(p==4 and dr*df!=0):continue
     rr=i//8+dr;ff=i%8+df
     while 0<=rr<8 and 0<=ff<8:
      j=rr*8+ff;q=b[j]
      if not q:o.append((i,j,0))
      else:
       if q*me<0 and abs(q)!=6:o.append((i,j,0))
       break
      rr+=dr;ff+=df
  return o
 def m(s,x):
  f,t,pr=x;b=s.b;cap=b[t];mv=b[f];oc=s.c;oe=s.e;ev=-1
  b[t]=b[f];b[f]=0
  if pr:b[t]=pr*s.t
  if not cap and mv==1 and t==s.e:cap=-99;ev=s.e-8*s.t;b[ev]=0
  cg=0
  if mv==6*s.t:
   if f==4 and t==6:b[5],b[7]=b[7],0;cg=1
   elif f==4 and t==2:b[3],b[0]=b[0],0;cg=1
   elif f==60 and t==62:b[61],b[63]=b[63],0;cg=1
   elif f==60 and t==58:b[59],b[56]=b[56],0;cg=1
  if mv==6*s.t:
   s.c&=~(3 if s.t==1 else 12)
  else:
   if f==7 or t==7:s.c&=~1
   if f==0 or t==0:s.c&=~2
   if f==63 or t==63:s.c&=~4
   if f==56 or t==56:s.c&=~8
  s.e=-1
  if mv==1 and f//8==1 and t//8==3:s.e=f+8
  elif mv==-1 and f//8==6 and t//8==4:s.e=f-8
  s.st.append((f,t,pr,cap,oc,oe,mv,cg,ev));s.t=-s.t
 def u(s):
  f,t,pr,cap,oc,oe,mv,cg,ev=s.st.pop();b=s.b
  s.t=-s.t;b[f]=mv;b[t]=0
  if cap==-99:b[ev]=-s.t
  elif cap:b[t]=cap
  if cg:
   if f==4 and t==6:b[7],b[5]=b[5],0
   elif f==4 and t==2:b[0],b[3]=b[3],0
   elif f==60 and t==62:b[63],b[61]=b[61],0
   elif f==60 and t==58:b[56],b[59]=b[59],0
  s.c=oc;s.e=oe
PT=[0]*8+[50]*8+[10,10,20,30,30,20,10,10]+[5,5,10,25,25,10,5,5]+[0]*8+[5,-5,-10,0,0,-10,-5,5]+[5,10,10,-20,-20,10,10,5]+[0]*8
PN=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
PB=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
PR=[0,0,0,5,5,0,0,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0]
PQ=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,5,0,0,0,0,-10,-10,5,5,5,5,5,0,-10,0,0,5,5,5,5,0,-5,-5,0,5,5,5,5,0,-5,-10,0,5,5,5,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
PK=[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]
def x(s):
 z=0;Ba=0;Bb=0
 for i in range(64):
  v=s.b[i]
  if not v:continue
  p=abs(v);q=i if v>0 else i^56
  if p==1:w=V[1]+PT[q]
  elif p==2:w=V[2]+PN[q]
  elif p==3:
   w=V[3]+PB[q]
   if v>0:Ba+=1
   else:Bb+=1
  elif p==4:
   w=V[4]+PR[q]
   f=i%8
   if all(abs(s.b[f+k*8])!=1 for k in range(8)):w+=15 if v>0 else -15
  elif p==5:w=V[5]+PQ[q]
  else:w=V[6]+PK[q]
  z+=w if v>0 else -w
  if p in(2,3,4,5):
   en=-1 if v>0 else 1
   for dd in(7,9):
    j=i+dd*en
    if 0<=j<64 and abs(j%8-i%8)==1 and s.b[j]==en:
     z-=V[p]//2 if v>0 else -V[p]//2
     break
 z+=30 if Ba>1 else 0
 z-=30 if Bb>1 else 0
 return z*s.t if s.t>0 else -z
def q(s,b):
 z=x(b)
 m=[]
 for f,t,pr in b.g():
  if b.b[t] or pr:
   if b.b[t] and not pr and z-V[abs(b.b[t])]>200:continue
   m.append((f,t,pr))
 m.sort(key=lambda x:-V[abs(b.b[x[1]])]);m=m[:8]
 for f,t,pr in m:
  if time.time()-s.t0>s.tl:return z
  b.m((f,t,pr))
  if b.ck(-b.t):b.u();continue
  w=-q1(s,b)
  if w>z:z=w
  b.u()
 return z
def q1(s,b):
 z=x(b)
 C=[]
 for f,t,pr in b.g():
  if not b.b[t] and not pr:continue
  if b.b[t] and not pr and z-V[abs(b.b[t])]>200:continue
  C.append((f,t,pr))
 C.sort(key=lambda x:-V[abs(b.b[x[1]])]);C=C[:8]
 for f,t,pr in C:
  if time.time()-s.t0>s.tl:return z
  b.m((f,t,pr))
  if b.ck(-b.t):b.u();continue
  w=-x(b)
  if w>z:z=w
  b.u()
 return z
class E:
 def __init__(s,bu=50000,dp=5,tl=7):s.bu=bu;s.d=dp;s.n=0;s.k=[0]*12;s.tl=tl;s.h=[[0]*64 for _ in range(64)];s.pv=[0]*12
 def o(s,b,mv,d):
  L=[]
  for f,t,pr in mv:
   sc=0;vic=b.b[t]
   if vic:sc=10*V[abs(vic)]-V[abs(b.b[f])]
   elif pr:sc=900+V[pr]
   elif b.b[f]==1 and t==b.e:sc=100
   elif (f,t,pr)==s.k[d] or (f,t,pr)==s.k[d+1]:sc-=60
   elif (f,t,pr)==s.pv[d]:sc-=80
   sc-=s.h[f][t]//16
   L.append((-sc,(f,t,pr)))
  L.sort();return[m for _,m in L]
 def s(s,b,d,a,be):
  s.n+=1
  if s.n>s.bu or time.time()-s.t0>s.tl:return x(b)
  if b.ck():d+=1
  mv=b.g()
  if not mv:return -30000+(s.d-d) if b.ck() else 0
  if d<=0:return q(s,b)
  if d>=3 and not b.ck() and a>-9900:
   b.t=-b.t
   z=-s.s(b,d-3,-be,-be+1)
   b.t=-b.t
   if z>=be:return be
  for i,m in enumerate(s.o(b,mv,d)):
   tmp=b.b[m[1]]
   b.m(m)
   if b.ck(-b.t):b.u();continue
   if d>=3 and i>=4 and not tmp and not m[2] and a>-9900:
    z=-s.s(b,d-2,-be,-a)
    if z>a:z=-s.s(b,d-1,-be,-a)
   else:z=-s.s(b,d-1,-be,-a)
   b.u()
   if z>=be:
    s.h[m[0]][m[1]]+=d*d
    return be
   if z>a:
    a=z;s.pv[d]=m
    if not tmp and not m[2] and m!=s.k[d]:
     s.k[d+1]=s.k[d];s.k[d]=m
  return a
 def b(s,b,legal=None):
  s.t0=time.time()
  mv=b.g()
  if legal is not None:
   L=set(legal);mv=[m for m in mv if s.q(m) in L]
  if not mv:return None
  bm=None;fl=0
  for d in range(1,s.d+1):
   s.n=0;a=-1e9;be=1e9;cur=None;cs=-1e9;ok=1
   for m in s.o(b,mv,0):
    b.m(m)
    if b.ck(-b.t):b.u();continue
    fl=1;z=-s.s(b,d-1,-be,-a);b.u()
    if z>cs:cs=z;cur=m
    if cs>a:a=cs
    if time.time()-s.t0>s.tl:ok=0;break
   if ok and cur is not None:bm=cur
   if s.n>s.bu or time.time()-s.t0>s.tl:break
  return None if not fl else bm
 def q(s,m):
  f,t,pr=m
  return chr(97+f%8)+str(f//8+1)+chr(97+t%8)+str(t//8+1)+('q' if pr else '')
def run(url,e):
 H={'content-type':'application/json'}
 while 1:
  g=json.load(U.urlopen(U.Request(url+'/game',data=json.dumps({}).encode(),headers=H)))
  if g['status']=='done':break
  while g['status']=='your_move':
   b=B(g['fen']);legal=g['legal_moves'];mv=e.b(b,legal)
   if mv is None:
    u=legal[0];mv=(ord(u[0])-97+(int(u[1])-1)*8,ord(u[2])-97+(int(u[3])-1)*8,len(u)>4)
   g=json.load(U.urlopen(U.Request(url+'/move',data=json.dumps({'game':g['game'],'move':e.q(mv)}).encode(),headers=H)))
  if g['status']=='done':break
if __name__=='__main__':
 e=E(int(os.environ.get('ENGINE_BUDGET','30000')),int(os.environ.get('ENGINE_DEPTH','5')))
 run(os.environ['MAKEFUN_ENV_URL'],e)
