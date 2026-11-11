"""Syntax (finite automaton) vs semantic / business rules (extra processing)."""
from dataclasses import dataclass
import hmac

from task2_finite_automata.pin import DFA_PIN
from task2_finite_automata.password import DFA_PASSWORD
from task2_finite_automata.email_validator import DFA_EMAIL

WEAK_PINS = {"0000", "1234", "1111", "4321", "123456", "000000", "654321"}
COMMON_PASSWORDS = {"Password1!", "Qwerty123!", "Welcome@123", "Admin@1234"}
DISPOSABLE_DOMAINS = {"mailinator.com", "10minutemail.com", "tempmail.com"}
MAX_ATTEMPTS = 3


@dataclass
class Verdict:
    ok: bool
    stage: str          # "syntax" (regular language) or "semantic" (business rule)
    reason: str


def check_pin(pin, stored_pin=None, failed_attempts=0) -> Verdict:
    if not DFA_PIN.accepts(pin):
        return Verdict(False, "syntax", "PIN must be exactly 4 or 6 ASCII digits")
    if failed_attempts >= MAX_ATTEMPTS:
        return Verdict(False, "semantic", "card locked after too many attempts")
    if pin in WEAK_PINS or len(set(pin)) == 1 or pin in "0123456789" or pin in "9876543210":
        return Verdict(False, "semantic", "PIN too easy to guess")
    if stored_pin is not None and not hmac.compare_digest(pin, stored_pin):
        return Verdict(False, "semantic", "PIN does not match the card record")
    return Verdict(True, "semantic", "PIN accepted")


def check_password(pw, username="") -> Verdict:
    if not DFA_PASSWORD.accepts(pw):
        return Verdict(False, "syntax", "policy: 8+ chars with lower, upper, digit, special")
    if username and username.lower() in pw.lower():
        return Verdict(False, "semantic", "password contains the username")
    if pw in COMMON_PASSWORDS:
        return Verdict(False, "semantic", "password appears in a common-password list")
    return Verdict(True, "semantic", "password accepted")


def check_email(addr) -> Verdict:
    if not DFA_EMAIL.accepts(addr):
        return Verdict(False, "syntax", "not a well-formed address")
    if addr.rsplit("@", 1)[1].lower() in DISPOSABLE_DOMAINS:
        return Verdict(False, "semantic", "disposable e-mail domain not allowed")
    return Verdict(True, "semantic", "format OK (deliverability still needs a confirmation mail)")
