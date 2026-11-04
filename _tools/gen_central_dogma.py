# -*- coding: utf-8 -*-
"""Generate the pixel-art transcription band used in the homepage hero.

Writes an SVG include that _sass/_bio.scss animates: an RNA polymerase rides the
DNA duplex left to right while a nascent RNA strand is revealed behind it.

Usage:
    python3 -I _tools/gen_central_dogma.py _includes/central_dogma.liquid

Edit the sprite grids below rather than hand-tweaking the generated rects.

Layout follows the biology. The duplex runs 5' to 3' left to right. Factors
cluster at the promoter near the 5' end with a cofactor bound on top of one of
them, and they stay put. The polymerase initiates at the transcription start
site downstream of that cluster, so it never runs through the factors, and it
elongates rightward while the RNA strand trails from behind it.

Parked, deliberately not emitted: a ribosome that folds out a protein to complete
DNA to RNA to protein. Add it back by defining the grid and placing it in
compose().
"""
import io
import math
import sys

# Canvas in pixel-art user units. Scaled to the container width by CSS, so these
# are "pixels" of the artwork, not of the screen.
W, H = 640, 48

PALETTE = {
    "O": "#14868c",  # polymerase body
    "T": "#d4762a",  # transcription factor
    "C": "#8e5fd3",  # cofactor
    "W": "#ffffff",  # eye white
    "K": "#0b2a2e",  # pupil
}

# Chunky blob with two eyes; the split bottom row straddles the duplex.
POLYMERASE = [
    "....OOOOOO....",
    "..OOOOOOOOOO..",
    ".OOOOOOOOOOOO.",
    "OOOOOOOOOOOOOO",
    "OOWWOOOOOOWWOO",
    "OOWKOOOOOOWKOO",
    "OOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOO",
    ".OOOOOOOOOOOO.",
    ".OO.OOOOOO.OO.",
    "OOO..OOOO..OOO",
]

# Transcription factor: a squat blob with two eyes and little feet.
FACTOR = [
    "..TTTT..",
    ".TTTTTT.",
    "TTWTTWTT",
    "TTKTTKTT",
    "TTTTTTTT",
    ".TTTTTT.",
    "T.T..T.T",
]

# Cofactor: smaller, binds on top of a factor. The space above the promoter is
# free because the RNA strand only begins downstream, at the start site.
COFACTOR = [
    ".CCC.",
    "CCCCC",
    "CWCWC",
    "CCCCC",
    ".CCC.",
]

# DNA duplex geometry
RAIL_TOP, RAIL_BOT, RAIL_T = 28, 38, 2
RAIL_COLOUR = "#64748b"
BASE_COLOURS = ["#e0565b", "#f2b134", "#4aa3df", "#58c07a"]  # A T G C
RUNG_PITCH = 6

# Nascent RNA strand
RNA_COLOUR = "#e05fa8"
RNA_MID, RNA_AMP, RNA_WAVELENGTH = 18.0, 2.5, 26.0

# Promoter: the factors bind as a cluster near the 5' end rather than spread
# along the gene, with the cofactor on top of the middle one.
FACTOR_X = (24, 36, 48)
COFACTOR_X = 37

# Transcription start site, downstream of the promoter cluster. The polymerase
# sprite is emitted here and the RNA path begins here, so transcription starts
# from the start site rather than from the left edge of the band.
TSS = 72

# CSS must translate the polymerase by exactly this much, over the same duration
# and step count as the RNA reveal, or the strand will not track the sprite.
TRAVEL = W - TSS


def sprite(grid, ox, oy, indent):
    """Emit rects for a pixel grid, merging horizontal runs of one colour."""
    out = []
    for row_index, row in enumerate(grid):
        col = 0
        while col < len(row):
            ch = row[col]
            if ch == ".":
                col += 1
                continue
            run = 1
            while col + run < len(row) and row[col + run] == ch:
                run += 1
            out.append(
                '{0}<rect x="{1}" y="{2}" width="{3}" height="1" fill="{4}"/>'.format(
                    indent, ox + col, oy + row_index, run, PALETTE[ch]
                )
            )
            col += run
    return "\n".join(out)


