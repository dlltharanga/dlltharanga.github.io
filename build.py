#!/usr/bin/env python3
"""Build website (index.html) and LinkedIn copy (linkedin.md) from resume.json.

Usage:  python build.py            -> writes dist/index.html, dist/linkedin.md
No third-party dependencies.
"""
import json, html, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"
DIST = ROOT / "dist"
d = json.loads((ROOT / "resume.json").read_text(encoding="utf-8"))
b, s = d["basics"], d["x-site"]
e = html.escape
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fmt(date):
    if not date:
        return "Present"
    p = date.split("-")
    return f"{MONTHS[int(p[1]) - 1]} {p[0]}" if len(p) > 1 else p[0]


def profile(net):
    return next((p["url"] for p in b["profiles"] if p["network"] == net), "#")


def tags(items):
    return "".join(f'<span class="tag">{e(t)}</span>' for t in items)


# ---------- group consecutive roles at the same company for the site timeline
groups = []
for w in d["work"]:
    if groups and groups[-1]["name"] == w["name"]:
        groups[-1]["roles"].append(w)
    else:
        groups.append({"name": w["name"], "roles": [w]})


def job_html(g):
    roles = g["roles"]
    first, last = roles[-1], roles[0]
    title = last["position"] if len(roles) == 1 else f'{first["position"]} → {last["position"]}'
    hl = [h for r in roles for h in r.get("highlights", [])][:4]
    clients = last.get("x-clients")
    if clients:
        hl = [f'{c["name"]} ({c["status"]}): {c["description"]}' for c in clients] + hl[:2]
    tech = list(dict.fromkeys(t for r in roles for t in r.get("x-tech", [])))[:7]
    lis = "".join(f"<li>{e(h)}</li>" for h in hl)
    return f'''<div class="job rv"><div class="top"><div><h3>{e(title)}</h3><div class="co">{e(g["name"])} · {e(last.get("location", ""))}</div></div><div class="when">{fmt(first.get("startDate"))} — {fmt(last.get("endDate"))}</div></div><ul>{lis}</ul><div class="tags">{tags(tech)}</div></div>'''


