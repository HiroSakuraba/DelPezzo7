import json, itertools
# This file records the exact normalized-screen computations summarized in v80.
V80 = {
  "headline": "v80 normalized blowup-basis geometric screen",
  "setup": {
    "ambient": "Work in the standard blowup lattice NS(Y)=<H,E_1,...,E_n> with H^2=1, E_i^2=-1, K_Y=-3H+sum E_i.",
    "goal": "Test whether the five v79 survivor baskets admit concrete exceptional configurations in the standard blowup model, rather than only discriminant-form survivals."
  },
  "results": {
    "7A1_plus_1_7_11": {
      "representative_curve": "C = H - E1 - ... - E8 on Bl_8 P2",
      "curve_square": -7,
      "curve_K_pairing": 5,
      "exact_orthogonal_root_count": 56,
      "identified_root_type": "A7 (by root count 56)",
      "max_mutually_orthogonal_roots": 4,
      "verdict": "Fails: the orthogonal root subsystem is A7, which supports at most 4 pairwise orthogonal roots, far short of the needed 7 A1 curves."
    },
    "7A1_plus_1_7_2": {
      "representative_chain": [
        "C1 = H - E1 - ... - E5",
        "C2 = E6 - E5"
      ],
      "squares": [
        -4,
        -2
      ],
      "K_pairings": [
        2,
        0
      ],
      "adjacency": 1,
      "exact_orthogonal_real_root_count": 14,
      "identified_root_type": "A5 (by root count 30)",
      "max_mutually_orthogonal_roots": 3,
      "verdict": "Fails in the normalized screen: the affine-E8 real roots orthogonal to the noncanonical [4,2] block form an A5 subsystem, so at most 3 pairwise orthogonal A1 roots survive, not 7."
    },
    "7A1_plus_1_11_2": {
      "representative_chain": [
        "C1 = H - E1 - ... - E7",
        "C2 = E8 - E7"
      ],
      "squares": [
        -6,
        -2
      ],
      "K_pairings": [
        4,
        0
      ],
      "adjacency": 1,
      "exact_orthogonal_real_root_count": 30,
      "identified_root_type": "A5 (by root count 30)",
      "max_mutually_orthogonal_roots": 3,
      "verdict": "Fails in the normalized screen: again the orthogonal real-root subsystem is A5, so the needed 7 extra A1 curves cannot fit."
    },
    "mixed_basket_normalized": {
      "root_subsystem": [
        "E1-E2",
        "E2-E3",
        "E4-E5",
        "E5-E6",
        "E7-E8"
      ],
      "small_minus3_candidates_total": 420,
      "small_minus3_candidates_orthogonal_to_root_subsystem": 11,
      "max_pairwise_orthogonal_minus3_classes": 3,
      "example_maximal_set": [
        [
          1,
          0,
          0,
          0,
          0,
          0,
          0,
          1,
          1,
          1,
          1
        ],
        [
          1,
          0,
          0,
          0,
          1,
          1,
          1,
          0,
          0,
          0,
          1
        ],
        [
          1,
          1,
          1,
          1,
          0,
          0,
          0,
          0,
          0,
          0,
          1
        ]
      ],
      "verdict": "Fails in the normalized screen: after fixing a standard A2+A2+A1 canonical root subsystem, the bounded exact search over all small -3 classes finds at most 3 pairwise orthogonal -3 classes orthogonal to it, never the required 5."
    },
    "pure_8A1": {
      "status": "Still survives the lattice/geometric screen; this is the Gorenstein basket already isolated earlier."
    }
  },
  "interpretation": {
    "non_gorenstein_survivors": "All four non-Gorenstein v79 survivors fail this normalized geometric screen.",
    "remaining_live_case": "Only the pure 8A1 basket survives this step, and that is precisely the Gorenstein degree-1 lane already attacked separately in v72/v73.",
    "caution": "The mixed basket failure is strongest in the normalized standard-form screen; promoting it to a theorem would still require proving enough orbit-rigidity for the chosen A2+A2+A1 normalization."
  }
}
if __name__ == "__main__":
    print(json.dumps(V80, indent=2))
