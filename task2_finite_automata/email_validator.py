"""Simplified e-mail *format* validator (subset of RFC 5322).

local   = alnum+ ( [._-] alnum+ )*          no leading/trailing/double separators
domain  = ( label '.' )+ tld                at least one dot
label   = alnum+ ( '-'+ alnum+ )*           hyphens only inside a label
tld     = [A-Za-z]{2,}                      letters only, length >= 2
"""
import re
import string
from fla.dfa import DFA

LD = ("letter", "digit")


def classify(ch):
    if ch in string.ascii_letters:
        return "letter"
    if ch in string.digits:
        return "digit"
    return {".": "dot", "_": "underscore", "-": "hyphen", "@": "at"}.get(ch, "other")


def build_email_dfa() -> DFA:
    d = {}

    def add(src, syms, dst):
        for s in ([syms] if isinstance(syms, str) else syms):
            d[(src, s)] = dst

    # local part
    add("S0", LD, "L1")
    add("L1", LD, "L1"); add("L1", ("dot", "underscore", "hyphen"), "L2"); add("L1", "at", "P0")
    add("L2", LD, "L1")
    # domain, before the first dot
    add("P0", LD, "P1")
    add("P1", LD, "P1"); add("P1", "hyphen", "P2"); add("P1", "dot", "Q0")
    add("P2", "hyphen", "P2"); add("P2", LD, "P1")
    # domain, after >= 1 dot (Ql2 = current label is letters-only, length >= 2)
    add("Q0", "letter", "Ql1"); add("Q0", "digit", "Qh")
    for src in ("Ql1", "Ql2"):
        add(src, "letter", "Ql2"); add(src, "digit", "Qh")
        add(src, "hyphen", "Qd"); add(src, "dot", "Q0")
    d[("Ql1", "letter")] = "Ql2"
    add("Qh", LD, "Qh"); add("Qh", "hyphen", "Qd"); add("Qh", "dot", "Q0")
    add("Qd", "hyphen", "Qd"); add("Qd", LD, "Qh")
    alphabet = ["letter", "digit", "dot", "underscore", "hyphen", "at"]
    return DFA("E-mail format", alphabet, d, "S0", {"Ql2"}, classify=classify)


DFA_EMAIL = build_email_dfa()
_LOCAL = r"[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*"
_DOMAIN = r"(?:[A-Za-z0-9]+(?:-+[A-Za-z0-9]+)*\.)+[A-Za-z]{2,}"
REGEX = re.compile(_LOCAL + "@" + _DOMAIN)

VALID = ["user@example.com", "first.last@mail.srmist.edu.in", "a_b-c@x1.org",
         "student123@srm-trichy.ac.in", "A@b.co"]
INVALID = ["user@example", "user@.com", "@example.com", "user..name@example.com",
           ".user@example.com", "user@exam_ple.com", "user@example.c",
           "user@example.c0m", "user name@example.com", "user@@example.com",
           "user@-example.com", "user@example-.com"]
