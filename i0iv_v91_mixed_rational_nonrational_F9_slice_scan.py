
from math import comb, isqrt
import itertools, json, glob, collections

RAT_PT=(1,1)
ADD=[[0]*9 for _ in range(9)]; SUB=[[0]*9 for _ in range(9)]; MUL=[[0]*9 for _ in range(9)]; INV=[0]*9
for x in range(9):
    ax,bx=x%3,x//3
    for y in range(9):
        ay,by=y%3,y//3
        ADD[x][y]=((ax+ay)%3)+3*((bx+by)%3)
        SUB[x][y]=((ax-ay)%3)+3*((bx-by)%3)
        MUL[x][y]=((ax*ay + 2*bx*by)%3)+3*((ax*by + bx*ay)%3)
for x in range(1,9):
    for y in range(1,9):
        if MUL[x][y]==1:
            INV[x]=y; break

BINOM=[[0]*11 for _ in range(11)]
for n in range(11):
    for k in range(n+1): BINOM[n][k]=comb(n,k)%3
MONO_CACHE=[tuple((i,j) for i in range(d+1) for j in range(d+1-i)) for d in range(11)]
POW=[[1]*11 for _ in range(9)]
for x in range(9):
    for n in range(1,11): POW[x][n]=MUL[POW[x][n-1]][x]
ORD_CACHE={}; CHAIN_CACHE={}; DIM_CACHE={}
def ordinary_rows(d,pt,m):
    key=(d,pt,m)
    if key in ORD_CACHE: return ORD_CACHE[key]
    monos=MONO_CACHE[d]; a,b=pt; rows=[]
    for total in range(m):
        for u in range(total+1):
            v=total-u; row=[0]*len(monos)
            for idx,(i,j) in enumerate(monos):
                if u<=i and v<=j:
                    coeff=BINOM[i][u]*BINOM[j][v]%3
                    row[idx]=MUL[coeff][MUL[POW[a][i-u]][POW[b][j-v]]]
            rows.append(tuple(row))
    ORD_CACHE[key]=tuple(rows); return ORD_CACHE[key]
def coeff_entry(i,j,pt,s,k,v,lam):
    a,b=pt; total=0
    for p in range(i+1):
        r=k-p-(s-1)*v
        if r<0 or v>j or r>j-v: continue
        coeff=BINOM[i][p]*BINOM[j][v]*BINOM[j-v][r]%3
        if coeff:
            term=MUL[coeff][MUL[POW[a][i-p]][MUL[POW[lam][r]][POW[b][j-v-r]]]]
            total=ADD[total][term]
    return total
def chain_rows(d,pt,mults,lam):
    key=(d,pt,mults,lam)
    if key in CHAIN_CACHE: return CHAIN_CACHE[key]
    monos=MONO_CACHE[d]; rows=[]; M_prev=0
    for s,m in enumerate(mults,start=1):
        for total in range(m):
            for u in range(total+1):
                v=total-u; k=u+M_prev
                rows.append(tuple(coeff_entry(i,j,pt,s,k,v,lam) for (i,j) in monos))
        M_prev += m
    CHAIN_CACHE[key]=tuple(rows); return CHAIN_CACHE[key]
def rank_f9(mat):
    A=[list(r) for r in mat if any(r)]
    if not A: return 0
    m=len(A); n=len(A[0]); r=0; c=0
    while r<m and c<n:
        piv=r
        while piv<m and A[piv][c]==0: piv+=1
        if piv==m: c+=1; continue
        if piv!=r: A[r],A[piv]=A[piv],A[r]
        invp=INV[A[r][c]]; rowr=A[r]
        if invp!=1:
            rowr=[MUL[invp][x] for x in rowr]; A[r]=rowr
        for i in range(m):
            if i!=r and A[i][c]!=0:
                factor=A[i][c]; Ai=A[i]
                A[i]=[SUB[Ai[j]][MUL[factor][rowr[j]]] for j in range(n)]
        r+=1; c+=1
    return r
def inter(v,w):
    return v[0]*w[0]-sum(v[i]*w[i] for i in range(1,11))
