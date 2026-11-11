"""Nondeterministic pushdown automaton simulator (BFS over configurations)."""
from __future__ import annotations

from collections import defaultdict, deque

from fla.cfg import CFG

EPS = ""


def _fmt(seq, empty="ε"):
    seq = list(seq)
    if not seq:
        return empty
    return "".join(seq) if all(len(s) == 1 for s in seq) else " ".join(seq)


class PDAResult:
    def __init__(self, accepted, trace, explored):
        self.accepted, self.trace, self.explored = accepted, trace, explored

    def __bool__(self):
        return self.accepted


class PDA:
    """rules: iterable of (state, input_or_'', stack_top, next_state, push).

    ``push`` is a string of 1-char symbols or a tuple of symbols; its first
    element becomes the new top of stack. ``accept_by`` is 'final' or 'empty'.
    If ``endmarker`` is set the machine reads ``input + endmarker`` (standard
    trick for presenting deterministic PDAs).
    """

    def __init__(self, name, rules, start, start_stack, finals=(),
                 accept_by="final", endmarker=None, prune=None,
                 max_stack=200, max_configs=200_000):
        self.name, self.start = name, start
        self.start_stack = tuple(start_stack)
        self.finals, self.accept_by = set(finals), accept_by
        self.endmarker, self.prune = endmarker, prune
        self.max_stack, self.max_configs = max_stack, max_configs
        self.delta = defaultdict(list)
        self.states = {start} | set(finals)
        for q, a, X, q2, push in rules:
            self.delta[(q, a, X)].append((q2, tuple(push)))
            self.states |= {q, q2}

    # --------------------------------------------------------------- running
    def _accepting(self, st, stack):
        return (st in self.finals) if self.accept_by == "final" else (not stack)

    def accepts(self, tokens) -> PDAResult:
        toks = list(tokens) + ([self.endmarker] if self.endmarker else [])
        n = len(toks)
        init = (self.start, 0, self.start_stack)
        parent, queue, explored = {init: None}, deque([init]), 0

        def build_trace(cfg):
            seq = []
            while cfg is not None:
                st, pos, stack = cfg
                seq.append(f"({st}, {_fmt(toks[pos:])}, ⟨{_fmt(stack)}⟩)")
                cfg = parent[cfg][0] if parent[cfg] else None
            return list(reversed(seq))

        while queue and explored < self.max_configs:
            cfg = queue.popleft()
            explored += 1
            st, pos, stack = cfg
            if pos == n and self._accepting(st, stack):
                return PDAResult(True, build_trace(cfg), explored)
            if not stack:
                continue
            X, rest = stack[0], stack[1:]
            moves = [(q2, pos, push) for q2, push in self.delta.get((st, EPS, X), [])]
            if pos < n:
                moves += [(q2, pos + 1, push)
                          for q2, push in self.delta.get((st, toks[pos], X), [])]
            for q2, p2, push in moves:
                ns = push + rest
                nxt = (q2, p2, ns)
                if len(ns) > self.max_stack or nxt in parent:
                    continue
                if self.prune and self.prune(q2, p2, ns, n):
                    continue
                parent[nxt] = (cfg, None)
                queue.append(nxt)
        return PDAResult(False, [], explored)

    # -------------------------------------------------------------- analysis
    def is_deterministic(self) -> bool:
        has_eps, has_inp = set(), set()
        for (q, a, X), outs in self.delta.items():
            if len(outs) > 1:
                return False
            (has_eps if a == EPS else has_inp).add((q, X))
        return not (has_eps & has_inp)

    def rules_text(self):
        rows = []
        for (q, a, X), outs in sorted(self.delta.items(), key=str):
            for q2, push in outs:
                rows.append(f"δ({q}, {a or 'ε'}, {X}) = ({q2}, {_fmt(push)})")
        return "\n".join(rows)

    def to_mermaid(self) -> str:
        qt = '"'
        edges = defaultdict(list)
        for (q, a, X), outs in self.delta.items():
            for q2, push in outs:
                edges[(q, q2)].append(f"{a or 'ε'},{X}/{_fmt(push)}")
        lines = ["flowchart LR", f'    init(["start"]) --> {self.start}']
        for s in sorted(self.states):
            lines.append(f"    {s}(((" + qt + s + qt + ")))" if s in self.finals
                         else f"    {s}((" + qt + s + qt + "))")
        for (q, q2), labs in edges.items():
            lines.append(f"    {q} -->|" + qt + "<br/>".join(sorted(labs)) + qt + f"| {q2}")
        return "\n".join(lines)


def cfg_to_pda(cfg: CFG) -> PDA:
    """Textbook construction: one state, accept by empty stack.

    δ(q, ε, A) ∋ (q, α) for every production A → α;  δ(q, a, a) = (q, ε).
    The prune hook only discards configurations that can never finish.
    """
    rules = [("q", EPS, A, "q", rhs) for A, rs in cfg.prods.items() for rhs in rs]
    rules += [("q", a, a, "q", ()) for a in cfg.terminals]
    return PDA(cfg.name + " → PDA", rules, "q", (cfg.start,), accept_by="empty",
               prune=lambda st, pos, stack, n: cfg.min_len(stack) > n - pos)
