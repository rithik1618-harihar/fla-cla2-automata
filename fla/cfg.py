"""Context-free grammar: parsing, leftmost derivations, parse trees, ambiguity."""
from __future__ import annotations

EPS_NAMES = {"ε", "eps", "epsilon"}


class CFG:
    def __init__(self, name, productions, start):
        self.name = name
        self.prods = {A: [tuple(r) for r in rs] for A, rs in productions.items()}
        self.start = start
        self.nt = set(self.prods)
        self.terminals = {s for rs in self.prods.values() for r in rs
                          for s in r if s not in self.nt}
        self.nullable = self._compute_nullable()

    @classmethod
    def from_text(cls, name, text):
        """Parse lines such as ``E -> E + T | T`` (space-separated symbols, ε = empty)."""
        prods, start = {}, None
        for line in text.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            lhs, rhs = line.split("->")
            lhs = lhs.strip()
            start = start or lhs
            for alt in rhs.split("|"):
                prods.setdefault(lhs, []).append(
                    tuple(s for s in alt.split() if s not in EPS_NAMES))
        return cls(name, prods, start)

    # --------------------------------------------------------------- helpers
    def _compute_nullable(self):
        nullable, changed = set(), True
        while changed:
            changed = False
            for A, rs in self.prods.items():
                if A not in nullable and any(all(s in nullable for s in r) for r in rs):
                    nullable.add(A)
                    changed = True
        return nullable

    def min_len(self, form):
        """Lower bound on the number of terminals a sentential form must yield."""
        return sum(1 for s in form if s not in self.nullable)

    def productions_text(self):
        rows = []
        for A, rs in self.prods.items():
            rows.append(f"{A} -> " + " | ".join(" ".join(r) if r else "ε" for r in rs))
        return "\n".join(rows)

    # ----------------------------------------------------------- derivations
    def leftmost_derivations(self, tokens, limit=50, max_steps=80):
        """All leftmost derivations of ``tokens`` (up to ``limit``).

        Each derivation is a list of steps ``(A, rhs, sentential_form)``.
        Number of leftmost derivations == number of parse trees.
        """
        tokens, out = list(tokens), []
        n = len(tokens)

        def dfs(prefix, form, pos, path):
            if len(out) >= limit or len(path) > max_steps:
                return
            while form and form[0] not in self.nt:     # match leading terminals
                if pos < n and tokens[pos] == form[0]:
                    prefix, form, pos = prefix + (form[0],), form[1:], pos + 1
                else:
                    return
            if not form:
                if pos == n:
                    out.append(path)
                return
            A, rest = form[0], form[1:]
            for rhs in self.prods[A]:
                nf = rhs + rest
                if self.min_len(nf) > n - pos:
                    continue
                dfs(prefix, nf, pos, path + [(A, rhs, prefix + nf)])

        dfs((), (self.start,), 0, [])
        return out

    def generates(self, tokens) -> bool:
        return bool(self.leftmost_derivations(tokens, limit=1))

    def count_trees(self, tokens, limit=50) -> int:
        return len(self.leftmost_derivations(tokens, limit=limit))

    def strings_up_to(self, max_len):
        """Every terminal string of length <= max_len (as tuples) the grammar derives."""
        start = (self.start,)
        seen, frontier, result = {start}, [start], set()
        cap = 3 * max_len + 3
        while frontier:
            nxt = []
            for form in frontier:
                i = next((k for k, s in enumerate(form) if s in self.nt), None)
                if i is None:
                    result.add(form)
                    continue
                for rhs in self.prods[form[i]]:
                    nf = form[:i] + rhs + form[i + 1:]
                    if len(nf) > cap or self.min_len(nf) > max_len or nf in seen:
                        continue
                    seen.add(nf)
                    nxt.append(nf)
            frontier = nxt
        return {w for w in result if len(w) <= max_len}

    def ambiguity_witness(self, max_len, tree_limit=3):
        """Shortest string (<= max_len) with >= 2 parse trees, or None."""
        for w in sorted(self.strings_up_to(max_len), key=lambda w: (len(w), w)):
            if self.count_trees(w, limit=tree_limit) >= 2:
                return w
        return None

    # ---------------------------------------------------------- presentation
    def parse_tree(self, derivation):
        it = iter(derivation)

        def build(sym):
            if sym not in self.nt:
                return sym
            A, rhs, _ = next(it)
            return (A, [build(x) for x in rhs])

        return build(self.start)

    @staticmethod
    def tree_str(t):
        if isinstance(t, str):
            return t
        A, ch = t
        return A + "⟨" + (" ".join(CFG.tree_str(c) for c in ch) if ch else "ε") + "⟩"

    def format_derivation(self, derivation):
        lines = [self.start]
        for A, rhs, form in derivation:
            lines.append("  ⇒ " + (" ".join(form) if form else "ε")
                         + f"    [{A} → {' '.join(rhs) if rhs else 'ε'}]")
        return "\n".join(lines)
