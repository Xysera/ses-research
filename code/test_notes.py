from lib import *
for c in CONDS[1:]:
    for k in (0, 7, 19):
        n, s = make_note(c, k); print(c, k, s, len(n.split()), "|", n)
