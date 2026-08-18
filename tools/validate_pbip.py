"""Offline PBIP validator.

Cross-checks a PBIP report against its semantic model without opening Power BI
Desktop: every visual field binding must resolve to a real table/column/measure,
every relationship endpoint must exist, and the house rules from
powerbi-kb/01-checklist.md that are checkable from files must hold.

Run it after any TMDL or PBIR edit, and after any rename.

    python tools/validate_pbip.py

Exit code 0 = all checks passed, 1 = at least one failure.
"""
import json, os, io, re, glob, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TM   = os.path.join(BASE, "Bank Marketing.SemanticModel", "definition")
RP   = os.path.join(BASE, "Bank Marketing.Report", "definition")

fail = []
def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: fail.append(msg)

# ---------------------------------------------------------------- parse TMDL
tables, columns, measures = set(), {}, set()
for f in glob.glob(os.path.join(TM, "tables", "*.tmdl")):
    s = io.open(f, encoding="utf-8").read()
    t = re.search(r"^table\s+('([^']+)'|\S+)", s, re.M)
    tn = (t.group(2) or t.group(1)).strip("'")
    tables.add(tn); columns[tn] = set()
    for mm in re.finditer(r"^\tcolumn\s+('([^']+)'|\S+)", s, re.M):
        columns[tn].add((mm.group(2) or mm.group(1)).strip("'"))
    for mm in re.finditer(r"^\tmeasure\s+('([^']+)'|\S+)\s*=", s, re.M):
        measures.add((mm.group(2) or mm.group(1)).strip("'"))

print("MODEL")
print(f"  tables   : {len(tables)}  -> {', '.join(sorted(tables))}")
print(f"  columns  : {sum(len(v) for v in columns.values())}")
print(f"  measures : {len(measures)}")

# relationships must point at real columns
rel = io.open(os.path.join(TM, "relationships.tmdl"), encoding="utf-8").read()
pairs = re.findall(r"(from|to)Column:\s*([A-Za-z_][\w]*)\.('([^']+)'|\S+)", rel)
print("\nRELATIONSHIP ENDPOINTS")
for _, t, raw, q in pairs:
    cn = (q or raw).strip("'")
    check(t in tables and cn in columns.get(t, set()), f"{t}.{cn}")

# ---------------------------------------------------------------- parse report
print("\nREPORT JSON")
allrefs, nvis = set(), 0
pages = json.load(io.open(os.path.join(RP, "pages", "pages.json"), encoding="utf-8"))
for pid in pages["pageOrder"]:
    pj = os.path.join(RP, "pages", pid, "page.json")
    check(os.path.isfile(pj), f"page.json exists for {pid}")
    for vf in glob.glob(os.path.join(RP, "pages", pid, "visuals", "*", "visual.json")):
        nvis += 1
        try:
            d = json.load(io.open(vf, encoding="utf-8"))
        except Exception as e:
            check(False, f"{vf}: {e}"); continue
        def walk(o):
            if isinstance(o, dict):
                for k in ("Column", "Measure", "HierarchyLevel"):
                    if k in o and isinstance(o[k], dict):
                        ent = o[k].get("Expression", {}).get("SourceRef", {}).get("Entity")
                        prop = o[k].get("Property")
                        if ent and prop: allrefs.add((k, ent, prop))
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(d)
check(True, f"all {nvis} visual.json files parse as JSON")

print(f"\nFIELD BINDINGS ({len(allrefs)} distinct)")
for kind, ent, prop in sorted(allrefs):
    if kind == "Measure":
        check(ent in tables and prop in measures, f"[measure] {ent}.{prop}")
    else:
        check(ent in tables and prop in columns.get(ent, set()), f"[column]  {ent}.{prop}")

# ---------------------------------------------------------------- structural
print("\nSTRUCTURE")
model = io.open(os.path.join(TM, "model.tmdl"), encoding="utf-8").read()
check("__PBI_TimeIntelligenceEnabled = 0" in model, "auto date/time disabled")
check("discourageImplicitMeasures" in model, "implicit measures discouraged")
for t in sorted(tables):
    check(f"ref table {t}" in model or f"ref table '{t}'" in model, f"model.tmdl refs {t}")
dd = io.open(os.path.join(TM, "tables", "DimDate.tmdl"), encoding="utf-8").read()
check("dataCategory: Time" in dd and "\t\tisKey" in dd, "DimDate marked as date table")

# every measure has a description and a display folder
mt = io.open(os.path.join(TM, "tables", "_Measures.tmdl"), encoding="utf-8").read()
blocks = re.split(r"(?=^\t/// )", mt, flags=re.M)
nm = sum(1 for b in blocks if re.search(r"^\tmeasure ", b, re.M))
nd = sum(1 for b in blocks if re.search(r"^\tmeasure ", b, re.M) and b.lstrip().startswith("///"))
nf = len(re.findall(r"^\t\tdisplayFolder:", mt, re.M))
check(nd == nm, f"all {nm} measures have a description ({nd}/{nm})")
check(nf == nm, f"all {nm} measures have a display folder ({nf}/{nm})")
# Format strings: every measure needs one EXCEPT measures that return text and
# measures that return an SVG/image URI. ImageUrl ones are detected from their
# dataCategory; the text ones are named explicitly so a rename fails loudly here
# rather than silently widening the exemption (this check used to be a bare
# count of 3, which went stale the moment sparkline measures were added).
TEXT_MEASURES = {"Avg Call Duration (mm:ss)", "Selected Segment", "Data Coverage Note",
                 "Campaign Window"}
