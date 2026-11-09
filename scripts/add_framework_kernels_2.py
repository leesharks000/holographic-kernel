#!/usr/bin/env python3
"""Two more framework kernels on holographickernel.org, in the Framework Kernels section after the Socrates hologram: And the Last Shall Be First
(Revelation First, Damascus Dancings) and The Tenth Muse (Sappho and the future reader, Rebekah Cranes), each with its record, kernel files, Hugging Face
copy and the page that renders it at revelationfirst.com; two reference links, the noscript line and the llms.txt section extended. At the author's word
of 2026-11-08 23:59: "both to hk". Idempotent.   python3 scripts/add_framework_kernels_2.py <alexanarch root>"""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[1]; ARCH = pathlib.Path(sys.argv[1])
REG = {r["deposit_number"]: r for r in json.loads((ARCH / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
f = lambda start: next(n for n, r in REG.items() if r["title"].startswith(start))
RF = f("And the Last Shall Be First: Revelation First — The Framework Hologram"); TM = f("The Tenth Muse: Sappho and the Future Reader — The Framework Hologram")
def facts(n):
    K = ARCH / f"files/AXN-{REG[n]['hex']}/kernel"; G = json.loads((K / "02-graph.jsonld").read_text(encoding="utf-8")); V = json.loads((K / "10-verification.json").read_text(encoding="utf-8"))
    C = sum(1 for l in (K / "03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())
    recs = sum(1 for x in G["@graph"] if x.get("@type") in ("Record", "SurfaceRecord") and not x.get("external"))
    return recs, C, len(G["edges"]), sum(1 for v in V["structural_tests"].values() if v["pass"])
rr, rc, re_, rt = facts(RF); tr, tc, te, tt = facts(TM)
MARK = "<!-- FRAMEWORK-KERNELS-2 -->"
sec = f'''{MARK}
<div class="example">
<div class="example-label">Second Instance · And the Last Shall Be First · EA-HK-REVFIRST-01 v1.0</div>
<strong>Revelation First as a hologram.</strong> Damascus Dancings holds Lee Sharks's framework (#202), the Apocalypse of John as the first-composed book of the New Testament, with its three claims kept apart (absolute priority priced, corpus priority a finding about form, generative priority tested arrow by arrow) and its argument ladder as the kernel's dependency structure: six rungs with their fits and defeat conditions, the dependency of the Logos rung on the Josephus rung carried on the rungs and tested by propagation. {rr} records and site pages, {rc} claims bound to quotations and hashes, {re_} edges, {rt} structural tests; the received chronology weighed on the same five bodies in one ledger. <a class="axn-chip" href="{A}/s/records/{RF}/">#{RF} &middot; {REG[RF]['axn']}</a> · <a class="axn-chip" href="{A}/files/AXN-{REG[RF]['hex']}/kernel/">the kernel files</a> · <a class="axn-chip" href="https://huggingface.co/datasets/leesharks/mantle-bearing/tree/main/holograms/EA-HK-REVFIRST-01">on Hugging Face</a> · <a class="axn-chip" href="https://www.revelationfirst.com/and-the-last-shall-be-first/">the reading</a>
  </div>
<div class="example">
<div class="example-label">Third Instance · The Tenth Muse: Sappho and the Future Reader · EA-HK-TENTHMUSE-01 v1.0</div>
<strong>Sappho 31 as a hologram.</strong> Rebekah Cranes holds the framework (#1270) that reads fragment 31 as a written instrument of persistence: the two open positions, the three seats (Sappho in the third proposed by the author and held as a dated claim and a line of research), four evidence bodies in three rings, and the received reading, jealous and not the maker of her own persistence, weighed on the same bodies with its propositions kept apart. {tr} records, {tc} claims, {te} edges, {tt} structural tests; joined to Revelation First at rung VI. <a class="axn-chip" href="{A}/s/records/{TM}/">#{TM} &middot; {REG[TM]['axn']}</a> · <a class="axn-chip" href="{A}/files/AXN-{REG[TM]['hex']}/kernel/">the kernel files</a> · <a class="axn-chip" href="https://huggingface.co/datasets/leesharks/mantle-bearing/tree/main/holograms/EA-HK-TENTHMUSE-01">on Hugging Face</a> · <a class="axn-chip" href="https://www.revelationfirst.com/the-tenth-muse/">the reading</a>
  </div>
'''
p = R / "index.html"; s = p.read_text(encoding="utf-8")
if MARK not in s:
    a = "<!-- FRAMEWORK-KERNELS -->"; assert s.count(a) == 1
    i = s.index(a); j = s.index("\n</div>\n<!-- Links -->", i); s = s[:j] + "\n" + sec + s[j:]
    a = '<div class="link-item"><span class="link-label">IB Bridge</span>'; assert s.count(a) == 1
    s = s.replace(a, f'<div class="link-item"><span class="link-label">Second Instance</span> <a class="axn-chip" href="{A}/s/records/{RF}/">EA-HK-REVFIRST-01 &middot; #{RF} &middot; {REG[RF]["axn"]}</a></div>\n'
                     f'<div class="link-item"><span class="link-label">Third Instance</span> <a class="axn-chip" href="{A}/s/records/{TM}/">EA-HK-TENTHMUSE-01 &middot; #{TM} &middot; {REG[TM]["axn"]}</a></div>\n' + a)
    a = "its first instance is the hologram of Socrates as Orthonym (#1754).</p>"; assert s.count(a) == 1
    s = s.replace(a, f"its first instance is the hologram of Socrates as Orthonym (#1754); its second and third, And the Last Shall Be First (Revelation First, #{RF}) and The Tenth Muse (Sappho and the future reader, #{TM}).</p>")
    p.write_text(s, encoding="utf-8")
p = R / "llms.txt"; t = p.read_text(encoding="utf-8")
if "EA-HK-REVFIRST-01" not in t:
    a = "https://www.restoredacademy.com/readings/socrates-as-orthonym  the hologram's map, rendered\n"; assert t.count(a) == 1
    t = t.replace(a, a + f"{A}/s/records/{RF}/  EA-HK-REVFIRST-01 — And the Last Shall Be First: Revelation First, the framework hologram (Damascus Dancings; {REG[RF]['axn']})\n"
                         f"https://www.revelationfirst.com/and-the-last-shall-be-first/  its map, rendered\n"
                         f"{A}/s/records/{TM}/  EA-HK-TENTHMUSE-01 — The Tenth Muse: Sappho and the Future Reader, the framework hologram (Rebekah Cranes; {REG[TM]['axn']})\n"
                         f"https://www.revelationfirst.com/the-tenth-muse/  its map, rendered\n")
    p.write_text(t, encoding="utf-8")
print("ok", RF, TM)
