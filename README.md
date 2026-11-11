# Formal Language & Automata – CLA-2 (Tasks 2 & 3)

![CI](../../actions/workflows/ci.yml/badge.svg)

**SRM Institute of Science and Technology, Tiruchirappalli · B.Tech AIML, Sem V · 21CSC301T**
Continuous Learning Assessment 2 · SDG 9 (Industry, Innovation and Infrastructure) · Design Alignment

| | |
|---|---|
| **Student** | **B S Rithik Harihar – RA2411026050052 – Section: [add your section]** |
| **Faculty** | Dr. C. Gunasundari (AP) |

Executable, tested implementations of the two term-work assignments:

| Task | Topic | Deadline | Folder |
|---|---|---|---|
| **2** | Finite automata for real-time validation (ATM PIN, password, e-mail) | 25.09.2026 | [`task2_finite_automata/`](task2_finite_automata/README.md) |
| **3** | PDA / CFG case studies (brackets, palindromes, arithmetic, aⁿbⁿ) | 26.10.2026 | [`task3_pda_cfg/`](task3_pda_cfg/README.md) |

Each folder's `README.md` is the **design note / case-study report** (diagrams, formal definitions, transitions, derivations, test tables, limitations).

## Quick start
```bash
git clone <your-repo-url> && cd fla-cla2-automata
python -m venv .venv && source .venv/bin/activate     # optional
pip install -r requirements.txt                       # only pytest
python run_demo.py                                    # 5-minute demonstration output
python -m pytest -v                                   # 17 tests
python make_diagrams.py                               # Mermaid + Graphviz diagrams -> docs/diagrams/
```
Python ≥ 3.9, no third-party runtime dependencies. PNG/SVG rendering needs Graphviz (`dot`) but is optional.

## Repository layout
```
fla/                     reusable library: DFA, CFG (derivations, parse trees, ambiguity), PDA simulator, CFG→PDA
task2_finite_automata/   pin.py · password.py · email_validator.py · semantic_layer.py · README (design note)
task3_pda_cfg/           balanced.py · palindrome.py · arithmetic.py · anbn.py · README (case-study report)
tests/                   test_task2.py · test_task3.py  (exhaustive / fuzz cross-checks)
docs/diagrams/           generated .mmd (Mermaid), .dot, .png/.svg
run_demo.py              console demonstration (traces, derivations, stack moves)
```

## How correctness is validated
* **Task 2** – every DFA is compared with an independent regular expression on 20 000 random strings, plus fixed accepted/rejected lists (≥ 5 each) and state-minimisation counts.
* **Task 3** – CFG, PDA and a reference recogniser are compared on **all** strings up to length 8; ambiguity is *computed* (counting leftmost derivations), grammar equivalence checked up to bounded length, and determinism tested structurally.
* Bounded checks are evidence, not proofs; the proofs (pumping-lemma argument, grammar structure) are in the task READMEs.

## Publish to GitHub
```bash
git init && git add . && git commit -m "CLA-2 Tasks 2 & 3: automata, CFG/PDA, tests"
git branch -M main
git remote add origin https://github.com/<username>/fla-cla2-automata.git
git push -u origin main
```
Mermaid diagrams in the READMEs render automatically on GitHub.

## Academic integrity
The brief requires individual work with plagiarism < 15 %. Treat this repo as a reference build: **replace the placeholder details, re-derive the diagrams and explanations in your own words, and be ready to explain every transition in the viva.** Cite any external sources you add (e.g. Hopcroft–Ullman, Sipser).

## License
MIT – see [LICENSE](LICENSE).
