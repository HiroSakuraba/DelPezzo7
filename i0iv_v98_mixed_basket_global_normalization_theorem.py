import itertools, math, json, numpy as np, importlib.util

spec=importlib.util.spec_from_file_location('v95', '/mnt/data/v95_work/i0iv_v95_mixed_basket_polarization_orbit_reduction.py')
v95=importlib.util.module_from_spec(spec); spec.loader.exec_module(v95)

roots=v95.enumerate_root_classes()
roots0=[r for r in roots if v95.L2_dot(r)==0]
rootsm2=[r for r in roots if v95.L2_dot(r)==-2]
root0_to_idx={r:i for i,r in enumerate(roots0)}
n0=len(roots0); n1=len(rootsm2)
M0=[[v95.inter(roots0[i],roots0[j]) for j in range(n0)] for i in range(n0)]
M1=[[v95.inter(rootsm2[i],rootsm2[j]) for j in range(n1)] for i in range(n1)]
adj0=[set(j for j in range(n0) if j!=i and M0[i][j]==1) for i in range(n0)]
adj1=[set(j for j in range(n1) if j!=i and M1[i][j]==1) for i in range(n1)]
orth_matrix=[[v95.inter(roots0[i],rootsm2[j])==0 for j in range(n1)] for i in range(n0)]
neg0={}
for i,r in enumerate(roots0):
    nr=(-r[0], tuple(-x for x in r[1]))
    neg0[i]=root0_to_idx[nr]

def root_arr(r):
    return np.array([r[0], *r[1]], dtype=int)

def generated_rootset_from_simple5(state):
    inds=list(state)
    edges=[]; iso=None; used=set()
    for i in range(5):
        if i in used: continue
        found=False
        for j in range(i+1,5):
            if M0[inds[i]][inds[j]]==1:
                edges.append((inds[i],inds[j])); used|={i,j}; found=True; break
        if not found:
            iso=inds[i]
    out=set()
    for a,b in edges:
        rv=root_arr(roots0[a])+root_arr(roots0[b])
        rk=(int(rv[0]), tuple(int(x) for x in rv[1:]))
        k=root0_to_idx[rk]
        out|={a,b,k,neg0[a],neg0[b],neg0[k]}
    out|={iso,neg0[iso]}
    return frozenset(out)

def is_A2A2A1_state(state):
    state=list(state)
    ones=0
    for i in range(5):
        for j in range(i+1,5):
            x=M0[state[i]][state[j]]
            if x==1:
                ones += 1
            elif x!=0:
                return False
    return ones==2

# standard canonical subsystem from v95
std_roots=[
    (0,(1,0,-1,0,0,0,0,0,0,0)),
    (0,(-1,1,0,0,0,0,0,0,0,0)),
    (0,(0,0,0,1,0,-1,0,0,0,0)),
    (0,(0,0,0,0,-1,1,0,0,0,0)),
    (0,(0,0,0,0,0,0,0,1,-1,0)),
]
std_state=tuple(sorted(root0_to_idx[r] for r in std_roots))
std_rootset=generated_rootset_from_simple5(std_state)

# enumerate all A2 rootsets in roots0
A2_sets=set()
for i in range(n0):
    for j in adj0[i]:
        if j>i:
            rv=root_arr(roots0[i])+root_arr(roots0[j])
            rk=(int(rv[0]), tuple(int(x) for x in rv[1:]))
            k=root0_to_idx[rk]
            A2_sets.add(frozenset([i,j,k,neg0[i],neg0[j],neg0[k]]))
A2_list=list(A2_sets)

def rootset_orth(S,T):
    return all(M0[i][j]==0 for i in S for j in T)

orth_to_A2=[]
for S in A2_list:
    orth={i for i in range(n0) if all(M0[i][j]==0 for j in S)}
    orth_to_A2.append(orth)

A2A2A1_rootsets=set()
for a_idx,S1 in enumerate(A2_list):
    for b_idx in range(a_idx+1,len(A2_list)):
        S2=A2_list[b_idx]
        if not rootset_orth(S1,S2):
            continue
        common=orth_to_A2[a_idx] & orth_to_A2[b_idx]
        for i in common:
            if i>neg0[i]:
                continue
            rootset=frozenset(set(S1)|set(S2)|{i,neg0[i]})
            if len(rootset)==14:
                A2A2A1_rootsets.add(rootset)
