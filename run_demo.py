"""Console demo for both assignments:  python run_demo.py"""
from task2_finite_automata import pin, password, email_validator as email
from task2_finite_automata.semantic_layer import check_pin, check_password, check_email
from task3_pda_cfg import balanced, palindrome, arithmetic as ar, anbn


def hdr(t):
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


def table(dfa, valid, invalid):
    for s in valid + invalid:
        print(f"  {'ACCEPT' if dfa.accepts(s) else 'REJECT'}  {s!r}")


hdr("TASK 2 - FINITE AUTOMATA FOR VALIDATION")
for mod, dfa in ((pin, pin.DFA_PIN), (password, password.DFA_PASSWORD), (email, email.DFA_EMAIL)):
    print(f"\n[{dfa.name}] reachable states={len(dfa.reachable())}, "
          f"minimal states (incl. dead)={dfa.minimal_state_count()}")
    table(dfa, mod.VALID, mod.INVALID)
ok, trace = email.DFA_EMAIL.run("a.b@c.io")
print("\nTrace for 'a.b@c.io':", " ".join(f"{s}-{c}->{t}" for s, c, t in trace), "| accepted:", ok)
print("\nSyntax vs semantic layer:")
for v in (check_pin("0000"), check_pin("12a4"), check_pin("4821"),
          check_password("Passw0rd!", username="passw0rd"), check_email("x@mailinator.com")):
    print("  ", v)

hdr("TASK 3 - CFG / PDA CASE STUDIES")
print("\n-- Case 1: balanced brackets (ambiguous grammar) --")
w = list("()()()")
for d in balanced.AMBIGUOUS.leftmost_derivations(w):
    print(balanced.AMBIGUOUS.tree_str(balanced.AMBIGUOUS.parse_tree(d)))
print("revised grammar trees:", balanced.REVISED.count_trees(w))
r = balanced.DPDA.accepts(list("([])"))
print("DPDA on '([])' accepted:", r.accepted, "\n  " + "\n  ⊢ ".join(r.trace))
print("DPDA on '([)]' accepted:", balanced.DPDA.accepts(list("([)]")).accepted)

print("\n-- Case 2: palindromes --")
r = palindrome.NPDA.accepts(list("abba"))
print("NPDA 'abba':", r.accepted, "\n  " + "\n  ⊢ ".join(r.trace))
print("NPDA deterministic?", palindrome.NPDA.is_deterministic(),
      "| w c w^R DPDA deterministic?", palindrome.MARKED_DPDA.is_deterministic())

print("\n-- Case 3: arithmetic expressions --")
t = ar.toks("id + id * id")
for d in ar.AMBIGUOUS.leftmost_derivations(t):
    tree = ar.AMBIGUOUS.parse_tree(d)
    print(ar.AMBIGUOUS.tree_str(tree), "=> value with id=2,3,4:", ar.evaluate(tree, [2, 3, 4]))
d = ar.REVISED.leftmost_derivations(t)[0]
print("\nRevised grammar, unique leftmost derivation:\n" + ar.REVISED.format_derivation(d))
print("value:", ar.evaluate(ar.REVISED.parse_tree(d), [2, 3, 4]))
print("rejected 'id + * id':", ar.PDA_FROM_REVISED.accepts(ar.toks("id + * id")).accepted)

print("\n-- Case 4: a^n b^n and the pigeonhole argument --")
i, j, v1, v2 = anbn.pigeonhole_witness(anbn.a_star_b_star())
print(f"a*b* DFA: a^{i} and a^{j} reach the same state, so a^{i}b^{i} and a^{j}b^{i} get the same verdict "
      f"({v1} / {v2}); but only a^{i}b^{i} is in {{a^n b^n}} -> the DFA must be wrong on one of them.")
print("DPDA on 'aaabbb':", anbn.DPDA.accepts("aaabbb").accepted)
