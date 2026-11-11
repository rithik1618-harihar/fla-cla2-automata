"""Deterministic finite automaton with trace, minimisation and diagram export.

Transitions are defined over *symbol classes* (e.g. "digit", "letter") through a
``classify`` function, so a 256-character alphabet stays readable. Any missing
transition goes to an implicit, non-accepting ``dead`` (trap) state.
"""
from __future__ import annotations

from collections import defaultdict, deque


class DFA:
    DEAD = "dead"

    def __init__(self, name, alphabet, delta, start, accepting,
                 classify=None, state_label=None):
        self.name = name
        self.alphabet = list(alphabet)          # symbol classes
        self.delta = dict(delta)                # (state, class) -> state
        self.start = start
        self.accepting = set(accepting)
        self.classify = classify or (lambda ch: ch)
        self.state_label = state_label or str
        self.states = ({start} | {s for (s, _) in self.delta}
                       | set(self.delta.values()) | self.accepting | {self.DEAD})

    # ---------------------------------------------------------------- running
    def step(self, state, ch):
        if state == self.DEAD:
            return self.DEAD
        return self.delta.get((state, self.classify(ch)), self.DEAD)

    def run(self, string):
        """Return (accepted, trace) where trace = [(state, char, next_state)]."""
        s, trace = self.start, []
        for ch in string:
            nxt = self.step(s, ch)
            trace.append((s, ch, nxt))
            s = nxt
        return s in self.accepting, trace

    def accepts(self, string) -> bool:
        return self.run(string)[0]

    # --------------------------------------------------------------- analysis
    def reachable(self):
        seen, q = {self.start}, deque([self.start])
        while q:
            s = q.popleft()
            for a in self.alphabet:
                t = self.delta.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    q.append(t)
        return seen

    def minimal_state_count(self) -> int:
        """Moore partition refinement on the complete DFA (dead state included)."""
        states = list(self.reachable() | {self.DEAD})
        block = {s: (s in self.accepting) for s in states}
        while True:
            sig = {s: (block[s], tuple(block[self.delta.get((s, a), self.DEAD)]
                                       for a in self.alphabet)) for s in states}
            ids, new = {}, {}
            for s in states:
                new[s] = ids.setdefault(sig[s], len(ids))
            if len(set(new.values())) == len(set(block.values())):
                return len(set(new.values()))
            block = new

    # ---------------------------------------------------------------- exports
    def _order(self):
        order, seen, i = [self.start], {self.start}, 0
        while i < len(order):
            s = order[i]
            i += 1
            for a in self.alphabet:
                t = self.delta.get((s, a))
                if t is not None and t != self.DEAD and t not in seen:
                    seen.add(t)
                    order.append(t)
        return order

    def _grouped_edges(self):
        g = defaultdict(list)
        for s in self._order():
            for a in self.alphabet:
                t = self.delta.get((s, a))
                if t is not None and t != self.DEAD:
                    g[(s, t)].append(a)
        return g

    def to_mermaid(self) -> str:
        q = '"'
        order = self._order()
        ids = {s: f"s{i}" for i, s in enumerate(order)}
        lines = ["flowchart LR", f'    init(["start"]) --> {ids[self.start]}']
        for s in order:
            lab = self.state_label(s)
            shape = ("(((" + q + lab + q + ")))") if s in self.accepting \
                else ("((" + q + lab + q + "))")
            lines.append(f"    {ids[s]}{shape}")
        for (s, t), syms in self._grouped_edges().items():
            lines.append(f"    {ids[s]} -->|" + q + ", ".join(syms) + q + f"| {ids[t]}")
        return "\n".join(lines)

    def to_dot(self) -> str:
        q = '"'
        order = self._order()
        ids = {s: f"s{i}" for i, s in enumerate(order)}
        out = ["digraph DFA {", "  rankdir=LR;", '  node [shape=circle];',
               '  __start [shape=point];', f"  __start -> {ids[self.start]};"]
        for s in order:
            shape = "doublecircle" if s in self.accepting else "circle"
            out.append(f"  {ids[s]} [label={q}{self.state_label(s)}{q}, shape={shape}];")
        for (s, t), syms in self._grouped_edges().items():
            out.append(f"  {ids[s]} -> {ids[t]} [label={q}{', '.join(syms)}{q}];")
        out.append("}")
        return "\n".join(out)
