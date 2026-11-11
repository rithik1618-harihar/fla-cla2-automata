"""Generate Mermaid (.mmd) and Graphviz (.dot) diagrams into docs/diagrams/."""
import pathlib
from task2_finite_automata import pin, password, email_validator
from task3_pda_cfg import balanced, palindrome, anbn

OUT = pathlib.Path(__file__).parent / "docs" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

dfas = {"pin_dfa": pin.DFA_PIN, "email_dfa": email_validator.DFA_EMAIL,
        "password_dfa": password.DFA_PASSWORD}
pdas = {"balanced_dpda": balanced.DPDA, "palindrome_npda": palindrome.NPDA,
        "marked_palindrome_dpda": palindrome.MARKED_DPDA, "anbn_dpda": anbn.DPDA}

for name, d in dfas.items():
    (OUT / f"{name}.dot").write_text(d.to_dot() + "\n", encoding="utf-8")
    if name != "password_dfa":        # ~50 states: too big for a readable Mermaid chart
        (OUT / f"{name}.mmd").write_text(d.to_mermaid() + "\n", encoding="utf-8")
for name, p in pdas.items():
    (OUT / f"{name}.mmd").write_text(p.to_mermaid() + "\n", encoding="utf-8")
print("diagrams written to", OUT)

# Optional: render PNGs when Graphviz ('dot') is installed.
import shutil, subprocess
if shutil.which("dot"):
    for dot in OUT.glob("*.dot"):
        fmt = "svg" if dot.stem == "password_dfa" else "png"     # ~100 states: SVG stays small & zoomable
        subprocess.run(["dot", f"-T{fmt}", "-Gdpi=130", str(dot), "-o", str(dot.with_suffix("." + fmt))], check=True)
    print("PNG/SVG renders written (Graphviz found)")
