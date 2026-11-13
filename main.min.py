#!/usr/bin/env python3
_F=' PNBRQK'
_E=False
_D='0000000000000000000000000000000000000000000000000000000000000000'
_C=True
_A=None
import os,json,urllib.request as U
V=0,100,320,330,500,900,20000
IC=_F
KN=-17,-15,-10,-6,6,10,15,17
KI=-9,-8,-7,-1,1,7,8,9
_P=_D
_N=_D
_B=_D
_R=_D
_Q=_D
_K=_D
PST=0,1,2,3,4,5,6
class B:
	def __init__(A,fen=_A):A.b=[0]*64;A.t=1;A.c=0;A.e=-1;A.q=[];A.f(fen if fen is not _A else'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
	def f(A,fen):
		A.b=[0]*64;B=fen.split();F=B[0].split('/')
		for(G,H)in enumerate(F):
			D=0
			for C in H:
				if C.isdigit():D+=int(C)
				else:A.b[(7-G)*8+D]=(1 if C.isupper()else-1)*_F.index(C.upper());D+=1
		A.t=1 if B[1]=='w'else-1;E=0
		for(I,C)in enumerate('KQkq'):
			if C in B[2]:E|=1<<I
		A.c=E;A.e=-1
		if B[3]!='-':A.e=ord(B[3][0])-97+(int(B[3][1])-1)*8
	def fen(B):
		E=' ';F=[]
		for H in range(8):
			C='';A=0
			for I in range(8):
				D=B.b[(7-H)*8+I]
				if D==0:A+=1
				else:
					if A:C+=str(A);A=0
					C+=IC[abs(D)]if D>0 else IC[abs(D)].lower()
			if A:C+=str(A)
			F.append(C)
		G=''
		for(J,K)in enumerate('KQkq'):
			if B.c&1<<J:G+=K
		A='-'if B.e<0 else chr(97+B.e%8)+str(B.e//8+1);return'/'.join(F)+E+('w'if B.t==1 else'b')+E+(G or'-')+E+A
	def king(B,side):
		for A in range(64):
			if B.b[A]==6*side:return A
		return-1
	def att(J,i,by):
		C=by;D=J.b
		if C==1:
			for B in(-9,-7):
				A=i+B
				if 0<=A<64 and abs(A%8-i%8)==1 and D[A]==1:return _C
		else:
			for B in(9,7):
				A=i+B
				if 0<=A<64 and abs(A%8-i%8)==1 and D[A]==-1:return _C
		for B in KN:
			A=i+B
			if 0<=A<64 and abs(A%8-i%8)in(1,2)and D[A]==2*C:return _C
		for B in KI:
			A=i+B
			if 0<=A<64 and abs(A%8-i%8)<=1 and D[A]==6*C:return _C
		for(E,F)in((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
			H=i//8+E;I=i%8+F
			while 0<=H<8 and 0<=I<8:
				A=H*8+I;G=D[A]
				if G:
					if G==5*C or G==4*C and(E==0 or F==0)or G==3*C and E!=0 and F!=0:return _C
					break
				H+=E;I+=F
		return _E
	def chk(A,side=_A):B=side;C=A.king(-A.t if B is _A else B);return C>=0 and A.att(C,A.t if B is _A else-B)
	def gm(D):
		F=D.t;B=D.b;E=[]
		for C in range(64):
			K=B[C]
			if K==0 or K*F<=0:continue
			H=abs(K);I=C%8;J=C//8
			if H==1:
				if F==1:
					A=C+8
					if J==6 and A<64 and B[A]<=0:
						for L in(2,3,4,5):E.append((C,A,L))
					elif A<64 and B[A]==0:
						E.append((C,A,0))
						if J==1 and B[A+8]==0:E.append((C,A+8,0))
					for G in(7,9):
						A=C+G
						if A<64 and abs(A%8-I)==1:
							if B[A]<0 or A==D.e:E.append((C,A,0))
				else:
					A=C-8
					if J==1 and A>=0 and B[A]>=0:
						for L in(2,3,4,5):E.append((C,A,L))
					elif A>=0 and B[A]==0:
						E.append((C,A,0))
						if J==6 and B[A-8]==0:E.append((C,A-8,0))
					for G in(-7,-9):
						A=C+G
						if A>=0 and abs(A%8-I)==1:
							if B[A]>0 or A==D.e:E.append((C,A,0))
			elif H==2:
				for G in KN:
					A=C+G
					if 0<=A<64 and abs(A%8-I)in(1,2)and B[A]*F<=0:E.append((C,A,0))
			elif H in(3,4,5):
				R=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))if H==5 else((-1,-1),(-1,1),(1,-1),(1,1))if H==3 else((-1,0),(0,-1),(0,1),(1,0))
				for(O,P)in R:
					M=J+O;N=I+P
					while 0<=M<8 and 0<=N<8:
						A=M*8+N;Q=B[A]
						if Q==0:E.append((C,A,0))
						else:
							if Q*F<0:E.append((C,A,0))
							break
						M+=O;N+=P
			elif H==6:
				for G in KI:
					A=C+G
					if 0<=A<64 and abs(A%8-I)<=1 and B[A]*F<=0:E.append((C,A,0))
				if F==1 and C==4:
					if D.c&1 and not B[5]and not B[6]and B[7]==4 and not D.att(4,-1)and not D.att(5,-1)and not D.att(6,-1):E.append((4,6,0))
					if D.c&2 and not B[3]and not B[2]and not B[1]and B[0]==4 and not D.att(4,-1)and not D.att(3,-1)and not D.att(2,-1):E.append((4,2,0))
				elif F==-1 and C==60:
					if D.c&4 and not B[61]and not B[62]and B[63]==-4 and not D.att(60,1)and not D.att(61,1)and not D.att(62,1):E.append((60,62,0))
					if D.c&8 and not B[59]and not B[58]and not B[57]and B[56]==-4 and not D.att(60,1)and not D.att(59,1)and not D.att(58,1):E.append((60,58,0))
		return E
	def mk(A,m):
		C,D,H=m;B=A.b;I=B[D];E=B[C];K=A.c;L=A.e;B[D]=B[C];B[C]=0
		if H:B[D]=H*A.t
		J=-1
		if I==0 and E==1 and D==A.e:I=-99;J=A.e-8*A.t;B[J]=0
		F=_E
		if E==6*A.t:
			if C==4 and D==6:B[5],B[7]=B[7],0;F=_C
			elif C==4 and D==2:B[3],B[0]=B[0],0;F=_C
			elif C==60 and D==62:B[61],B[63]=B[63],0;F=_C
			elif C==60 and D==58:B[59],B[56]=B[56],0;F=_C
		if A.c:
			for G in(C,D):
				if G==0:A.c&=~2
				elif G==7:A.c&=~1
				elif G==56:A.c&=~8
				elif G==63:A.c&=~4
			if E==6:A.c&=~3
			elif E==-6:A.c&=~12
		A.e=-1
		if E==1 and C//8==1 and D//8==3:A.e=C+8
		if E==-1 and C//8==6 and D//8==4:A.e=C-8
		A.q.append((C,D,H,I,K,L,E,F,J));A.t=-A.t
	def un(B):
		D,C,K,E,F,G,H,I,J=B.q.pop();A=B.b;B.t=-B.t;A[D]=H;A[C]=0
		if E==-99:A[J]=-B.t
		elif E:A[C]=E
		if I:
			if D==4 and C==6:A[7],A[5]=A[5],0
			elif D==4 and C==2:A[0],A[3]=A[3],0
			elif D==60 and C==62:A[63],A[61]=A[61],0
			elif D==60 and C==58:A[56],A[59]=A[59],0
		B.c=F;B.e=G
E=0
def ev(board):
	B=0;E=F=0;G=board.b
	for C in range(64):
		A=G[C]
		if not A:continue
		if A>0:
			B+=V[A]+PTV[A][C]
			if A==3:E+=1
		else:
			D=-A;B-=V[D]+PTV[D][63-C]
			if D==3:F+=1
	if E>=2:B+=25
	if F>=2:B-=25
	return B
def order(board,moves):
	A=board;I=A.t;C=[]
	for D in moves:
		E,F,G=D;B=0;H=A.b[F]
		if H:B+=10*V[abs(H)]-V[abs(A.b[E])]
		elif G:B+=900+V[G]
		elif A.b[E]==1 and F==A.e:B+=100
		C.append((-B,D))
	C.sort();return[A for(B,A)in C]
class E:
	def __init__(A,budget=20000,depth=5):A.budget=budget;A.maxdepth=depth;A.nodes=0
	def qs(B,board,a,b):
		A=board;B.nodes+=1
		if B.nodes>B.budget:return ev(A)*A.t
		C=ev(A)*A.t
		if C>=b:return b
		if C>a:a=C
		for E in order(A,[B for B in A.gm()if A.b[B[1]]or A.b[B[0]]==1 and B[1]==A.e or B[2]]):
			A.mk(E)
			if A.chk(-A.t):A.un();continue
			D=-B.qs(A,-b,-a);A.un()
			if D>=b:return b
			if D>a:a=D
		return a
	def sr(B,board,d,a,b):
		A=board;B.nodes+=1
		if B.nodes>B.budget:return ev(A)*A.t
		D=A.gm()
		if not D:return-30000+(B.maxdepth-d)if A.chk()else 0
		if d<=0:return B.qs(A,a,b)
		for E in order(A,D):
			A.mk(E)
			if A.chk(-A.t):A.un();continue
			C=-B.sr(A,d-1,-b,-a);A.un()
			if C>=b:return b
			if C>a:a=C
		return a
	def best(A,board,legal=_A):
		G=legal;B=board;D=B.gm()
		if G is not _A:L=set(G);D=[B for B in D if A.uci(B)in L]
		if not D:return
		H=_A;M=-1e9;I=_E
		for N in range(1,A.maxdepth+1):
			A.nodes=0;E=-1e9;O=1e9;F=_A;C=-1e9
			for J in order(B,D):
				B.mk(J)
				if B.chk(-B.t):B.un();continue
				I=_C;K=-A.sr(B,N-1,-O,-E);B.un()
				if K>C:C=K;F=J
				if C>E:E=C
				if A.nodes>A.budget:break
			if F is not _A:H,M=F,C
			if A.nodes>A.budget:break
		return H if I else _A
	@staticmethod
	def uci(m):
		A,B,C=m;D=chr(97+A%8)+str(A//8+1)+chr(97+B%8)+str(B//8+1)
		if C:D+=IC[C].lower()
		return D
def post(base,path,body):
	A=U.Request(base+path,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
	with U.urlopen(A)as B:return json.load(B)
def main():
	J='game';I='done';D='status';F=os.environ['MAKEFUN_ENV_URL'];G=E(int(os.environ.get('ENGINE_BUDGET','20000')),int(os.environ.get('ENGINE_DEPTH','5')))
	while _C:
		A=post(F,'/game',{})
		if A[D]==I:break
		while A[D]=='your_move':
			K=B(A['fen']);H=A['legal_moves'];C=G.best(K,H)
			if C is _A:C=H[0]
			A=post(F,'/move',{J:A[J],'move':G.uci(C)})
		if A[D]==I:break
if __name__=='__main__':main()