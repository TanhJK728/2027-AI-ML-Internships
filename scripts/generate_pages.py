#!/usr/bin/env python3
"""
Generate README.md, country pages, and track pages from data/internships.csv.

Run:
    python scripts/generate_pages.py
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "internships.csv"

FOCI = [
    ("world-models", "🌍 World Models", ["world model", "world models", "world modeling", "world understanding", "behavior modeling", "prediction"]),
    ("multimodal", "🧩 Multimodal", ["multimodal", "vlm", "mllm", "video generation", "image", "visual generation", "vision-language", "aigc"]),
    ("ml-research", "🧠 ML Research", ["ml research", "machine learning", "foundation model", "foundation models", "llm", "deep learning", "representation learning", "research"]),
    ("robotics", "🤖 Robotics / Embodied AI", ["robot", "robotics", "embodied", "physical ai", "humanoid", "autonomous", "autonomy", "vla", "driving", "simulation"]),
    ("data-science", "📊 Data Science", ["data science", "analytics", "experimentation", "applied ml"]),
]

COUNTRIES = {
    "United States": ("united-states", "🇺🇸 United States"),
    "China": ("china", "🇨🇳 China"),
}

def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")

def table(rs):
    lines = [
        "| Company | Role | Focus | Location | Degree | Deadline | Apply |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rs:
        lines.append(
            f"| **{esc(r['Company'])}** | {esc(r['Role'])} | {esc(r['Track'])} | "
            f"{esc(r['Location'])} | {esc(r['Degree'])} | {esc(r['Deadline'])} | "
            f"[Link]({r['Link']}) |"
        )
    return "\n".join(lines)

def match(r, keywords):
    hay = " ".join([r.get("Role",""), r.get("Track",""), r.get("Company",""), r.get("Location","")]).lower()
    return any(k in hay for k in keywords)

with CSV.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

last_checked = max(r["Last Checked"] for r in rows if r.get("Last Checked"))

def get(country=None, status=None, keywords=None):
    out = rows
    if country:
        out = [r for r in out if r["Country"] == country]
    if status:
        out = [r for r in out if r["Status"] == status]
    if keywords:
        out = [r for r in out if match(r, keywords)]
    return out

# README
us_open = get("United States", "Open")
cn_open = get("China", "Open")
us_watch = get("United States", "Watch")
cn_watch = get("China", "Watch")

readme = f"""# 2027 AI / ML Internships

<p align="center">
  <strong>Summer 2027 internship tracker for AI / ML research in the United States and China.</strong>
</p>

<p align="center">
  <img alt="US roles" src="https://img.shields.io/badge/US_open-{len(us_open)}-2ea44f">
  <img alt="China roles" src="https://img.shields.io/badge/China_open-{len(cn_open)}-2ea44f">
  <img alt="Last updated" src="https://img.shields.io/badge/updated-{last_checked.replace('-', '--')}-blue">
</p>

This repository tracks public internship opportunities in **machine learning research, student research, world models, multimodal AI, embodied/physical AI, robotics, foundation models, reinforcement learning**, plus a small number of strong **data science / applied ML** roles.

> **No personal application data is stored here.** This is a public, community-style job list.

## Choose a region

<table>
<tr>
<td align="center" width="50%">

### [🇺🇸 United States →](countries/united-states.md)

**{len(us_open)} open roles** · {len(us_watch)} companies/programs on watch

Google · Apple · NVIDIA · Waymo · Physical Intelligence · Pika · Persona AI · Tesla · and more

</td>
<td align="center" width="50%">

### [🇨🇳 China →](countries/china.md)

**{len(cn_open)} open roles/programs** · {len(cn_watch)} companies/programs on watch

ByteDance Seed · MSRA · Baidu · Momenta · NVIDIA · Huawei · Xiaomi · Meituan · and more

</td>
</tr>
</table>

## Browse by focus

