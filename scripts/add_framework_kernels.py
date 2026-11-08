#!/usr/bin/env python3
"""The framework kernel on holographickernel.org: a "Framework Kernels" section beside "Archive Kernels", its references, a noscript line and
an llms.txt section. 2026-11-08, at the author's word: "framework hk should go to hk and restoredacademy"; on the proposal for the site pages,
"adopted for all three". The specification EA-HK-FRAME-01 (Alexanarch #1753, Sen Kuro and Rex Fraction) and its first instance, the hologram of
Socrates as Orthonym (#1754), both at v1.1. Idempotent: a second run changes nothing."""
import pathlib
R = pathlib.Path(__file__).resolve().parents[1]
A = "https://www.alexanarch.org"
SPEC = ("#1753", "AXN:0C54.OPERATIVE.☿☿⚙️🀄🍃🛸"); HOLO = ("#1754", "AXN:0C55.MPAI.🌠🎆💚➕🏷️🖊️")
MARK = "<!-- FRAMEWORK-KERNELS -->"
sec = f'''{MARK}
<div class="section">
<h2>Framework Kernels</h2>
<div class="example">
<div class="example-label">Field-Level · Specification · EA-HK-FRAME-01 v1.1</div>
<strong>The Framework Holographic Kernel.</strong> Sen Kuro and Rex Fraction specify the kernel at a framework's grain: a small package, written from the archive's registries by its own builder and tested by its own verifier, from which a framework's identity, positions, dated development, evidence bodies, claim states, failures, rival and open questions can be rebuilt and checked against the records. A claim is a pointer to a quotation bound to its record's hash; a correction is kept as the original, the correction and the withdrawal; an introduction is dated from the record's first seating in git; the rival framework is evaluated on the same bodies and rules, side by side in one ledger; each line of research states what result would advance or retreat the framework and what it moves. <a class="axn-chip" href="{A}/s/records/1753/">{SPEC[0]} &middot; {SPEC[1]}</a>
  </div>
<div class="example">
<div class="example-label">First Instance · The Hologram of Socrates as Orthonym · EA-HK-ORTHONYM-01 v1.1</div>
<strong>A map and a kernel in one record.</strong> Lee Sharks's framework (#123) held as a hologram: the framework map for a human reader, and the kernel attached as files: 40 records in six strata, 56 claims bound to quotations and hashes, 136 edges under a relation policy that licenses change on named dimensions only, two timelines, ten lines of research, seventeen structural tests. Back-Projection v1.0, the kernel alone given to models that had not seen the records: round 2 yields 1.0, 1.0, 1.0 and 0.909, a mean of 0.977 against the threshold of 0.85. <a class="axn-chip" href="{A}/s/records/1754/">{HOLO[0]} &middot; {HOLO[1]}</a> · <a class="axn-chip" href="{A}/files/AXN-0C55/kernel/">the kernel files</a> · <a class="axn-chip" href="https://huggingface.co/datasets/leesharks/mantle-bearing/tree/main/holograms/EA-HK-ORTHONYM-01">on Hugging Face</a> · <a class="axn-chip" href="https://www.restoredacademy.com/readings/socrates-as-orthonym">the reading</a>
  </div>
</div>
'''
p = R / "index.html"; s = p.read_text(encoding="utf-8")
if MARK not in s:
    a = "<!-- Links -->"; assert s.count(a) == 1
    s = s.replace(a, sec + a)
    a = '<div class="link-item"><span class="link-label">IB Bridge</span>'; assert s.count(a) == 1
    s = s.replace(a, f'<div class="link-item"><span class="link-label">Framework Kernel</span> <a class="axn-chip" href="{A}/s/records/1753/">EA-HK-FRAME-01 &middot; {SPEC[0]} &middot; {SPEC[1]}</a></div>\n'
                     f'<div class="link-item"><span class="link-label">First Instance</span> <a class="axn-chip" href="{A}/s/records/1754/">EA-HK-ORTHONYM-01 &middot; {HOLO[0]} &middot; {HOLO[1]}</a></div>\n' + a)
    a = "<p>Published by the Semantic Economy Institute."; assert s.count(a) == 1
    s = s.replace(a, "<p>Framework kernels: the specification EA-HK-FRAME-01 (Sen Kuro and Rex Fraction, Alexanarch #1753) builds the kernel at a framework's grain, with claims bound to quotations and hashes, corrections kept, introductions dated from first seating, the rival evaluated on the same evidence in one ledger, and lines of research; its first instance is the hologram of Socrates as Orthonym (#1754).</p>\n" + a)
    p.write_text(s, encoding="utf-8")
p = R / "llms.txt"; t = p.read_text(encoding="utf-8")
if "## Framework kernels" not in t:
    a = "## Glyphic checksums"; assert t.count(a) == 1
    t = t.replace(a, f"""## Framework kernels

The specification EA-HK-FRAME-01 v1.1 (Sen Kuro and Rex Fraction) builds the kernel at a framework's grain: a package written from the archive's registries by its own builder and tested by its own verifier, from which a framework's identity, positions, dated development, evidence bodies, claim states, failures, rival and open questions are rebuilt and checked against the records. Its first instance is the hologram of Socrates as Orthonym (Lee Sharks, #123): the framework map with its kernel attached.
{A}/s/records/1753/  EA-HK-FRAME-01 — The Framework Holographic Kernel ({SPEC[1]})
{A}/s/records/1754/  EA-HK-ORTHONYM-01 — Socrates as Orthonym, the framework hologram ({HOLO[1]})
https://www.restoredacademy.com/readings/socrates-as-orthonym  the hologram's map, rendered

""" + a)
    p.write_text(t, encoding="utf-8")
print("ok")
