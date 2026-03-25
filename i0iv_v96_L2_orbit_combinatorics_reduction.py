import importlib.util

spec=importlib.util.spec_from_file_location("v85", "/mnt/data/v85_work/i0iv_v85_restricted_simultaneous_effectivity_screen.py")
v85=importlib.util.module_from_spec(spec); spec.loader.exec_module(v85)
spec2=importlib.util.spec_from_file_location("v95", "/mnt/data/v95_work/i0iv_v95_mixed_basket_polarization_orbit_reduction.py")
v95=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(v95)

cand=v85.all_grouped_candidates()
adj=[[False]*len(cand) for _ in range(len(cand))]
for i in range(len(cand)):
    for j in range(i+1,len(cand)):
        if v85.inter(cand[i],cand[j])==0:
            adj[i][j]=adj[j][i]=True

cliques=[]
for a in range(len(cand)):
    Na=[j for j in range(a+1,len(cand)) if adj[a][j]]
    for b in Na:
        Nab=[j for j in Na if j>b and adj[b][j]]
        for c in Nab:
            Nabc=[j for j in Nab if j>c and adj[c][j]]
            for d in Nabc:
                Nabcd=[j for j in Nabc if j>d and adj[d][j]]
                for e in Nabcd:
                    cliques.append((a,b,c,d,e))

roots=v95.enumerate_root_classes()
roots0=[r for r in roots if v95.L2_dot(r)==0]
rootsm2=[r for r in roots if v95.L2_dot(r)==-2]
n1=len(rootsm2); n0=len(roots0)

M1=[[v95.inter(rootsm2[i],rootsm2[j]) for j in range(n1)] for i in range(n1)]
adj1=[set(j for j in range(n1) if j!=i and M1[i][j]==1) for i in range(n1)]
M0=[[v95.inter(roots0[i],roots0[j]) for j in range(n0)] for i in range(n0)]
adj0=[set(j for j in range(n0) if j!=i and M0[i][j]==1) for i in range(n0)]
orth_matrix=[[v95.inter(roots0[i],rootsm2[j])==0 for j in range(n1)] for i in range(n0)]

def has_A2A2A1(clique):
    orth=[i for i in range(n0) if all(orth_matrix[i][j] for j in clique)]
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
                            return True
    return False

total=0
extendable=0
for a in range(n1):
    Na=[j for j in adj1[a] if j>a]
    for b in Na:
        Nab=[j for j in Na if j>b and j in adj1[b]]
        for c in Nab:
            Nabc=[j for j in Nab if j>c and j in adj1[c]]
            for d in Nabc:
                Nabcd=[j for j in Nabc if j>d and j in adj1[d]]
                for e in Nabcd:
                    total += 1
                    if has_A2A2A1((a,b,c,d,e)):
                        extendable += 1

print("grouped 5-cliques:", len(cliques))
print("L2 transformed 5-cliques:", total)
print("extendable transformed 5-cliques:", extendable)