def duplex():
    """Two rails plus colour-cycled base-pair rungs."""
    out = [
        '    <rect x="0" y="{0}" width="{1}" height="{2}" fill="{3}"/>'.format(
            RAIL_TOP, W, RAIL_T, RAIL_COLOUR
        ),
        '    <rect x="0" y="{0}" width="{1}" height="{2}" fill="{3}"/>'.format(
            RAIL_BOT, W, RAIL_T, RAIL_COLOUR
        ),
    ]
    rung_y = RAIL_TOP + RAIL_T
    rung_h = RAIL_BOT - rung_y
    for i, x in enumerate(range(3, W - 2, RUNG_PITCH)):
        out.append(
            '    <rect x="{0}" y="{1}" width="2" height="{2}" fill="{3}" opacity="0.85"/>'.format(
                x, rung_y, rung_h, BASE_COLOURS[i % len(BASE_COLOURS)]
            )
        )
    return "\n".join(out)


def rna_path():
    """A gentle wave spanning the full width, sampled coarsely to stay small."""
    pts = []
    for x in range(TSS, W + 1, 4):
        y = RNA_MID + RNA_AMP * math.sin(x / RNA_WAVELENGTH)
        pts.append("{0},{1:.1f}".format(x, y))
    return "M " + " L ".join(pts)


def compose():
    pol_y = RAIL_TOP - len(POLYMERASE) + 3  # split bottom row straddles the top rail
    parts = [
        "  <!-- DNA duplex -->",
        '  <g class="cd-dna">',
        duplex(),
        "  </g>",
        "  <!-- nascent RNA, revealed in step with the polymerase -->",
        '  <path class="cd-rna" d="{0}" pathLength="100" fill="none" stroke="{1}"'
        ' stroke-width="2" stroke-linecap="round"/>'.format(rna_path(), RNA_COLOUR),
        "  <!-- bound transcription factors, with a cofactor docked to the second -->",
    ]
    fac_y = RAIL_TOP - len(FACTOR) + 1
    for i, x in enumerate(FACTOR_X):
        parts.append('  <g class="cd-factor cd-factor--{0}">'.format(i + 1))
        parts.append(sprite(FACTOR, x, fac_y, "    "))
        parts.append("  </g>")
    parts.append('  <g class="cd-cofactor">')
    parts.append(sprite(COFACTOR, COFACTOR_X, fac_y - len(COFACTOR), "    "))
    parts.append("  </g>")
    parts += [
        "  <!-- RNA polymerase, riding the duplex left to right. Drawn last so it",
        "       passes in front of the bound factors. -->",
        '  <g class="cd-polymerase">',
        '    <g class="cd-polymerase-bob">',
        sprite(POLYMERASE, TSS, pol_y, "      "),
        "    </g>",
        "  </g>",
    ]
    return "\n".join(parts), pol_y


def main():
    body, pol_y = compose()
    svg = """@@OPEN@@ comment @@CLOSE@@
  Pixel-art transcription band: an RNA polymerase rides the DNA duplex while the
  RNA strand it is producing is revealed behind it.

  Generated by _tools/gen_central_dogma.py -- edit the sprite grids there rather
  than these rects. Motion lives in _sass/_bio.scss and switches off under
  prefers-reduced-motion, leaving a composed mid-transcription frame.

  Decorative, so it is hidden from assistive technology.
@@OPEN@@ endcomment @@CLOSE@@
<svg
  class="central-dogma"
  viewBox="0 0 {W} {H}"
  preserveAspectRatio="xMinYMid slice"
  shape-rendering="crispEdges"
  role="presentation"
  aria-hidden="true"
  focusable="false"
>
{BODY}
</svg>
""".format(W=W, H=H, BODY=body)

    svg = svg.replace("@@OPEN@@", "{%-").replace("@@CLOSE@@", "-%}")
    io.open(sys.argv[1], "w", encoding="utf-8").write(svg)
    print("wrote {0} ({1} bytes)".format(sys.argv[1], len(svg)))
    print("polymerase rows at y={0}..{1}; rails at {2} and {3}".format(
        pol_y, pol_y + len(POLYMERASE) - 1, RAIL_TOP, RAIL_BOT))
    print("promoter at x={0}; start site x={1}".format(FACTOR_X, TSS))
    print("CSS cd-travel must run 0 -> {0}px; RNA midline y={1}".format(TRAVEL, RNA_MID))


if __name__ == "__main__":
    main()
