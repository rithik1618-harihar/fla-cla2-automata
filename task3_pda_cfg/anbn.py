"""Case study 4 - {a^n b^n}: why finite automata are insufficient (pigeonhole witness)."""
from fla.cfg import CFG
from fla.dfa import DFA
from fla.pda import PDA

GRAMMAR = CFG.from_text("a^n b^n", "S -> a S b | ε")
_r = [("q0", "a", "Z", "q0", "AZ"), ("q0", "a", "A", "q0", "AA"),
      ("q0", "b", "A", "q1", ""), ("q1", "b", "A", "q1", ""),
      ("q0", "$", "Z", "qf", "Z"), ("q1", "$", "Z", "qf", "Z")]
DPDA = PDA("a^n b^n DPDA", _r, "q0", "Z", finals={"qf"}, endmarker="$")

VALID = ["", "ab", "aabb", "aaabbb"]
INVALID = ["a", "b", "ba", "aab", "abb", "abab"]


def a_star_b_star() -> DFA:
    """A 'best-effort' DFA for a*b* - it cannot count, so it accepts too much."""
    d = {("s0", "a"): "s0", ("s0", "b"): "s1", ("s1", "b"): "s1"}
    return DFA("a*b*", ["a", "b"], d, "s0", {"s0", "s1"})


def pigeonhole_witness(dfa: DFA):
    """Find i<j with δ*(q0,a^i) = δ*(q0,a^j); then a^i b^i and a^j b^i get the same verdict,
    yet exactly one of them belongs to {a^n b^n}.  Hence no DFA recognises it."""
    seen, s = {}, dfa.start
    for i in range(len(dfa.states) + 1):
        if s in seen:
            j, i0 = i, seen[s]
            return (i0, j, dfa.accepts("a" * i0 + "b" * i0), dfa.accepts("a" * j + "b" * i0))
        seen[s] = i
        s = dfa.step(s, "a")