A2A2A1_list=list(A2A2A1_rootsets)
rs_to_idx={S:i for i,S in enumerate(A2A2A1_list)}

# root reflections on roots0
perms=[]
for j in range(n0):
    perm=[]
    rj=root_arr(roots0[j])
    for i in range(n0):
        coeff=M0[i][j]
        if coeff==0:
            perm.append(i)
        elif coeff==2:
            perm.append(neg0[i])
        else:
            rv=root_arr(roots0[i]) + coeff*rj
            rk=(int(rv[0]), tuple(int(x) for x in rv[1:]))
            perm.append(root0_to_idx[rk])
    perms.append(tuple(perm))

# orbit decomposition on canonical rootsets
unseen=set(range(len(A2A2A1_list)))
orbit_id=[None]*len(A2A2A1_list)
orbit_sizes=[]
oid=0
while unseen:
    start=unseen.pop()
    orb={start}
    stack=[start]
    while stack:
        sidx=stack.pop()
        arr=list(A2A2A1_list[sidx])
        for perm in perms:
            im=frozenset(perm[i] for i in arr)
            j=rs_to_idx.get(im)
            if j is not None and j not in orb:
                orb.add(j); unseen.discard(j); stack.append(j)
    for j in orb:
        orbit_id[j]=oid
    orbit_sizes.append(len(orb))
    oid += 1
std_orbit_id=orbit_id[rs_to_idx[std_rootset]]

# complement root counts for each orbit representative
comp_counts={}
for oid in range(len(orbit_sizes)):
    rep_idx=orbit_id.index(oid)
    S=A2A2A1_list[rep_idx]
    comp=sum(1 for i in range(n0) if all(M0[i][j]==0 for j in S))
    comp_counts[oid]=comp

# enumerate transformed 5-cliques and determine which canonical orbit(s) are compatible
compat_patterns={}
pattern_counter={}
example_clique_for_pattern={}
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
                    orth=[i for i in range(n0) if all(orth_matrix[i][j] for j in clique)]
                    O=set(orth)
                    rs_orbits=set()
                    for i1 in orth:
                        for j1 in (adj0[i1] & O):
                            if j1<=i1: continue
                            used={i1,j1}
                            cand2=[x for x in orth if x not in used and M0[i1][x]==0 and M0[j1][x]==0]
                            O2=set(cand2)
                            for i2 in cand2:
                                for j2 in (adj0[i2] & O2):
                                    if j2<=i2 or j2 in used: continue
                                    if any(M0[u][v]!=0 for u in (i1,j1) for v in (i2,j2)): continue
                                    used2=used|{i2,j2}
                                    for k in orth:
                                        if k in used2: continue
                                        if all(M0[k][u]==0 for u in used2):
                                            rs=generated_rootset_from_simple5((i1,j1,i2,j2,k))
                                            rs_orbits.add(orbit_id[rs_to_idx[rs]])
                    patt=tuple(sorted(rs_orbits))
                    pattern_counter[patt]=pattern_counter.get(patt,0)+1
                    example_clique_for_pattern.setdefault(patt, clique)

out={
    'L2_root_count': n0,
    'transformed_root_count': n1,
    'A2A2A1_rootset_count': len(A2A2A1_list),
    'canonical_orbit_sizes_under_WL2': orbit_sizes,
    'standard_orbit_id': std_orbit_id,
    'complement_root_counts_by_orbit': comp_counts,
    'transformed_5_clique_count': sum(pattern_counter.values()),
    'canonical_orbit_compatibility_patterns': {str(k): v for k,v in pattern_counter.items()},
    'example_clique_for_pattern': {str(k): list(v) for k,v in example_clique_for_pattern.items()},
}
print(json.dumps(out, indent=2, sort_keys=True))
with open('/mnt/data/v98_work/i0iv_v98_mixed_basket_global_normalization_theorem.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True)
