import itertools
import pytest
from task3_pda_cfg import balanced, palindrome, arithmetic as ar, anbn
from fla.pda import cfg_to_pda


def bal_ref(s):
    st = []
    for c in s:
        if c in "([":
            st.append(c)
        elif not st or st.pop() != {")": "(", "]": "["}[c]:
            return False
    return not st


def test_balanced_dpda_matches_reference_up_to_8():
    assert balanced.DPDA.is_deterministic()
    for n in range(9):
        for w in itertools.product("()[]", repeat=n):
            assert bool(balanced.DPDA.accepts(w)) == bal_ref(w), w


def test_balanced_listed_cases():
    for s in balanced.VALID:
        assert balanced.DPDA.accepts(s) and balanced.REVISED.generates(list(s))
    for s in balanced.INVALID:
        assert not balanced.DPDA.accepts(s) and not balanced.REVISED.generates(list(s))


def test_balanced_grammars_equivalent_and_ambiguity():
    amb = balanced.AMBIGUOUS.strings_up_to(8)
    rev = balanced.REVISED.strings_up_to(8)
    assert amb == rev - {()}
    assert balanced.AMBIGUOUS.count_trees(list("()()()")) == 2
    assert balanced.AMBIGUOUS.ambiguity_witness(6) == tuple("()()()")
    assert balanced.REVISED.ambiguity_witness(8) is None


def test_palindrome_all_models_agree_up_to_8():
    assert not palindrome.NPDA.is_deterministic()
    for n in range(9):
        for w in itertools.product("ab", repeat=n):
            ref = w == w[::-1]
            assert bool(palindrome.NPDA.accepts(w)) == ref, w
            assert palindrome.GRAMMAR.generates(w) == ref, w
    assert palindrome.GRAMMAR.ambiguity_witness(7) is None


def test_marked_palindrome_is_deterministic():
    assert palindrome.MARKED_DPDA.is_deterministic()
    for w in ["c", "aca", "abcba", "abbcbba"]:
        assert palindrome.MARKED_DPDA.accepts(w)
    for w in ["", "ab", "acb", "abcab", "cc"]:
        assert not palindrome.MARKED_DPDA.accepts(w)


def test_arithmetic():
    A, R = ar.AMBIGUOUS, ar.REVISED
    t = ar.toks("id + id * id")
    assert A.count_trees(t) == 2 and R.count_trees(t) == 1
    assert {ar.evaluate(A.parse_tree(d), [2, 3, 4]) for d in A.leftmost_derivations(t)} == {14, 20}
    assert ar.evaluate(R.parse_tree(R.leftmost_derivations(t)[0]), [2, 3, 4]) == 14
    for s in ar.VALID:
        assert R.generates(ar.toks(s)) and ar.PDA_FROM_REVISED.accepts(ar.toks(s)), s
    for s in ar.INVALID:
        assert not R.generates(ar.toks(s)) and not ar.PDA_FROM_REVISED.accepts(ar.toks(s)), s
    assert A.strings_up_to(5) == R.strings_up_to(5)
    assert R.ambiguity_witness(5) is None
    w = A.ambiguity_witness(5)
    assert w is not None and len(w) == 5 and A.count_trees(list(w)) >= 2


def test_cfg_to_pda_agrees_with_grammar():
    for g in (balanced.REVISED, palindrome.GRAMMAR, anbn.GRAMMAR):
        p = cfg_to_pda(g)
        terms = sorted(g.terminals)
        for n in range(7):
            for w in itertools.product(terms, repeat=n):
                assert bool(p.accepts(w)) == g.generates(w), (g.name, w)


def test_anbn():
    assert anbn.DPDA.is_deterministic()
    for s in anbn.VALID:
        assert anbn.DPDA.accepts(s) and anbn.GRAMMAR.generates(list(s))
    for s in anbn.INVALID:
        assert not anbn.DPDA.accepts(s) and not anbn.GRAMMAR.generates(list(s))
    i, j, v1, v2 = anbn.pigeonhole_witness(anbn.a_star_b_star())
    assert i < j and v1 == v2          # same verdict, but only a^i b^i is in the language
