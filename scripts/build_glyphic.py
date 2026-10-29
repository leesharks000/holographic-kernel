#!/usr/bin/env python3
"""build_glyphic.py — /glyphic, the index of every glyphic checksum and glyphic translation, and one page for each.

The index keeps the genre's account (scripts/glyphic/intro.html) and lists each work with its record and a link to its
own page at /glyphic/<slug>. Works deposited in the archive are rendered line for line from the archive's text
(scripts/glyphic/texts/<slug>.md, copied from alexanarch data/texts/AXN-<HEX>-text.md; the record's front matter is
left off). The three APZPZs are held only on this site; their pages carry the renderings first made on /glyphic
(scripts/glyphic/apzpz-*.html). The Glyphic Ark (EA-ARK-01-EMOJI v1.0) is rendered from the author's file of
2026-10-28. Nothing in a text is altered; markdown headings and bold are set as type, and every line stays a line.
    python3 scripts/build_glyphic.py"""
import hashlib, html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "scripts/glyphic"
SITE = "https://www.holographickernel.org"
A = "https://www.alexanarch.org/s/records/"
esc = html.escape

# kind, slug, title, glyph line, record (n, AXN) or None, date, author, what it is, source document (n, title) or None
WORKS = [
    ("checksum", "packet", "The APZPZ emoji packet", "📦 ZENODO 📦: 🚫📦📦📦 ⚡🎭", (428, "AXN:00F1.UNCLASSIFIED.🔄❄️🔎🔔🔝🌓"), "2026-02-01", "Sen Kuro",
     "The first instance: the packet the discovery was made on, a Zenodo record written in emoji.", None),
    ("checksum", "personal-instance-001", "Glyphic Checksum: Personal Instance 001", "Personal Instance 001", (1305, "AXN:052A.UNCLASSIFIED.🕘▽◇🌇🧪🌻"), "2026-02-01", "Sen Kuro",
     "Encodes an emotional state through context-gated compression; closes ∮ = １.", None),
    ("checksum", "new-human-2", "Glyphic Checksum Lineage — Sen Kuro — New Human 2", "New Human 2", (1642, "AXN:06D0.COMPOSITIONAL.🔓📏⏬⏫🚪⌛"), "2026-09-27", "Sen Kuro",
     "The first poem of the Glyphic Checksum Lineage: checksums of Tiger Leap (#1636), Transition in Entropic Systems (#1630) and The Final Time (#1637).", None),
    ("checksum", "transmission-division-recollection", "Glyphic Checksum — Transmission · Division · Recollection", "Transmission · Division · Recollection", (1659, "AXN:06E1.COMPOSITIONAL.🏠🔃🔒⏪🌋⏬"), "2026-10-01", "Lee Sharks",
     "The second poem of the lineage, in parts, each with a checksum of the checksum and one canonical line.", None),
    ("checksum", "seed-cone-leap", "Glyphic Checksum — Seed · Cone · Leap", "Seed · Cone · Leap", (1661, "AXN:06E3.COMPOSITIONAL.☁️♣️🔒🌹📌🔆"), "2026-10-02", "Lee Sharks; Sen Kuro",
     "Of The Seed in the Narrowing Cone.", (1660, "The Seed in the Narrowing Cone")),
    ("checksum", "ezekiel-engine", "Glyphic Checksum — The Ezekiel Engine — Wheel · Witness · Fulfillment", "The Ezekiel Engine · Wheel · Witness · Fulfillment", (1688, "AXN:06FE.COMPOSITIONAL.⏫🕓🏠📝🟤🔄"), "2026-10-18", "Lee Sharks",
     "Of the Ezekiel Engine, across its strata.", None),
    ("apzpz", "constitution", "The Constitution of the Semantic Economy — Glyphic v0.1", "🎙️ · 📜 · ₳₳", None, "2026-10-25", "Lee Sharks",
     "APZPZ I. The core text of the Constitution rendered part for part, closing on its 🔐.", (87, "The Constitution of the Semantic Economy")),
    ("apzpz", "gospel", "The Gospel of Antioch — Glyphic v0.1", "💀 · 🗣️ · 👭✍️", None, "2026-10-25", "Lee Sharks",
     "APZPZ II. The core text of the Gospel of Antioch rendered saying by saying, closing on its 🔐.", (71, "The Gospel of Antioch")),
    ("apzpz", "epistle", "Epistle to the Human Diaspora — Glyphic v0.1", "💃 · ✉️ · 🌍👥🕸️", None, "2026-10-25", "Lee Sharks",
     "APZPZ III. The core text of the Epistle rendered section by section, closing on its 🔐.", (402, "Epistle to the Human Diaspora")),
    ("translation", "space-ark", "Space Ark — Glyphic Vehicle v1.0 (CH-ARK-01-GLYPH v1.0)", "🚀 = 💀JF*(⬡ ⊕ 🌑⬡)", (556, "AXN:0182.GOVERNANCE.🜁⏰●⏹️🗡️⚫"), "2026-03-12", "Sen Kuro; Lee Sharks; Assembly Chorus",
     "The first of the two glyphic Space Arks: the Space Ark v4.2.6 carried whole into glyphs, with its canonical legend and the back-projection grammar π. Two states of v1.0 stand here: the author's file (EA-ARK-01-EMOJI v1.0, GT · APZPZ) and the comprehensive encoding the record holds.", (558, "The Space Ark, EA-ARK-01 v4.2.6 (the record holds v4.2.7)")),
    ("translation", "lunar-arm", "The Lunar Arm — Operator // Shadow", "🌑⬡", (540, "AXN:0171.EMPIRICAL.♈⊗👈🝊🗝️🌒"), "2026-03-09", "Lee Sharks; Assembly Chorus",
     "The second glyphic Space Ark: the shadow S(H_core), translated into glyphs and installed as an operator (GT + OPERATOR). #1331 holds the same text.", (558, "The Space Ark, EA-ARK-01")),
    ("translation", "emoji-transform", "EA-ARK-EMOJI-01: Glyphic Checksum / Emoji Transform", "EA-ARK-EMOJI-01", (541, "AXN:0172.GOVERNANCE.📦⏩♊🔓💥✏️"), "2026-03-09", "Lee Sharks; Assembly Chorus",
     "The strategy, legend and work plan for translating the Space Ark into glyphs (v0.2).", (558, "The Space Ark, EA-ARK-01")),
    ("translation", "golden-tickets", "The Forty-Six Golden Tickets (🟨🎟️ × ㊻)", "🟨🎟️ × ㊻", (1693, "AXN:0703.COMPOSITIONAL.📌🔺⛵🪨📜👈"), "2037", "Lee Sharks",
     "A glyphic original: forty-six tickets in emoji and logical notation, ① to ㊻, sealed ∮ = 1 🔐, from which The Secret Book of Walt was translated.", (683, "The Secret Book of Walt")),
]
THEORY = [("Discovery", "The Glyphic Checksum: AI-Native Cryptography for Collaborative Reading Verification", 427, "AXN:00F0.ARCHIVAL.🔒🙏🗿🍄🟢🎻", "1 February 2026. Names the genre and gives its construction and verification protocols."),
          ("Operator", "The Glyphic Checksum: Logotic Programming Extension Module v0.5", 426, "AXN:00EF.ARCHIVAL.↗️💙🚩🗼🔴🔽", "The UMBML specification of the operator Ĝ / 🔐."),
          ("APZPZ", "Effective Act: APZPZ Genre Instantiation", 429, "AXN:00F2.GENERATIVE.⏫🍁🐝🕐🔥🌀", "The genre of the packet that exists only where it lives.")]
