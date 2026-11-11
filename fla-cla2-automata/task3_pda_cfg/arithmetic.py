"""Case study 3 - arithmetic expressions: ambiguity, precedence and CFG -> PDA."""
from fla.cfg import CFG
from fla.pda import cfg_to_pda

AMBIGUOUS = CFG.from_text("Expr (ambiguous)", "E -> E + E | E * E | ( E ) | id")
REVISED = CFG.from_text("Expr (unambiguous)", """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
""")
PDA_FROM_REVISED = cfg_to_pda(REVISED)


def evaluate(tree, values):
    """Evaluate a parse tree, assigning ``values`` to the id leaves left to right."""
    it = iter(values)

    def ev(t):
        if isinstance(t, str):
            return next(it)
        _, ch = t
        if len(ch) == 1:
            return ev(ch[0])
        if ch[0] == "(":
            return ev(ch[1])
        left = ev(ch[0])
        right = ev(ch[2])
        return left + right if ch[1] == "+" else left * right

    return ev(tree)


def toks(s):
    return s.split()


VALID = ["id", "id + id", "id * id", "id + id * id", "( id + id ) * id", "( ( id ) )"]
INVALID = ["id +", "+ id", "( id", "id id", ") id (", "id + * id", ""]
