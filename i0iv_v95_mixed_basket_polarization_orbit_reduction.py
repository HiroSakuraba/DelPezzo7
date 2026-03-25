
import itertools, math

def inter(x,y):
    d1,m1=x; d2,m2=y
    return d1*d2 - sum(a*b for a,b in zip(m1,m2))

def enumerate_root_classes():
    roots=[]
    for d in range(-4,5):
        target_sum=3*d
        target_sq=d*d+2
        arr=[0]*10
        out=[]
        def rec(i, rem_sum, rem_sq):
            if i==10:
                if rem_sum==0 and rem_sq==0:
                    out.append(tuple(arr))
                return
            n=10-i
            B=int(math.isqrt(rem_sq)) if rem_sq>=0 else 0
            for m in range(-B,B+1):
                rs=rem_sum-m; rq=rem_sq-m*m
                if rq < 0:
                    continue
                if n-1>0 and rs*rs > (n-1)*rq:
                    continue
                arr[i]=m
                rec(i+1, rs, rq)
        rec(0,target_sum,target_sq)
        roots.extend((d,m) for m in out)
    return roots

def L1_dot(r):
    d,m=r
    return d  # because sum m_i = 3d on roots

def L2_dot(r):
    d,m=r
    return 6*d - 2*sum(m[:7]) - m[7] - m[8]

def search_configuration(roots0, rootsm2):
    n0=len(roots0); n1=len(rootsm2)
    M0=[[inter(roots0[i],roots0[j]) for j in range(n0)] for i in range(n0)]
    M1=[[inter(rootsm2[i],rootsm2[j]) for j in range(n1)] for i in range(n1)]
    adj0=[set(j for j in range(n0) if j!=i and M0[i][j]==1) for i in range(n0)]
    adj1=[set(j for j in range(n1) if j!=i and M1[i][j]==1) for i in range(n1)]
    for a in range(n1):
        Na=[j for j in adj1[a] if j>a]
        for b in Na:
            Nab=[j for j in Na if j>b and j in adj1[b]]
            for c in Nab:
                Nabc=[j for j in Nab if j>c and j in adj1[c]]
                for d in Nabc:
                    Nabcd=[j for j in Nabc if j>d and j in adj1[d]]
                    for e in Nabcd:
                        clique=(a,b,c,d,e)
                        orth=[i for i in range(n0) if all(inter(roots0[i], rootsm2[j])==0 for j in clique)]
                        O=set(orth)
                        for i1 in orth:
                            for j1 in (adj0[i1] & O):
                                if j1<=i1:
                                    continue
                                used={i1,j1}
                                cand2=[x for x in orth if x not in used and M0[i1][x]==0 and M0[j1][x]==0]
                                O2=set(cand2)
                                for i2 in cand2:
                                    for j2 in (adj0[i2] & O2):
                                        if j2<=i2 or j2 in used:
                                            continue
                                        if any(M0[u][v]!=0 for u in (i1,j1) for v in (i2,j2)):
                                            continue
                                        used2=used|{i2,j2}
                                        for k in orth:
                                            if k in used2:
                                                continue
                                            if all(M0[k][u]==0 for u in used2):
                                                return clique,(i1,j1,i2,j2,k)
    return None

if __name__ == "__main__":
    roots=enumerate_root_classes()
    roots0_L1=[r for r in roots if L1_dot(r)==0]
    rootsm2_L1=[r for r in roots if L1_dot(r)==-2]
    roots0_L2=[r for r in roots if L2_dot(r)==0]
    rootsm2_L2=[r for r in roots if L2_dot(r)==-2]
    print("L1 sizes", len(roots0_L1), len(rootsm2_L1))
    print("L2 sizes", len(roots0_L2), len(rootsm2_L2))
    print("L1 config", search_configuration(roots0_L1, rootsm2_L1))
    print("L2 config", search_configuration(roots0_L2, rootsm2_L2))
