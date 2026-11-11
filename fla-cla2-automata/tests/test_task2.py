import random
import pytest
from task2_finite_automata import pin, password, email_validator as email
from task2_finite_automata.semantic_layer import check_pin, check_password, check_email

MODULES = [(pin, pin.DFA_PIN), (password, password.DFA_PASSWORD), (email, email.DFA_EMAIL)]


@pytest.mark.parametrize("mod,dfa", MODULES)
def test_listed_cases(mod, dfa):
    assert len(mod.VALID) >= 5 and len(mod.INVALID) >= 5
    for s in mod.VALID:
        assert dfa.accepts(s), s
    for s in mod.INVALID:
        assert not dfa.accepts(s), s


@pytest.mark.parametrize("mod,dfa,alpha", [
    (pin, pin.DFA_PIN, "0123456789a -"),
    (password, password.DFA_PASSWORD, "aA1! é"),
    (email, email.DFA_EMAIL, "aZ9.-_@ !"),
])
def test_dfa_equals_regex_on_random_strings(mod, dfa, alpha):
    rng = random.Random(0)
    for _ in range(20000):
        s = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 14)))
        assert dfa.accepts(s) == bool(mod.REGEX.fullmatch(s)), repr(s)


def test_email_fuzz_with_realistic_tokens():
    rng = random.Random(1)
    parts = ["ab", "x1", "-", ".", "_", "@", "com", "in", "c", "9"]
    for _ in range(20000):
        s = "".join(rng.choice(parts) for _ in range(rng.randint(1, 9)))
        assert email.DFA_EMAIL.accepts(s) == bool(email.REGEX.fullmatch(s)), s


def test_state_counts():
    assert pin.DFA_PIN.minimal_state_count() == 8       # q0..q6 + dead
    assert len(email.DFA_EMAIL.reachable()) == 11        # hand-made design
    assert email.DFA_EMAIL.minimal_state_count() == 9    # P1~Qh and P2~Qd merge; +dead included
    assert password.DFA_PASSWORD.minimal_state_count() <= len(password.DFA_PASSWORD.reachable()) + 1


def test_syntax_vs_semantic_layers():
    assert check_pin("0000").stage == "semantic" and not check_pin("0000").ok
    assert check_pin("12a4").stage == "syntax"
    assert check_pin("4821", stored_pin="4821").ok
    assert not check_pin("4821", stored_pin="9999").ok
    assert not check_pin("4821", failed_attempts=3).ok
    assert check_password("Passw0rd!").ok
    assert not check_password("Alice9!xyz", username="alice").ok
    assert not check_email("x@mailinator.com").ok
    assert check_email("x@srmist.edu.in").ok