def all_grouped_candidates():
    out=[]
    for d in range(0,11):
        for a in range(0,d+1):
            for b in range(0,d+1):
                for c in range(0,d+1):
                    rhs=d*d-3*a*a-3*b*b-2*c*c+3
                    if rhs<0: continue
                    s=3*d+1-3*a-3*b-2*c
                    if s<0 or (s*s-rhs)%2: continue
                    mn=(s*s-rhs)//2; disc=s*s-4*mn
                    if disc<0: continue
                    t=isqrt(disc)
                    if t*t!=disc or (s+t)%2 or (s-t)%2: continue
                    for m,n in {((s+t)//2,(s-t)//2),((s-t)//2,(s+t)//2)}:
                        if not(0<=m<=d and 0<=n<=d): continue
                        if d*d-3*a*a-3*b*b-2*c*c-m*m-n*n != -3: continue
                        if -3*d+3*a+3*b+2*c+m+n != 1: continue
                        out.append((d,a,a,a,b,b,b,c,c,m,n))
    return sorted(set(out))
CAND=all_grouped_candidates(); N=len(CAND)
ADJ=[[False]*N for _ in range(N)]
for i in range(N):
    for j in range(i+1,N):
        if inter(CAND[i],CAND[j])==0: ADJ[i][j]=ADJ[j][i]=True
def max_orth(indices):
    if not indices: return 0, []
    P0=set(indices); best=[0,[]]
    def rec(R,P,X):
        if not P and not X:
            if len(R)>best[0]:
                best[0]=len(R); best[1]=sorted(R)
            return
        if len(R)+len(P)<=best[0]: return
        union=P|X
        if union:
            u=max(union, key=lambda u: sum(1 for v in P if ADJ[u][v]))
            cand=list(P - {v for v in P if ADJ[u][v]})
        else:
            cand=list(P)
        for v in cand:
            rec(R|{v}, P & {w for w in P if ADJ[v][w]}, X & {w for w in X if ADJ[v][w]})
            P.remove(v); X.add(v)
    rec(set(), set(P0), set())
    return best[0], [CAND[i] for i in best[1]]
def dim_class(cfg,cls):
    key=(cfg,cls)
    if key in DIM_CACHE: return DIM_CACHE[key]
    lams=cfg[:3]; p9=cfg[3:5]; p10=cfg[5:7]
    d=cls[0]; a=cls[1]; b=cls[4]; c=cls[7]; m=cls[9]; n=cls[10]
    rows=[]
    rows += chain_rows(d,(0,0),(a,a,a),lams[0])
    rows += chain_rows(d,(1,0),(b,b,b),lams[1])
    rows += chain_rows(d,(0,1),(c,c),lams[2])
    rows += ordinary_rows(d,p9,m)
    rows += ordinary_rows(d,p10,n)
    DIM_CACHE[key]=len(MONO_CACHE[d])-rank_f9(rows)
    return DIM_CACHE[key]
def grouped(d,a,b,c,m,n): return (d,a,a,a,b,b,b,c,c,m,n)
def find_decomposition(cfg,D):
    d,a,b,c,m,n = D[0],D[1],D[4],D[7],D[9],D[10]
    for da in range(d+1):
        for aa in range(a+1):
            for bb in range(b+1):
                for cc in range(c+1):
                    for ma in range(m+1):
                        for na in range(n+1):
                            if da==aa==bb==cc==ma==na==0: continue
                            if da==d and aa==a and bb==b and cc==c and ma==m and na==n: continue
                            A=grouped(da,aa,bb,cc,ma,na)
                            B=grouped(d-da,a-aa,b-bb,c-cc,m-ma,n-na)
                            if dim_class(cfg,A)>0 and dim_class(cfg,B)>0:
                                return A,B
    return None

chunks=[json.load(open(f)) for f in sorted(glob.glob('/mnt/data/v90_work/chunk*.json'))]
summary=collections.Counter()
survivors=[]
for ch in chunks:
    summary.update({int(k):v for k,v in ch['summary_counts'].items()})
    survivors.extend([tuple(rec['config']['slopes']+rec['config']['p9']+rec['config']['p10']) for rec in ch['survivors']])

stage2=[]
hist=collections.Counter()
for cfg in survivors:
    rigid_idx=[i for i,cls in enumerate(CAND) if dim_class(cfg,cls)==1]
    indecomp=[]
    for i in rigid_idx:
        if find_decomposition(cfg,CAND[i]) is None:
            indecomp.append(i)
    m, subset=max_orth(indecomp)
    hist[m]+=1
    stage2.append({
        "config":{"slopes":list(cfg[:3]),"p9":list(cfg[3:5]),"p10":list(cfg[5:7])},
        "rigid_count":len(rigid_idx),
        "indecomposable_count":len(indecomp),
        "max_pairwise_orthogonal_indecomposable_subset_size":m,
        "one_maximal_subset":[list(t) for t in subset],
    })
print(json.dumps({
    "stage1_hist": dict(sorted(summary.items())),
    "stage1_survivors": len(survivors),
    "stage2_hist": dict(sorted(hist.items())),
    "stage2_global_max": max(hist) if hist else 0,
    "max_configs": [x for x in stage2 if x["max_pairwise_orthogonal_indecomposable_subset_size"]==max(hist)],
}, indent=2))
