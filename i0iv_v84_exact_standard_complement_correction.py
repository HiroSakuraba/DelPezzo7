import json, math

def inter(v,w):
    return v[0]*w[0]-sum(v[i]*w[i] for i in range(1,11))

classes=[]
for d in range(0, 11):
    for a in range(0, d+1):
        for b in range(0, d+1):
            for c in range(0, d+1):
                rhs = d*d - 3*a*a - 3*b*b - 2*c*c + 3
                if rhs < 0:
                    continue
                s = 3*d + 1 - 3*a - 3*b - 2*c
                if s < 0 or (s*s-rhs) % 2:
                    continue
                mn = (s*s-rhs)//2
                disc = s*s - 4*mn
                if disc < 0:
                    continue
                t = math.isqrt(disc)
                if t*t != disc:
                    continue
                if (s+t)%2 or (s-t)%2:
                    continue
                for m,n in {((s+t)//2,(s-t)//2),((s-t)//2,(s+t)//2)}:
                    if not (0 <= m <= d and 0 <= n <= d):
                        continue
                    if d*d - 3*a*a - 3*b*b - 2*c*c - m*m - n*n != -3:
                        continue
                    if -3*d + 3*a + 3*b + 2*c + m + n != 1:
                        continue
                    classes.append((d,a,a,a,b,b,b,c,c,m,n))
classes=sorted(set(classes))

n=len(classes)
adj=[[False]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1,n):
        if inter(classes[i], classes[j]) == 0:
            adj[i][j]=adj[j][i]=True

best=[]
def bronk(R,P,X):
    global best
    if not P and not X:
        if len(R)>len(best):
            best=list(R)
        return
    if len(R)+len(P)<=len(best):
        return
    union=P|X
    if union:
        u=max(union, key=lambda u: sum(1 for v in P if adj[u][v]))
        cand=list(P - {v for v in P if adj[u][v]})
    else:
        cand=list(P)
    for v in cand:
        bronk(R|{v}, P & {w for w in P if adj[v][w]}, X & {w for w in X if adj[v][w]})
        P.remove(v); X.add(v)
bronk(set(), set(range(n)), set())
best_classes=[classes[i] for i in best]
roots=[(v[0]-3,)+tuple(v[i]-1 for i in range(1,11)) for v in best_classes]
summary={
    "exact_grouped_effective_classes_count": len(classes),
    "max_pairwise_orthogonal_subset_size": len(best_classes),
    "one_maximal_pairwise_orthogonal_subset": best_classes,
    "corresponding_root_classes_R_equals_C_plus_K": roots,
    "root_gram_matrix": [[inter(r,s) for s in roots] for r in roots],
}
print(json.dumps(summary, indent=2))
