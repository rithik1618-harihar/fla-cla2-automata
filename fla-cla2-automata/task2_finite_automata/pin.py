"""ATM PIN syntax validator: exactly 4 or 6 ASCII digits."""
import re
from fla.dfa import DFA

DIGITS = "0123456789"


def classify(ch):
    return "digit" if ch in DIGITS else "other"


def build_pin_dfa(lengths=(4, 6)) -> DFA:
    m = max(lengths)
    delta = {(f"q{i}", "digit"): f"q{i + 1}" for i in range(m)}
    return DFA("ATM PIN", ["digit"], delta, "q0",
               {f"q{l}" for l in lengths}, classify=classify)


DFA_PIN = build_pin_dfa()
REGEX = re.compile(r"[0-9]{4}(?:[0-9]{2})?")      # equivalent regular expression

VALID = ["1234", "0000", "4821", "987654", "000007"]
INVALID = ["", "123", "12345", "1234567", "12a4", "12 34", "-123", "١٢٣٤"]