def site():
    li, gh = profile("LinkedIn"), profile("GitHub")
    pub = d.get("publications", [{}])[0]
    stats = "".join(f'<div class="stat"><b>{e(a)}</b><span>{e(c)}</span></div>' for a, c in s["stats"])
    about = "".join(f"<p>{p}</p>" for p in s["about"])
    pillars = "".join(f'<div class="pillar"><div class="ic">{e(i)}</div><div><h4>{e(t)}</h4><p>{e(x)}</p></div></div>' for i, t, x in s["pillars"])
    jobs = "".join(job_html(g) for g in groups)
    skills = "".join(f'<div class="sk rv"><h4>{e(k["name"])}</h4><div class="tags">{tags(k["keywords"][:8])}</div></div>' for k in d["skills"])
    edu = "".join(f'<div class="ed rv"><h4>{e(x["studyType"])} {e(x["area"])}</h4><div class="co">{e(x["institution"])}</div><p>{fmt(x.get("startDate"))} – {fmt(x.get("endDate"))}{" · " + e(x["score"]) if x.get("score") else ""}</p></div>' for x in d["education"][:3])
    ref = d.get("references", [{}])[0]
    desc = f'{b["label"]}. {b["summary"][:160]}'
    css = (SITE / "style.css").read_text(encoding="utf-8")
    js = (SITE / "main.js").read_text(encoding="utf-8")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(b["displayName"])} | {e(b["label"].split("|")[0].strip())}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(b["displayName"])} | {e(b["label"])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{e(b["url"])}/">
<meta property="og:image" content="{e(b["url"])}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%230a1b33'/><text x='50%25' y='56%25' font-family='monospace' font-size='26' font-weight='700' fill='%233fd0ff' text-anchor='middle' dominant-baseline='middle'>LT</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{css}</style></head><body>
<nav><div class="wrap"><a href="#" class="logo">&lt;lahiru<span>.tharanga</span> /&gt;</a><div class="links"><a href="#about">About</a><a href="#experience">Experience</a><a href="#skills">Skills</a><a href="#handbook">Handbook</a><a href="#contact">Contact</a></div></div></nav>
<header class="hero"><div class="wrap"><div>
<div class="eyebrow">&lt;/&gt; {e(s["eyebrow"])}</div>
<h1>{e(s["heroTitle"])} <span class="g">{e(s["heroHighlight"])}</span></h1>
<p class="lead">{e(s["heroLead"])}</p>
<div class="cta"><a class="btn p" href="{li}" target="_blank" rel="noopener">Connect on LinkedIn →</a><a class="btn s" href="#handbook">AI-103 Handbook</a></div></div>
<div class="code rv" aria-hidden="true"><div class="bar"><i></i><i></i><i></i></div>
<pre><span class="k">public sealed class</span> <span class="t">Engineer</span>
{{
  <span class="k">public</span> <span class="t">string</span> Name =&gt; <span class="s">"{e(b["displayName"])}"</span>;
  <span class="k">public</span> <span class="t">string</span> Next =&gt; <span class="s">"Software Architect"</span>;

  <span class="k">public</span> <span class="t">Stack</span> Stack =&gt; <span class="k">new</span>(
    <span class="s">".NET 10"</span>, <span class="s">"Azure"</span>, <span class="s">"Angular"</span>);

  <span class="c">// spec-driven, agent-assisted</span>
  <span class="k">public async</span> <span class="t">Task</span>&lt;<span class="t">Value</span>&gt; ShipAsync(<span class="t">Spec</span> spec)
    =&gt; <span class="k">await</span> agents.BuildAsync(spec);
}}</pre></div></div></header>
<div class="wrap"><div class="stats rv">{stats}</div></div>
<section id="about"><div class="wrap"><div class="sh rv"><div class="eyebrow">01 · About</div><h2>{e(s["aboutTitle"])}</h2></div>
<div class="about"><div class="rv">{about}</div><div class="pillars rv">{pillars}</div></div></div></section>
<section id="experience" style="background:linear-gradient(180deg,transparent,rgba(10,27,51,.6),transparent)"><div class="wrap"><div class="sh rv"><div class="eyebrow">02 · Experience</div><h2>Where I've built things</h2></div><div class="tl">{jobs}</div></div></section>
<section id="skills"><div class="wrap"><div class="sh rv"><div class="eyebrow">03 · Skills</div><h2>The toolbox</h2></div><div class="skills">{skills}</div></div></section>
<section id="handbook"><div class="wrap"><div class="product rv">
<div class="book"><div><div class="bt">PROFESSIONAL EDITION</div><h5>AI-103 Learning Journey</h5><p>Azure OpenAI · Embeddings · Vector Search · RAG · Agents · AI Foundry</p></div><div class="bb">4 volumes · 102 pages · PDF</div></div>
<div class="info"><div class="eyebrow">04 · Handbook</div><h3>{e(pub.get("name", ""))}</h3><p>{e(pub.get("summary", ""))}</p>
<div class="vols"><div class="vol"><b>Vol 1</b> · Azure OpenAI, Embeddings and RAG</div><div class="vol"><b>Vol 2</b> · Agents and Azure AI Foundry</div><div class="vol"><b>Hands-on</b> · Running "Assistant Agent" example</div><div class="vol"><b>102 pages</b> · Four volumes in one PDF</div></div>
<div class="price"><a class="btn p" href="{e(pub.get("url", "#"))}" target="_blank" rel="noopener">Get it on Gumroad →</a><span class="note">Instant PDF download</span></div></div></div></div></section>
<section id="education" style="padding-top:0"><div class="wrap"><div class="sh rv"><div class="eyebrow">05 · Education</div><h2>Foundations</h2></div><div class="edu">{edu}</div>
<div class="quote rv"><p>"{e(ref.get("reference", ""))}"</p><cite>— {e(ref.get("name", ""))}</cite></div></div></section>
<section id="contact" class="contact"><div class="wrap"><div class="eyebrow">06 · Contact</div><h2>Let's build something</h2><p>{e(s["contactLead"])}</p>
<div class="cta"><a class="btn p" href="{li}" target="_blank" rel="noopener">LinkedIn</a><a class="btn s" href="{gh}" target="_blank" rel="noopener">GitHub</a><a class="btn s" href="{profile("Gumroad")}" target="_blank" rel="noopener">Gumroad</a></div></div></section>
<footer><div class="wrap"><span>© <span id="y">{datetime.date.today().year}</span> {e(b["displayName"])}</span><span>Hosted on GitHub Pages</span></div></footer>
<script>
{js}</script></body></html>
'''


def linkedin():
    out = [f"# LinkedIn copy — generated {datetime.date.today()} from resume.json", "",
           "Paste each block into the matching LinkedIn field. Avoid '&' in the headline.", "",
           "## Headline", "```", b["x-linkedin"]["headline"], "```", "", "## About", "```", b["summary"], "",
           "What I bring:"]
    for k in d["skills"]:
        out.append(f"• {k['name']} – {', '.join(k['keywords'][:5])}")
    out += ["", "Always happy to connect about software architecture, .NET, Azure and AI-enabled engineering.", "```", "", "## Experience"]
    for w in d["work"]:
        out += ["", f"### {w['position']} — {w['name']} ({fmt(w.get('startDate'))} – {fmt(w.get('endDate'))})",
                f"Location: {w.get('location', '')}", "```"]
        if w.get("summary"):
            out.append(w["summary"])
        for c in w.get("x-clients", []):
            out.append(f"• {c['name']} ({c['status']}, {c['region']}) – {c['description']}")
        out += [f"• {h}" for h in w.get("highlights", [])]
        if w.get("x-tech"):
            out.append("Tech: " + ", ".join(w["x-tech"]))
        out.append("```")
    out += ["", "## Education"] + [f"- {x['studyType']} {x['area']} — {x['institution']} ({fmt(x.get('startDate'))} – {fmt(x.get('endDate'))})" for x in d["education"]]
    out += ["", "## Certifications"] + [f"- {c['name']} — {c['issuer']}, {fmt(c['date'])}" for c in d["certificates"]]
    out += ["", "## Top skills to pin", "- " + "\n- ".join([".NET", "Software Architecture", "Microsoft Azure"])]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(site(), encoding="utf-8")
    (DIST / "linkedin.md").write_text(linkedin(), encoding="utf-8")
    import shutil
    for f in ("og-image.png",):
        if (SITE / f).exists():
            shutil.copy(SITE / f, DIST / f)
    print("Built dist/index.html and dist/linkedin.md")
