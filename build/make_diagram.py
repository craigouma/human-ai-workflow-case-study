"""Generate diagram/workflow.svg: the current and redesigned loan assessment workflows, side by side.

Usage: python3 build/make_diagram.py [output.svg]
Standard library only. One accent colour (navy) and black on white. No icons, no gradients.

Encoding, shown in the legend:
  white box with black outline  = a person does it
  navy-tinted box, navy outline = AI or code does it (tagged AI or CODE)
  solid navy box                = a person decides
Rows are aligned across the two columns. The numbered spine in the middle ties each pair of rows together.
"""
import sys
from xml.sax.saxutils import escape

INK, INK2, NAVY, TINT = "#111111", "#3a3a3a", "#1F3A5F", "#E6ECF4"
FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"

W, H = 1000, 450
ROW0, PITCH, CARD_H = 48, 52, 42
LX, LW = 10, 425          # left cards
SPINE = 500               # centre line
RX, RW = 565, 388         # right cards
LOOP_X = 968

# kind: person | machine | decide
LEFT = [
    ("person", "Applicant brings documents", "Officer collects ID, income records, cost estimate", None),
    ("person", "Officer reads and types the fields", "By hand, into a form or spreadsheet", None),
    ("person", "Officer compares documents by eye", "Conflicts and changed figures are easy to miss", None),
    ("person", "Officer visits and judges the case", "Cash flow and character, from notes and memory", None),
    ("person", "Officer writes a recommendation", "From notes, in short free text", None),
    ("decide", "Manager or committee decides", "Reasons are recorded in short notes", None),
    ("person", "File stored", "Little feedback on overrides or outcomes", None),
]
RIGHT = [
    ("person", "Applicant consents and brings documents", "A person-only route is offered to everyone", None),
    ("machine", "AI reads the documents", "Lists each field and where it came from", "AI"),
    ("machine", "Code raises review flags", "Missing, out of range, conflicting, unsure", "CODE"),
    ("person", "Officer checks the flags and judges the case", "Source beside each value. Visits when flagged", None),
    ("machine", "Scorecard recommends, with reasons", "A suggestion only. It never declines anyone", "CODE"),
    ("decide", "Loan officer decides", "Approve, change, decline or refer. Can override", None),
    ("person", "Overrides and reasons are logged", "Team lead reviews patterns monthly, by group", None),
]


def top(i):
    return ROW0 + i * PITCH


def centre(i):
    return top(i) + CARD_H / 2


def card(x, w, i, kind, title, detail, tag):
    y = top(i)
    if kind == "person":
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{CARD_H}" rx="2" fill="#ffffff" stroke="{INK}" stroke-width="1.25"/>'
        t1, t2 = INK, INK2
    elif kind == "machine":
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{CARD_H}" rx="2" fill="{TINT}" stroke="{NAVY}" stroke-width="1.25"/>'
        t1, t2 = NAVY, INK2
    else:
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{CARD_H}" rx="2" fill="{NAVY}" stroke="{NAVY}" stroke-width="1.25"/>'
        t1, t2 = "#ffffff", "#ffffff"
    out = [box,
           f'<text x="{x + 14}" y="{y + 18}" font-size="15" font-weight="700" fill="{t1}">{escape(title)}</text>',
           f'<text x="{x + 14}" y="{y + 35}" font-size="13.5" fill="{t2}">{escape(detail)}</text>']
    if tag:
        out.append(f'<text x="{x + w - 12}" y="{y + 18}" font-size="12" font-weight="700" letter-spacing="1.2" '
                   f'text-anchor="end" fill="{NAVY}">{tag}</text>')
    return "\n    ".join(out)