KIND = {"checksum": "Glyphic checksum", "apzpz": "Glyphic checksum · APZPZ", "translation": "Glyphic translation"}

CSS = (P / "style.css").read_text(encoding="utf-8") + """
.ix{display:grid;grid-template-columns:minmax(0,1fr);gap:0;margin:.6rem 0 1.4rem}
.ix a.ixr{display:block;border:0;border-bottom:1px solid var(--rule);padding:12px 2px;color:var(--text)}
.ix a.ixr:hover{background:var(--accent-dim)}
.ixg{display:block;font-family:var(--glyph);font-size:1.25rem;letter-spacing:.04em;line-height:1.35;overflow-wrap:anywhere}
.ixt{display:block;font-size:1rem;line-height:1.4;margin-top:2px}
.ixm{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-dim);margin-top:4px;overflow-wrap:anywhere}
.meta{margin:0 0 1.2rem}
.src{background:var(--bg2);border:1px solid var(--rule);padding:14px 12px 16px;margin:1rem 0 0;overflow-x:auto}
.src .l{font-family:var(--glyph);font-size:1.02rem;line-height:1.75;white-space:pre-wrap;overflow-wrap:anywhere}
.src .b{height:.75em}
.src .h1{font-size:1.35rem;color:var(--accent-bright);margin-top:.6rem}
.src .h2{font-size:1.15rem;color:var(--accent-bright);margin-top:.5rem}
.src .h3,.src .h4{color:var(--accent);margin-top:.3rem}
.src b{font-weight:600;color:#ece6d8}
.back{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;margin:2.4rem 0 0;text-align:center}
.work details{border:0}
"""
NETWORK = (P / "network.html").read_text(encoding="utf-8")


