"""v79 note.

This file records the theorem-grade correction after v78.

The proper odd-lattice filter is expressed using the discriminant bilinear form
and the descended anticanonical class, not the naive quadratic-form language.
At that corrected level, the five baskets listed below all survive.
"""

V79 = {
    "survivors_after_v79": [
        {"1/2(1,1)": 8},
        {"1/2(1,1)": 7, "1/7(1,1)": 1},
        {"1/2(1,1)": 7, "1/7(1,2)": 1},
        {"1/2(1,1)": 7, "1/11(1,2)": 1},
        {"1/2(1,1)": 1, "1/3(1,1)": 5, "1/3(1,2)": 2},
    ],
    "next_move": "geometric realization tests rather than more discriminant-form cleanup"
}

if __name__ == "__main__":
    import json
    print(json.dumps(V79, indent=2))