def build():
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
    p.append('  <title>Loan assessment workflow: today and redesigned</title>')
    p.append('  <desc>Seven aligned rows compare a typical manual loan assessment with the proposed redesign. In the redesign an AI reads the documents, '
             'code raises review flags, the officer checks them, a scorecard recommends and the loan officer decides and can override. '
             'Human decision points are filled navy. Overrides are logged and reviewed, and the review refines the checks.</desc>')
    p.append('  <defs>')
    p.append(f'    <marker id="down" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="{INK}"/></marker>')
    p.append(f'    <marker id="back" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="{NAVY}"/></marker>')
    p.append('  </defs>')
    p.append(f'  <rect width="{W}" height="{H}" fill="#ffffff"/>')

    # column headings: a bold line and a one-line summary
    p.append(f'  <text x="{LX}" y="19" font-size="17" font-weight="700" letter-spacing="0.6" fill="{INK}">TODAY</text>')
    p.append(f'  <text x="{LX + 72}" y="19" font-size="13.5" fill="{INK2}">generic model, not any one lender</text>')
    p.append(f'  <rect x="{LX}" y="28" width="{LW}" height="2" fill="{INK}"/>')
    p.append(f'  <text x="{RX}" y="19" font-size="17" font-weight="700" letter-spacing="0.6" fill="{NAVY}">REDESIGNED</text>')
    p.append(f'  <text x="{RX + 124}" y="19" font-size="13.5" fill="{INK2}">proposed, not deployed</text>')
    p.append(f'  <rect x="{RX}" y="28" width="{RW}" height="2" fill="{NAVY}"/>')

    # spine segments with down arrows, drawn first so circles sit on top
    for i in range(6):
        p.append(f'  <line x1="{SPINE}" y1="{centre(i) + 13}" x2="{SPINE}" y2="{centre(i + 1) - 13}" stroke="{INK}" stroke-width="1.5" marker-end="url(#down)"/>')

    for i in range(7):
        lk, rk = LEFT[i][0], RIGHT[i][0]
        # connectors from cards to the spine
        p.append(f'  <line x1="{LX + LW}" y1="{centre(i)}" x2="{SPINE - 13}" y2="{centre(i)}" stroke="{NAVY if lk == "decide" else INK}" stroke-width="1" />')
        p.append(f'  <line x1="{SPINE + 13}" y1="{centre(i)}" x2="{RX}" y2="{centre(i)}" stroke="{NAVY if rk == "decide" else INK}" stroke-width="1" />')
        # numbered node
        decide = rk == "decide"
        p.append(f'  <circle cx="{SPINE}" cy="{centre(i)}" r="13" fill="{NAVY if decide else "#ffffff"}" stroke="{NAVY if decide else INK}" stroke-width="1.5"/>')
        p.append(f'  <text x="{SPINE}" y="{centre(i) + 5}" font-size="14" font-weight="700" text-anchor="middle" fill="{"#ffffff" if decide else INK}">{i + 1}</text>')
        # cards
        p.append("  <g>\n    " + card(LX, LW, i, *LEFT[i]) + "\n  </g>")
        p.append("  <g>\n    " + card(RX, RW, i, *RIGHT[i]) + "\n  </g>")

    # feedback loop: the log feeds back into the checks
    y7, y3 = centre(6), centre(2)
    p.append(f'  <path d="M{RX + RW},{y7} H{LOOP_X} V{y3} H{RX + RW + 2}" fill="none" stroke="{NAVY}" stroke-width="1.25" stroke-dasharray="4 3" marker-end="url(#back)"/>')
    p.append(f'  <text transform="translate({LOOP_X + 15},{(y7 + y3) / 2}) rotate(-90)" font-size="12" text-anchor="middle" fill="{NAVY}">Overrides refine the checks</text>')

    # legend
    ly = ROW0 + 6 * PITCH + CARD_H + 24
    p.append(f'  <line x1="{LX}" y1="{ly - 12}" x2="{RX + RW}" y2="{ly - 12}" stroke="{INK}" stroke-width="0.75"/>')
    items = [
        (LX, f'<rect x="{LX}" y="{ly}" width="28" height="14" rx="2" fill="#ffffff" stroke="{INK}" stroke-width="1.25"/>', "Person does it", 50),
        (200, f'<rect x="200" y="{ly}" width="28" height="14" rx="2" fill="{TINT}" stroke="{NAVY}" stroke-width="1.25"/>', "AI or code does it", 240),
        (410, f'<rect x="410" y="{ly}" width="28" height="14" rx="2" fill="{NAVY}" stroke="{NAVY}" stroke-width="1.25"/>', "Person decides", 450),
    ]
    for _, shape, label, tx in items:
        p.append("  " + shape)
        p.append(f'  <text x="{tx}" y="{ly + 12}" font-size="13.5" fill="{INK}">{label}</text>')
    p.append(f'  <text x="{RX + RW}" y="{ly + 12}" font-size="13.5" font-weight="700" text-anchor="end" fill="{NAVY}">The AI and the scorecard never decide</text>')
    p.append('</svg>')
    return "\n".join(p) + "\n"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "diagram/workflow.svg"
    open(out, "w", encoding="utf-8").write(build())
    print("wrote", out)