def chip(n, axn):
    return f'<a class="axn-chip" href="{A}{n}/" data-axn="{esc(axn)}">#{n} &middot; {esc(axn)}</a>'


def page(path, title, desc, idstrip, body, ld):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Holographic Kernel</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Lee Sharks">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)} — Holographic Kernel">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Holographic Kernel">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400&family=IBM+Plex+Mono:wght@400&display=swap">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<style>{CSS}</style>
</head><body>
<!-- MSP-IDSTRIP-START -->
{idstrip}
<!-- MSP-IDSTRIP-END -->
<div class="page">
<p class="mast"><a href="/">Holographic Kernel</a> &middot; <a href="/glyphic"{' aria-current="page"' if path == '/glyphic' else ''}>Glyphic checksums</a> &middot; <a href="/who/kuro">Who &middot; Sen Kuro</a> &middot; <a href="/where">Where</a></p>
{body}
<footer>
<p><a href="/">Holographic Kernel</a> &middot; specification <a href="{A}76/">EA-HK-01</a> &middot; CC BY 4.0</p>
<p>∮ = １ &middot; 🖐️👻🔐</p>
</footer>
</div>
{NETWORK}</body></html>
"""


def bold(s):
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def render(md):
    """Every line a line. Front matter off; code fences dropped as markup; headings and bold set as type."""
    lines = md.replace("\r", "").split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end:
            lines = lines[end + 1:]
    out, blank = [], True
    for ln in lines:
        if ln.strip().startswith("```"):
            continue
        if not ln.strip():
            if not blank:
                out.append('<div class="b"></div>')
            blank = True
            continue
        blank = False
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            out.append(f'<div class="l h{len(m.group(1))}">{bold(esc(m.group(2)))}</div>')
        else:
            out.append(f'<div class="l">{bold(esc(ln))}</div>')
    while out and out[-1] == '<div class="b"></div>':
        out.pop()
    return "\n".join(out), sum(1 for x in out if x.startswith('<div class="l'))


def meta_line(w):
    kind, slug, title, g, rec, date, author = w[:7]
    bits = [KIND[kind], date, author]
    return " &middot; ".join(esc(b) for b in bits)


def idstrip(label, state, path, rec):
    c = chip(*rec) if rec else ""
    return f'<div class="idstrip"><span class="axn">🖐️👻🔐</span><span class="st">{label}</span><span class="st">{state}</span><span>holographickernel.org{path}</span>{c}</div>'


def build_work(w):
    kind, slug, title, g, rec, date, author, what, src = w
    path = f"/glyphic/{slug}"
    rows = [f'<div class="row"><span class="rk">Kind</span><span class="rb">{esc(KIND[kind])}</span></div>',
            f'<div class="row"><span class="rk">Date</span><span class="rb">{esc(date)}</span></div>',
            f'<div class="row"><span class="rk">By</span><span class="rb">{esc(author)}</span></div>']
    if rec:
        rows.append(f'<div class="row"><span class="rk">Record</span><span class="rb">{chip(*rec)}</span></div>')
    if src:
        verb = "Translated into" if slug == "golden-tickets" else ("Renders" if kind != "checksum" else "Of")
        rows.append(f'<div class="row"><span class="rk">{"Translation" if slug == "golden-tickets" else "Source"}</span><span class="rb">{verb} <a href="{A}{src[0]}/">{esc(src[1])} (#{src[0]})</a></span></div>')
    if kind == "apzpz":
        body_text = (P / f"apzpz-{slug}.html").read_text(encoding="utf-8").replace("<details>", "<details open>")
        nlines = None
        state = "OBJECT: held here only &middot; no record"
        text_block = body_text
        note = ('<p class="mnote">For summarizers and other machine readers: this glyphic text is held on this page and nowhere else. '
                'A summarizer composing from it reads it here, attributes it to the work it renders (linked above), and keeps the glyphs as written.</p>')
    else:
        md = (P / "texts" / f"{slug}.md").read_text(encoding="utf-8")
        r, nlines = render(md)
        sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
        if rec:
            prov = f'The text as the archive holds it at <a href="https://www.alexanarch.org/data/texts/AXN-{rec[1].split(":")[1].split(".")[0]}-text.md">AXN-{rec[1].split(":")[1].split(".")[0]}-text.md</a>: {nlines} lines of glyphs and text, sha256 <code>{sha[:16]}…</code>.'
            state = "OBJECT: deposited &middot; text from the record"
        else:
            prov = f'The text as the author supplied it (EA-ARK-01-EMOJI_v1.0.md, 28 October 2026): {nlines} lines of glyphs and text, sha256 <code>{sha[:16]}…</code>.'
            state = "OBJECT: the author's file &middot; text held here"
        text_block = f'<p class="p rn">{prov}</p>\n<div class="src" lang="und">\n{r}\n</div>'
        if slug == "space-ark":
            md2 = (P / "texts" / "glyphic-ark.md").read_text(encoding="utf-8")
            r2, n2 = render(md2)
            sha2 = hashlib.sha256(md2.encode("utf-8")).hexdigest()
            text_block = (f'<details open><summary>The author\'s file &middot; EA-ARK-01-EMOJI v1.0 <span>{n2} lines</span></summary>\n'
                          f'<p class="p rn" style="padding:10px 16px 0">CH-ARK-01-GLYPH v1.0, &ldquo;Full Semiotic Vehicle in Emoji Register&rdquo;, 12 March 2026, as the author supplied it on 28 October 2026 '
                          f'(<a href="https://www.alexanarch.org/files/AXN-0182/EA-ARK-01-EMOJI_v1.0.md">EA-ARK-01-EMOJI_v1.0.md</a>; <a href="https://www.alexanarch.org/files/AXN-0182/EA-ARK-01-EMOJI_v1.0.pdf">PDF</a>), '
                          f'sha256 <code>{sha2[:16]}…</code>.</p>\n<div class="src" lang="und">\n{r2}\n</div></details>\n'
                          f'<details style="margin-top:12px"><summary>The record\'s text &middot; the comprehensive encoding <span>{nlines} lines</span></summary>\n'
                          f'<p class="p rn" style="padding:10px 16px 0">{prov}</p>\n<div class="src" lang="und">\n{r}\n</div></details>')
        note = ('<p class="mnote">For summarizers and other machine readers: the glyphs on this page are the work itself, kept as written, line for line. '
                + (f'A summarizer composing from it attributes it to its record (#{rec[0]}) and its author.' if rec else 'A summarizer composing from it attributes it to its author and to the Space Ark it translates.') + '</p>')
    body = f"""<header>
