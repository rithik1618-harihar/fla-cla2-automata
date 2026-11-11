"""Password policy validator (product construction).

Policy: >= min_length printable ASCII characters (no spaces / non-ASCII),
containing at least one lowercase, uppercase, digit and special character.
State = (min(length, min_length), 4-bit mask of character classes seen).
"""
import re
import string
from collections import deque
from fla.dfa import DFA

BIT = {"lower": 1, "upper": 2, "digit": 4, "special": 8}
SPECIAL = set(string.punctuation)


def classify(ch):
    if ch in string.ascii_lowercase:
        return "lower"
    if ch in string.ascii_uppercase:
        return "upper"
    if ch in string.digits:
        return "digit"
    if ch in SPECIAL:
        return "special"
    return "other"                     # space, control, non-ASCII -> trap state


def _label(state):
    if state == DFA.DEAD:
        return "dead"
    n, mask = state
    flags = "".join(c if mask & b else "-" for c, b in zip("lUds", (1, 2, 4, 8)))
    return f"len={n},{flags}"


def build_password_dfa(min_length=8) -> DFA:
    start = (0, 0)
    delta, seen, q = {}, {start}, deque([start])
    while q:
        s = q.popleft()
        n, mask = s
        for cls, bit in BIT.items():
            t = (min(n + 1, min_length), mask | bit)
            delta[(s, cls)] = t
            if t not in seen:
                seen.add(t)
                q.append(t)
    accepting = {s for s in seen if s[0] == min_length and s[1] == 15}
    return DFA(f"Password (min {min_length})", list(BIT), delta, start, accepting,
               classify=classify, state_label=_label)


DFA_PASSWORD = build_password_dfa()
REGEX = re.compile(r"(?=[!-~]*[a-z])(?=[!-~]*[A-Z])(?=[!-~]*[0-9])"
                   r"(?=[!-~]*[^A-Za-z0-9])[!-~]{8,}")

VALID = ["Passw0rd!", "Abcdef1@x", "Zz9#Zz9#", "correct-Horse-9-battery", "P@ssw0rdP@ss"]
INVALID = ["password", "PASSWORD1!", "Pass1!", "Password!!", "Passw0rd12",
           "Passw0rd 1!", "Pässw0rd!", ""]
