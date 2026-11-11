"""Case study 1 - balanced parentheses/brackets: CFG, ambiguity, DPDA."""
from fla.cfg import CFG
from fla.pda import PDA

AMBIGUOUS = CFG.from_text("Balanced (ambiguous)", "B -> B B | ( B ) | [ B ] | ( ) | [ ]")
REVISED = CFG.from_text("Balanced (unambiguous)", "S -> ( S ) S | [ S ] S | ε")

_rules = []
for o, c in ("()", "[]"):
    for X in ("Z", "(", "["):
        _rules.append(("q0", o, X, "q0", o + X))      # push opener
    _rules.append(("q0", c, o, "q0", ""))             # matching closer pops
_rules.append(("q0", "$", "Z", "qf", "Z"))            # end marker, stack back at Z
DPDA = PDA("Balanced brackets DPDA", _rules, "q0", "Z", finals={"qf"}, endmarker="$")

VALID = ["", "()", "[]", "([])", "()[]()", "[([])]()"]
INVALID = ["(", ")", "(]", "([)]", "())(", "((]"]