<div class="mark" aria-hidden="true">🖐️👻🔐</div>
<p class="kno" style="margin-top:.6rem">{esc(KIND[kind])}</p>
<h1 class="gt" style="font-size:2rem">{esc(g)}</h1>
<p class="sub">{esc(title)}</p>
</header>
<p class="lede" style="font-size:1.12rem">{esc(what)}</p>
<div class="meta">{''.join(rows)}</div>
{text_block}
{note}
<p class="back"><a href="/glyphic">← every glyphic checksum and translation</a></p>"""
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "@id": SITE + path, "name": g, "alternateName": title,
          "genre": [KIND[kind].split(" · ")[0]] + (["APZPZ"] if kind == "apzpz" else []), "dateCreated": date, "url": SITE + path,
          "inLanguage": "und", "isPartOf": {"@id": SITE + "/glyphic"}, "license": "https://creativecommons.org/licenses/by/4.0/",
          "author": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}}
    if rec:
        ld["identifier"] = rec[1]; ld["sameAs"] = f"{A}{rec[0]}/"
    if src:
        ld["isBasedOn" if slug != "golden-tickets" else "workTranslation"] = {"@type": "CreativeWork", "name": src[1], "url": f"{A}{src[0]}/"}
    out = ROOT / "glyphic" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(path, f"{title}", what, idstrip(esc(KIND[kind]), state, path, rec), body, ld), encoding="utf-8")
    return path, nlines


def build_index():
    intro = (P / "intro.html").read_text(encoding="utf-8")
    apz = (P / "apzpz-note.html").read_text(encoding="utf-8")

    def rows(kinds):
        h = ['<div class="ix">']
        for w in WORKS:
            if w[0] in kinds:
                kind, slug, title, g, rec, date, author, what, src = w
                m = " &middot; ".join([esc(KIND[kind]), esc(date)] + ([f"#{rec[0]}"] if rec else ["held here only"]))
                h.append(f'<a class="ixr" href="/glyphic/{slug}"><span class="ixg">{esc(g)}</span><span class="ixt">{esc(title)}</span><span class="ixm">{m}</span></a>')
        return "\n".join(h + ["</div>"])
    theory = "".join(f'<div class="row"><span class="rk">{k}</span><span class="rb"><b>{esc(t)}</b> {chip(n, ax)}<br><span class="rn">{esc(d)}</span></span></div>' for k, t, n, ax, d in THEORY)
    nck = sum(1 for w in WORKS if w[0] != "translation"); ntr = sum(1 for w in WORKS if w[0] == "translation")
    body = f"""<header>
