[README.md](https://github.com/user-attachments/files/34696451/README.md)
<div align="center">

# Formal Language & Automata
### CLA-2 · Assessment Tasks 2 & 3

**Finite Automata for Real-Time Validation · Pushdown Automata & Context-Free Grammars**

B.Tech. Computer Science and Engineering — Artificial Intelligence & Machine Learning  
**SRM Institute of Science and Technology, Tiruchirappalli**

<br>

| Student | Faculty |
|:--|:--|
| **B S Rithik Harihar** | Dr. C. Gunasundari |
| RA2411026050052 | Assistant Professor, Department of AIML |
| III Year · V Semester · Section: *[Add section]* |  |

</div>

---

## Project overview

This project explores how automata theory can be applied to everyday input validation and language parsing. It contains three finite-automata validators for **Task 2**, followed by four grammar and pushdown-automaton case studies for **Task 3**.

| # | Application / case study | Model | What it demonstrates |
|:--:|---|---|---|
| 1 | ATM PIN verification | DFA | Fixed-length numeric input |
| 2 | Password policy | Product DFA | Length and character-class requirements |
| 3 | E-mail address format | DFA | Structured local-part and domain validation |
| 4 | Balanced brackets | CFG + DPDA | Nested matching using a stack |
| 5 | Palindrome recognition | CFG + NPDA | Guessing and comparing the two halves |
| 6 | Arithmetic expressions | CFG + PDA | Grammar ambiguity and operator precedence |
| 7 | \(a^n b^n\) | CFG + DPDA | Unbounded equal-count matching |

The Python implementation includes reusable DFA, CFG and PDA components, demonstration scripts, diagrams and automated validation tests.

---

# Task 2 · Finite Automata for Real-Time Validation

Finite automata are useful when an input rule can be checked by tracking a limited amount of information while reading a string from left to right. The validators below focus on the **format** of an input; external checks such as account ownership or mailbox existence belong to a separate semantic layer.

## 1 · ATM PIN verification

**Rule:** accept a PIN containing exactly four or six ASCII digits.

- **Alphabet:** \(\Sigma = \{0,1,\ldots,9\}\)
- **Language:** \(L_{PIN} = \{w \in \Sigma^* : |w| \in \{4,6\}\}\)
- **Accepting states:** \(q_4\) and \(q_6\)
- **Rejection:** a non-digit or a PIN with any other length.

The states \(q_0\) through \(q_6\) represent how many digits have been read. A non-digit or an extra digit after the sixth position leads to a rejecting trap state.

**DFA diagram:** [View PIN DFA](documentation/diagrams/pin_dfa.png)

| Accepted examples | Rejected examples |
|---|---|
| `1234`, `0000`, `4821`, `987654`, `000007` | `123`, `12345`, `1234567`, `12a4`, `12 34`, `-123` |

A correctly formatted PIN is not necessarily the correct PIN for a particular account. Comparing it with stored authentication data is a semantic operation.

## 2 · Password policy validation

**Policy:** at least eight printable ASCII characters, with at least one lowercase letter, one uppercase letter, one digit and one special character. Spaces and unsupported non-ASCII characters are rejected.

- **Character classes:** `lower`, `upper`, `digit`, `special`
- **Language:** strings of length at least eight containing all four required classes.
- **Construction:** a product automaton combines four class-presence flags with a length counter that saturates at eight.

The machine accepts only when the minimum length has been reached and every required character class has appeared.

**DFA diagram:** [View password DFA](documentation/diagrams/password_dfa.svg)

| Accepted examples | Rejected examples |
|---|---|
| `Passw0rd!`, `Abcdef1@x`, `Zz9#Zz9#`, `correct-Horse-9-battery` | `password`, `PASSWORD1!`, `Pass1!`, `Password!!`, `Passw0rd12` |

The DFA checks the stated composition policy. It does not check breached-password databases, password reuse or whether a password contains personal information.

## 3 · E-mail address format

The e-mail validator recognises a practical subset of common e-mail syntax rather than every form allowed by the full e-mail standard.

```text
local  = alnum+ ( [._-] alnum+ )*
domain = label ( "." label )*
label  = alnum+ ( "-"+ alnum+ )*
tld    = letter{2,}
```

- The local part contains alphanumeric groups with optional single separators.
- The domain contains dot-separated labels.
- The final top-level domain contains at least two letters.
- Leading, trailing or repeated local-part separators are rejected.

**DFA diagram:** [View e-mail DFA](documentation/diagrams/email_dfa.png)

| Accepted examples | Rejected examples |
|---|---|
| `user@example.com`, `first.last@mail.srmist.edu.in`, `a_b-c@x1.org`, `A@b.co` | `user@example`, `user@.com`, `@example.com`, `user..name@example.com`, `user@example.c`, `user@@gmail.com` |

The format check cannot establish that a domain has a mail server or that a mailbox exists. Those checks require DNS queries or an e-mail confirmation process.

## Syntax and semantics

| Application | Syntactic check handled by the automaton | Additional semantic / business check |
|---|---|---|
| ATM PIN | Four or six digits | Compare with the account's stored PIN; enforce attempt limits |
| Password | Length and required character classes | Check breached-password lists and password reuse |
| E-mail | Simplified `local@domain` structure | DNS/MX lookup and mailbox ownership verification |

### Design limitations

- The e-mail grammar is a practical subset, not a complete implementation of every valid e-mail address.
- The validators deliberately use ASCII character classes.
- DFAs validate input structure, not external facts or ownership.
- Combining many independent password rules can increase the number of DFA states.

---

# Task 3 · Case Studies with PDA and CFG

A Pushdown Automaton extends finite-state control with a stack. This additional memory is useful for nested structures, matching symbols and languages that require unbounded counting.

## 4 · Balanced brackets

**Target language:** strings over `{ (, ), [, ] }` in which every opening bracket is closed by the matching type in the correct order. The empty string is accepted.

An ambiguous first attempt is:

```text
B → BB | (B) | [B] | () | []
```

The production `B → BB` permits different groupings of the same concatenated string. A revised grammar is:

```text
S → (S)S | [S]S | ε
```

The PDA pushes each opening bracket onto the stack. A closing bracket pops only the matching opener. A mismatch or an attempt to pop an empty stack causes rejection. The input is accepted when all brackets have been matched.

**Diagram:** [Balanced-bracket PDA](documentation/diagrams/balanced_dpda.mmd)

| Accepted examples | Rejected examples |
|---|---|
| `ε`, `()`, `[]`, `([])`, `()[]()`, `[([])]()` | `(`, `)`, `(]`, `([)]`, `())(`, `((]` |

## 5 · Palindrome recognition

A palindrome reads the same from left to right and right to left. Over the alphabet `{a,b}`, the grammar is:

```text
P → aPa | bPb | a | b | ε
```

For example:

```text
P ⇒ aPa ⇒ abPba ⇒ abba
```

The NPDA pushes the first half of the input onto the stack, guesses the middle, and then compares the remaining symbols with the stack contents. Since an unmarked input does not identify its own midpoint, the machine is nondeterministic.

A marked palindrome of the form `w c wᴿ` has an explicit centre marker. That marker identifies when the machine should switch from pushing to popping, allowing a deterministic construction.

**Diagram:** [Palindrome NPDA](documentation/diagrams/palindrome_npda.mmd) · [Marked palindrome DPDA](documentation/diagrams/marked_palindrome_dpda.mmd)

| Accepted examples | Rejected examples |
|---|---|
| `ε`, `a`, `aa`, `aba`, `abba`, `baab`, `ababa` | `ab`, `aab`, `abb`, `abab`, `baa` |

## 6 · Arithmetic-expression parsing

The initial grammar

```text
E → E + E | E * E | (E) | id
```

is ambiguous. For example, `id + id * id` can be parsed as either:

```text
id + (id * id)
(id + id) * id
```

If the identifiers represent 2, 3 and 4, the two interpretations evaluate to 14 and 20. The grammar therefore needs to encode operator precedence.

The revised grammar separates expressions, terms and factors:

```text
E → E + T | T
T → T * F | F
F → (E) | id
```

Multiplication is handled at the term level and therefore has higher precedence than addition. The project also demonstrates grammar-to-PDA construction and explains why practical compilers use parsing strategies such as LL or LR.

**Case-study implementation:** `implementation/task3_pda_cfg/arithmetic.py`

| Accepted examples | Rejected examples |
|---|---|
| `id`, `id+id`, `id*id`, `id+id*id`, `(id+id)*id`, `((id))` | `ε`, `id+`, `+id`, `(id`, `id id`, `id+*id` |

## 7 · The language \(a^n b^n\)

The language contains an equal number of `a` symbols followed by `b` symbols:

\[
L = \{a^n b^n : n \geq 0\}
\]

Its grammar is:

```text
S → aSb | ε
```

The DPDA pushes one marker for every `a`. When the `b` phase begins, it pops one marker for every `b`. It rejects if the order is broken, if too many `b` symbols are read, or if unmatched markers remain at the end.

**Diagram:** [DPDA for aⁿbⁿ](documentation/diagrams/anbn_dpda.mmd)

| Accepted examples | Rejected examples |
|---|---|
| `ε`, `ab`, `aabb`, `aaabbb` | `a`, `b`, `ba`, `aab`, `abb`, `abab` |

This language is not regular. A finite automaton cannot store an unbounded count of the `a` symbols and compare it with the number of `b` symbols. The PDA stack provides the required memory.

## Case-study comparison

| Case study | Grammar / key idea | PDA behaviour |
|---|---|---|
| Balanced brackets | Revised grammar removes the ambiguous concatenation structure | Deterministic matching with a stack |
| Palindromes | Recursive grammar mirrors symbols around the centre | Nondeterministic midpoint guess |
| Marked palindrome | Centre marker identifies the midpoint | Deterministic push and pop |
| Arithmetic expressions | Expression/term/factor levels encode precedence | CFG-to-PDA construction |
| \(a^n b^n\) | `S → aSb \| ε` generates equal counts | Deterministic stack counting |

---

## Project structure

```text
documentation/
  diagrams/                 Automata diagrams and visual references

implementation/
  core/fla/                 Reusable DFA, CFG and PDA classes
  task2_finite_automata/    PIN, password and e-mail validators
  task3_pda_cfg/            Four CFG/PDA case studies

validation/                 Automated test suite
utilities/                  Demo and diagram-generation scripts

README.md                   Project overview
requirements.txt            Python dependencies
LICENSE                     MIT license
```

## Run the project

Run these commands from the repository root.

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run the demonstration
python utilities/run_demo.py

# Run the automated tests
python -m pytest validation -v

# Regenerate project diagrams
python utilities/make_diagrams.py
```

## Validation notes

The test suite exercises the Task 2 validators with accepted and rejected inputs and checks the Task 3 grammar and PDA case studies against reference recognisers over bounded input lengths. These tests help identify implementation errors, but bounded testing is not a mathematical proof of correctness for every possible string.

## Submission details

- **Student:** B S Rithik Harihar
- **Register number:** RA2411026050052
- **Course:** 21CSC301T – Formal Language and Automata
- **Assessment:** CLA-2 – Tasks 2 and 3
- **Faculty:** Dr. C. Gunasundari
- **Section:** Add your section before submission