missing, exempt = [], 0
for b in blocks:
    mm = re.search(r"^\tmeasure '?([^'=\n]+?)'? *=", b, re.M)
    if not mm:
        continue
    nmame = mm.group(1).strip()
    if nmame in TEXT_MEASURES or "dataCategory: ImageUrl" in b:
        exempt += 1
        check("formatString:" not in b, f"exempt measure {nmame} correctly carries no format string")
        continue
    if not re.search(r"^\t\tformatString:", b, re.M):
        missing.append(nmame)
check(not missing, f"all {nm-exempt} value measures have a format string"
                   + (f" - MISSING: {', '.join(missing)}" if missing else f" ({nm-exempt}/{nm-exempt}); {exempt} text/image measures exempt"))

check("formatString: None" not in mt, "no null format strings leaked")

# fact grain statements
for t in ("FactCampaignContact", "FactUgandaIndicator"):
    s = io.open(os.path.join(TM, "tables", t + ".tmdl"), encoding="utf-8").read()
    check(s.startswith("/// Grain:"), f"{t} description states its grain")

# ---------------------------------------------------------------- TMDL shape
# A multi-line body (expression/measure/source = with nothing after the "=")
# must be indented DEEPER than the object's own property lines, which sit one
# level in from the declaration. If it is not, the TMDL parser cannot tell where
# the body ends and swallows lineageTag/queryGroup/annotation into the code.
# ConnectFolder still "succeeds" on such a file; Power BI Desktop refuses it
# with "Token ';' expected". This check is what catches that.
print("\nTMDL BLOCK INDENTATION")
DECL = re.compile(r"^(\t*)(expression|measure|column|source|partition)\b[^=]*=\s*$")
nblocks = 0
for f in sorted(glob.glob(os.path.join(TM, "**", "*.tmdl"), recursive=True)):
    lines = io.open(f, encoding="utf-8").read().split("\n")
    for i, line in enumerate(lines):
        m = DECL.match(line.rstrip("\r"))
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        body = lines[j].rstrip("\r")
        body_indent = len(body) - len(body.lstrip("\t"))
        prop_indent = len(m.group(1)) + 1
        nblocks += 1
        if body.lstrip("\t").startswith("```"):
            continue                      # explicitly delimited, unambiguous
        check(body_indent > prop_indent,
              f"{os.path.basename(f)}:{i+1} {m.group(2)} body at {body_indent} tabs "
              f"must exceed property indent {prop_indent}")
check(True, f"{nblocks} multi-line blocks scanned")

# themeCollection entries each need reportVersionAtImport, or Desktop rejects
# the report on load.
print("\nREPORT THEME")
rj = json.load(io.open(os.path.join(RP, "report.json"), encoding="utf-8"))
for slot, theme in rj.get("themeCollection", {}).items():
    check("reportVersionAtImport" in theme, f"{slot} has reportVersionAtImport")

# per-page visual count. The <=8 rule exists because each visual costs at least
# one query, so it counts DATA visuals; textboxes, navigators and shapes issue
# no query and are chrome. Alt text is required on everything, chrome included.
print("\nPAGE BUDGET (max 8 data visuals) + ALT TEXT")
CHROME = {"textbox", "pageNavigator", "actionButton", "shape", "image", "basicShape"}
for pid in pages["pageOrder"]:
    pj = json.load(io.open(os.path.join(RP, "pages", pid, "page.json"), encoding="utf-8"))
    data_n = chrome_n = alt_n = tot = 0
    for vf in glob.glob(os.path.join(RP, "pages", pid, "visuals", "*", "visual.json")):
        d = json.load(io.open(vf, encoding="utf-8"))
        tot += 1
        if d["visual"]["visualType"] in CHROME:
            chrome_n += 1
        else:
            data_n += 1
        props = (d["visual"].get("visualContainerObjects", {})
                 .get("general", [{}])[0].get("properties", {}))
        if "altText" in props:
            alt_n += 1
    check(data_n <= 8, f"{pj['displayName']:24s} {data_n} data + {chrome_n} chrome")
    check(alt_n == tot, f"{pj['displayName']:24s} alt text {alt_n}/{tot}")
    # Navigation may be one pageNavigator, or explicit buttons carrying a
    # PageNavigation link. The rule is that every page offers a way out, not
    # that it uses a particular visual - the navigator packs horizontally and is
    # unusable in a narrow rail, so the Executive Overview uses buttons.
    navi = navbtn = 0
    for vf in glob.glob(os.path.join(RP, "pages", pid, "visuals", "*", "visual.json")):
        d = json.load(io.open(vf, encoding="utf-8"))
        vt = d["visual"]["visualType"]
        if vt == "pageNavigator":
            navi += 1
        elif vt == "actionButton" and "PageNavigation" in json.dumps(d):
            navbtn += 1
    check(navi == 1 or navbtn >= 2,
          f"{pj['displayName']:24s} navigation present ({navi} navigator, {navbtn} link buttons)")

print("\n" + ("ALL CHECKS PASSED" if not fail else f"{len(fail)} FAILURES"))
sys.exit(1 if fail else 0)