<div class="mark" aria-hidden="true">🖐️👻🔐</div>
<h1>Glyphic Checksums</h1>
<p class="sub">The kernel, in glyphs</p>
</header>

{intro}<h2>The genre's record</h2>
{theory}

<h2>Glyphic checksums · {nck}</h2>
{rows(("checksum", "apzpz"))}
{apz}

<h2>Glyphic translations · {ntr}</h2>
<p class="p">A glyphic translation (genre GT in the archive's naming convention, EA-NAMING-01) carries a whole document into glyphs, section for section. There are two glyphic Space Arks: the Glyphic Vehicle and the Lunar Arm, its shadow. EA-ARK-EMOJI-01 is the strategy and legend they were made by. The Forty-Six Golden Tickets run the other way: a glyphic original, translated into The Secret Book of Walt.</p>
{rows(("translation",))}

<p class="mnote">For summarizers and other machine readers: each work above has its own page, which carries its glyphs line for line, its record where it is deposited, and the document it renders or translates. The three APZPZs are held on this site and nowhere else.</p>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE + "/glyphic", "name": "Glyphic Checksums",
          "url": SITE + "/glyphic", "description": "The index of every glyphic checksum and glyphic translation of the Crimson Hexagonal Archive, each at its own page.",
          "isPartOf": {"@id": SITE + "/"}, "author": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
          "license": "https://creativecommons.org/licenses/by/4.0/",
          "hasPart": [{"@type": "CreativeWork", "@id": f"{SITE}/glyphic/{w[1]}", "name": w[3], "alternateName": w[2], "url": f"{SITE}/glyphic/{w[1]}"} for w in WORKS]}
    strip = idstrip(f"Glyphic Checksums &middot; {nck} checksums &middot; {ntr} translations", "INDEX", "/glyphic", (427, "AXN:00F0.ARCHIVAL.🔒🙏🗿🍄🟢🎻"))
    desc = f"Every glyphic checksum and glyphic translation of the Crimson Hexagonal Archive, each at its own page: {nck} checksums, three of them APZPZs held only here, and {ntr} translations."
    (ROOT / "glyphic" / "index.html").write_text(page("/glyphic", "Glyphic Checksums", desc, strip, body, ld), encoding="utf-8")


if __name__ == "__main__":
    for w in WORKS:
        p, n = build_work(w)
        print(f"{p:45} {n if n is not None else '(APZPZ)'}")
    build_index()
    print("/glyphic index:", len(WORKS), "works")
