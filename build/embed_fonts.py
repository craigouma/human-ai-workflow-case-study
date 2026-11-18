"""Embed CMU Serif (Computer Modern Unicode) in a .docx, so the page keeps its layout on machines without the font.

Usage: python3 build/embed_fonts.py case_study.docx /path/to/cmu-fonts
Needs: fonttools (pip install fonttools) and cmunrm.otf, cmunbx.otf, cmunti.otf, cmunbi.otf (SIL Open Font License).

What it does, in order:
  1. converts each OpenType (CFF) file to TrueType outlines, which Word can embed;
  2. subsets it to Latin letters, digits and common punctuation, to keep the .docx small;
  3. obfuscates it as the OOXML spec requires (first 32 bytes XORed with a GUID key) and stores it as word/fonts/*.odttf;
  4. registers the four styles in word/fontTable.xml and its relationships, and declares the .odttf content type.
"""
import io
import re
import sys
import uuid
import zipfile

from fontTools import subset
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

FAMILY = "CMU Serif"
FILES = [("Regular", "cmunrm.otf"), ("Bold", "cmunbx.otf"), ("Italic", "cmunti.otf"), ("BoldItalic", "cmunbi.otf")]
# Basic Latin, Latin-1, Latin Extended-A, general punctuation, euro, minus
UNICODES = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + list(range(0x2010, 0x2028)) + list(range(0x2030, 0x203B)) + [0x20AC, 0x2212, 0x2022]


def otf_to_ttf(font, max_err=1.0):
    """Replace cubic CFF outlines with quadratic TrueType outlines (after fontTools' otf2ttf snippet)."""
    assert font.sfntVersion == "OTTO" and "CFF " in font
    order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()
    quad = {}
    for name in glyph_set.keys():
        pen = TTGlyphPen(glyph_set)
        glyph_set[name].draw(Cu2QuPen(pen, max_err, reverse_direction=True))
        quad[name] = pen.glyph()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = quad
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]
    glyf.compile(font)
    hmtx = font["hmtx"]
    for name, glyph in glyf.glyphs.items():
        if hasattr(glyph, "xMin"):
            hmtx[name] = (hmtx[name][0], glyph.xMin)
    font["maxp"] = maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    maxp.maxZones = 1
    maxp.maxTwilightPoints = maxp.maxStorage = maxp.maxFunctionDefs = maxp.maxInstructionDefs = 0
    maxp.maxStackElements = maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = max(len(getattr(g, "components", [])) for g in glyf.glyphs.values())
    maxp.compile(font)
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = order
    font.sfntVersion = "\x00\x01\x00\x00"


def prepare(path):
    font = TTFont(path)
    otf_to_ttf(font)
    options = subset.Options()
    options.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.hinting = False
    sub = subset.Subsetter(options)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    font["OS/2"].fsType = 0   # installable embedding, as the licence allows
    out = io.BytesIO()
    font.save(out)
    return out.getvalue()


def obfuscate(data, guid):
    key = bytes.fromhex(guid.hex)[::-1]
    head = bytes(b ^ key[i % 16] for i, b in enumerate(data[:32]))
    return head + data[32:]


def main(docx_path, font_dir):
    embedded = []
    for n, (style, fname) in enumerate(FILES, start=1):
        data = prepare(f"{font_dir}/{fname}")
        guid = uuid.uuid4()
        embedded.append((style, f"fonts/font{n}.odttf", f"rIdFont{n}", "{" + str(guid).upper() + "}", obfuscate(data, guid)))
        print(f"  {style}: {len(data) // 1024} KB")

    with zipfile.ZipFile(docx_path) as zin:
        items = {i.filename: zin.read(i.filename) for i in zin.infolist() if not i.filename.endswith("/")}

    rels = "".join(
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="{target}"/>'
        for _, target, rid, _, _ in embedded
    )
    items["word/_rels/fontTable.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>'
    ).encode()

    tags = {"Regular": "embedRegular", "Bold": "embedBold", "Italic": "embedItalic", "BoldItalic": "embedBoldItalic"}
    embeds = "".join(f'<w:{tags[s]} r:id="{rid}" w:fontKey="{key}"/>' for s, _, rid, key, _ in embedded)
    items["word/fontTable.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<w:font w:name="{FAMILY}"><w:altName w:val="Times New Roman"/><w:charset w:val="00"/><w:family w:val="roman"/>'
        f'<w:pitch w:val="variable"/>{embeds}</w:font></w:fonts>'
    ).encode()

    for _, target, _, _, blob in embedded:
        items[f"word/{target}"] = blob

    ct = items["[Content_Types].xml"].decode()
    if "odttf" not in ct:
        ct = re.sub(r"(<Types[^>]*>)", r'\1<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/>', ct, count=1)
    items["[Content_Types].xml"] = ct.encode()

    names = ["[Content_Types].xml"] + [k for k in items if k != "[Content_Types].xml"]
    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, items[name])
    print("embedded", len(embedded), "font files in", docx_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
