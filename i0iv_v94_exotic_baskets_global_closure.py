
import json

def standard_form_solutions(numE, square_abs, Kpair):
    sols = []
    for d in range(0, 20):
        target_sum = 3*d + Kpair
        target_sq = d*d + square_abs
        def rec(i, prev, remsum, remsq, arr):
            if i == numE:
                if remsum == 0 and remsq == 0:
                    sols.append((d, tuple(arr)))
                return
            maxm = min(prev, remsum)
            for m in range(maxm, -1, -1):
                if m*m > remsq:
                    continue
                rec(i+1, m, remsum-m, remsq-m*m, arr+[m])
        rec(0, d, target_sum, target_sq, [])
    return sols

data = {
    "minus7_standard_solutions": standard_form_solutions(8, 7, 5),
    "minus4_standard_solutions": standard_form_solutions(9, 4, 2),
    "minus6_standard_solutions": standard_form_solutions(9, 6, 4),
    "notes": {
        "minus4_adjacency_filter": "For C2 = E5-E6 one needs m5-m6=1, which keeps only the first solution.",
        "root_counts_from_v80": {
            "7A1_plus_1_7_11": 56,
            "7A1_plus_1_7_2": 30,
            "7A1_plus_1_11_2": 30
        }
    }
}
print(json.dumps(data, indent=2))
