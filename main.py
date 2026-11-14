import json as j,os,urllib.request as u
U=os.environ['MAKEFUN_ENV_URL']
V=(0,100,320,330,500,900,0)
N=(-33,-31,-18,-14,14,18,31,33)
K=(-17,-16,-15,-1,1,15,16,17)
D=(-17,-15,15,17)
R=(-16,-1,1,16)
O=(0,0,N,D,R,D+R,K)
G={4:3,116:12,0:2,7:1,112:8,119:4}
ND=40000
I=99999
def A(B,x,s):
 for O,v in((N,2),(K,6)):
  for o in O:
   y=x+o
   if not y&136 and B[y]==v*s:return 1
 for o in(15,17):
  y=x-o*s
  if not y&136 and B[y]==s:return 1
 for o in D+R:
  y=x+o
  while not y&136:
   p=B[y]
   if p:
    if p==(3 if o in D else 4)*s or p==5*s:return 1
    break
   y+=o
 return 0
def M(P,m):
 B,s,c,e,w,k=P
 f=m&127;t=m>>7&127;q=m>>14
 p=B[f];Z=B[:];Z[f]=0
 if abs(p)==1 and t==e and not Z[t]:Z[t-16*s]=0
 Z[t]=q*s if q else p
 if abs(p)==6 and abs(t-f)==2:
  a=t+1 if t>f else t-2;b=t-1 if t>f else t+1;Z[b]=Z[a];Z[a]=0
 if abs(p)==6:
  if s>0:w=t
  else:k=t
 c2=c
 for z in(f,t):c2&=~G.get(z,0)
 e2=(f+t)//2 if abs(p)==1 and abs(t-f)==32 else -1
 if A(Z,w if s>0 else k,-s):return None
 return Z,-s,c2,e2,w,k
def L(P):
 B,s,c,e,w,k=P
 a=[]
 for i,p in enumerate(B):
  if p*s<=0 or i&136:continue
  v=abs(p)
  if v==1:
   d=16*s;lr=7 if s>0 else 0
   for dd in(d,d-1,d+1):
    t=i+dd
    if t&136:continue
    if dd==d:
     if B[t]:continue
     key=0;dp=1
    elif t==e and not B[t]:key=100;dp=0
    elif B[t]*s<0 and abs(B[t])!=6:key=V[abs(B[t])];dp=0
    else:continue
    if (t>>4)==lr:
     for x in(5,4,3,2):a.append((900,i|t<<7|x<<14))
    else:
     a.append((key,i|t<<7))
     if dp and (i>>4)==(1 if s>0 else 6) and not B[i+2*d]:a.append((0,i|(i+2*d)<<7))
  else:
   for d in O[v]:
    t=i+d
    while not t&136:
     if B[t]:
      if B[t]*s<0 and abs(B[t])!=6:a.append((V[abs(B[t])],i|t<<7))
      break
     a.append((0,i|t<<7))
     if v==2 or v==6:break
     t+=d
 kf=4 if s>0 else 116
 for d,em,ck,bt in((2,(1,2),(0,1,2),1 if s>0 else 4),(-2,(-1,-2,-3),(0,-1,-2),2 if s>0 else 8)):
  if c&bt and all(not B[kf+x] for x in em) and all(not A(B,kf+x,-s) for x in ck):a.append((0,kf|(kf+d)<<7))
 a.sort(reverse=True)
 return[m for _,m in a]
def E(P):
 B,s,c,e,w,k=P
 sc=0;wb=0;bb=0
 for i,p in enumerate(B):
  if not p or i&136:continue
  a=abs(p);r=i>>4;f=i&7
  cv=min(r,7-r,f,7-f)
  if a==1:v=100+8*(r if p>0 else 7-r)
  elif a==4:v=500+(12 if r==1+5*(p>0) else 2*cv)
  else:v=V[a]+(0,0,8,4,0,3,-10)[a]*cv
  if a==3:
   wb+=p>0;bb+=p<0
  sc+=v if p>0 else -v
 sc+=30*((wb>1)-(bb>1))
 return sc*s
nd=0
X=Exception
def n():
 global nd;nd+=1
 if nd>ND:raise X
def Q(P,a,b):
 n()
 st=E(P)
 if st>=b:return b
 if st>a:a=st
 for m in L(P):
  t=m>>7&127
  if P[0][t] or m>>14 or t==P[3]:
   P2=M(P,m)
   if not P2:continue
   sc=-Q(P2,-b,-a)
   if sc>=b:return b
   a=max(a,sc)
 return a
def S(P,d,a,b,pl):
 n()
 B,s,c,e,w,k=P
 ck=A(B,w if s>0 else k,-s)
 d=min(d+ck,8)
 if d<=0:return Q(P,a,b)
 ms=L(P)
 be=-I
 for m in ms:
  P2=M(P,m)
  if not P2:continue
  sc=-S(P2,d-1,-b,-a,pl+1)
  if sc>=b:return b
  be=max(be,sc);a=max(a,sc)
 if be==-I:return -I+pl if ck else 0
 return be
def F(fen):
 B=[0]*128;w=0;k=0
 pa=fen.split()
 for i,r in enumerate(pa[0].split('/')):
  f=0
  for ch in r:
   if ch.isdigit():f+=int(ch)
   else:
    q='PNBRQKpnbrqk'.index(ch);p=q%6+1
    if q>5:p=-p
    x=(7-i)*16+f;B[x]=p
    if p==6:w=x
    elif p==-6:k=x
    f+=1
 s=1 if pa[1]=='w' else -1
 c=sum(b for ch,b in zip('KQkq',(1,2,4,8)) if ch in pa[2])
 e=(int(pa[3][1])-1)*16+ord(pa[3][0])-97 if pa[3]!='-' else -1
 return B,s,c,e,w,k
def T(mv):
 f=ord(mv[0])+16*ord(mv[1])-881;t=ord(mv[2])+16*ord(mv[3])-881
 return f|t<<7|('nbrq'.index(mv[4])+2)<<14 if len(mv)==5 else f|t<<7
def H(fen,legal):
 global nd
 nd=0;bm=legal[0]
 try:
  P=F(fen)
  for d in range(1,11):
   cs=-I;cu=None
   for mv in legal:
    P2=M(P,T(mv))
    if not P2:continue
    sc=-S(P2,d-1,-I,I,1)
    if sc>cs:cs=sc;cu=mv
   if cu:bm=cu
 except X:pass
 return bm
def post(p,b):
 with u.urlopen(u.Request(U+p,data=j.dumps(b).encode())) as r:return j.load(r)
while True:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  g=post('/move',{'game':g['game'],'move':H(g['fen'],g['legal_moves'])})