<p>
<a href="tracks/world-models.md"><img src="https://img.shields.io/badge/🌍_World_Models-browse-6f42c1"></a>
<a href="tracks/multimodal.md"><img src="https://img.shields.io/badge/🧩_Multimodal-browse-1f6feb"></a>
<a href="tracks/ml-research.md"><img src="https://img.shields.io/badge/🧠_ML_Research-browse-0969da"></a>
<a href="tracks/robotics.md"><img src="https://img.shields.io/badge/🤖_Robotics-browse-d29922"></a>
<a href="tracks/data-science.md"><img src="https://img.shields.io/badge/📊_Data_Science-browse-8250df"></a>
</p>

## Status

| Symbol | Meaning |
|---|---|
| 🟢 | Open / currently listed |
| 🟡 | Watchlist — target company or program; matching 2027 role not yet verified as open |
| ⏳ | Rolling / no fixed deadline listed |
| 📅 | Explicit deadline found |

## Data

The machine-readable list is in [`data/internships.csv`](data/internships.csv).

China internship recruiting often uses **日常实习 / rolling internship programs** rather than a single fixed “Summer 2027” posting. The China page therefore includes roles active in the **2027 internship cycle** that can overlap Summer 2027.

## Updating the pages

`data/internships.csv` is the source of truth.

After editing the CSV, regenerate all Markdown pages with:

```bash
python scripts/generate_pages.py
```

## Contributing

PRs are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Disclaimer

Job postings and deadlines change quickly. Always verify the current requirements on the linked employer page before applying. This repository is not affiliated with any listed company.
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")

# Country pages
(ROOT / "countries").mkdir(exist_ok=True)
for country, (slug, label) in COUNTRIES.items():
    open_rows = get(country, "Open")
    watch_rows = get(country, "Watch")

    focus_nav = []
    focus_sections = []
    for fslug, flabel, keywords in FOCI:
        subset = [r for r in open_rows if match(r, keywords)]
        focus_nav.append(f"[{flabel} ({len(subset)})](#{fslug})")
        focus_sections.append(
            f'<a id="{fslug}"></a>\n\n## {flabel}\n\n'
            + (table(subset) if subset else "_No currently verified open roles in this category._")
            + "\n\n[↑ Back to filters](#browse-by-focus)"
        )

    page = f"""# {label} — 2027 AI / ML Internships

[← Main page](../README.md) · [CSV data](../data/internships.csv)

**Last checked:** {last_checked}  
**Open roles/programs:** {len(open_rows)} · **Watchlist:** {len(watch_rows)}

<a id="browse-by-focus"></a>

## Browse by focus

{" · ".join(focus_nav)}

> Roles may appear in more than one focus area when the work spans multiple research themes.

## 🟢 All open roles

{table(open_rows)}

{"".join(focus_sections)}

## 🟡 Watchlist

{table(watch_rows)}

---

[↑ Back to top](#{slug}--2027-ai--ml-internships) · [← Main page](../README.md)
"""
    (ROOT / "countries" / f"{slug}.md").write_text(page, encoding="utf-8")

# Track pages
(ROOT / "tracks").mkdir(exist_ok=True)
for slug, label, keywords in FOCI:
    us = get("United States", "Open", keywords)
    cn = get("China", "Open", keywords)
    us_w = get("United States", "Watch", keywords)
    cn_w = get("China", "Watch", keywords)

    page = f"""# {label} — 2027 Internships

[← Main page](../README.md) · [🇺🇸 United States](../countries/united-states.md) · [🇨🇳 China](../countries/china.md)

**Last checked:** {last_checked}

## 🇺🇸 United States — Open

{table(us) if us else "_No currently verified open roles._"}

## 🇨🇳 China — Open

{table(cn) if cn else "_No currently verified open roles._"}

## 🟡 Watchlist

### United States

{table(us_w) if us_w else "_No watchlist entries in this category._"}

### China

{table(cn_w) if cn_w else "_No watchlist entries in this category._"}

---

[← Main page](../README.md)
"""
    (ROOT / "tracks" / f"{slug}.md").write_text(page, encoding="utf-8")

print("Generated README, country pages, and focus pages.")
