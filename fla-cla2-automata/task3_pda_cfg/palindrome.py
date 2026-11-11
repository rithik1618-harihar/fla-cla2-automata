"""Case study 2 - palindromes over {a,b}: CFG, NPDA (guess the middle), DPDA for w c w^R."""
from fla.cfg import CFG
from fla.pda import PDA

GRAMMAR = CFG.from_text("Palindromes", "P -> a P a | b P b | a | b | ε")
MARKED_GRAMMAR = CFG.from_text("w c w^R", "S -> a S a | b S b | c")

_r = []
for X in ("Z", "a", "b"):
    for c in "ab":
        _r.append(("q0", c, X, "q0", c + X))     # push
        _r.append(("q0", c, X, "q1", X))         # odd length: this symbol is the centre
    _r.append(("q0", "", X, "q1", X))            # even length: guess the middle (ε-move)
for c in "ab":
    _r.append(("q1", c, c, "q1", ""))            # pop while matching
_r.append(("q1", "", "Z", "qf", "Z"))
NPDA = PDA("Palindrome NPDA", _r, "q0", "Z", finals={"qf"})

_d = []
for c in "ab":
    for X in "Zab":
        _d.append(("q0", c, X, "q0", c + X))
for X in "Zab":
    _d.append(("q0", "c", X, "q1", X))           # the marker removes the guess
for c in "ab":
    _d.append(("q1", c, c, "q1", ""))
_d.append(("q1", "$", "Z", "qf", "Z"))
MARKED_DPDA = PDA("w c w^R DPDA", _d, "q0", "Z", finals={"qf"}, endmarker="$")

VALID = ["", "a", "aa", "aba", "abba", "baab", "ababa"]
INVALID = ["ab", "aab", "abb", "abab", "baa"]
