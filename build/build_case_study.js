// Builds case_study.md and case_study.docx from one text source, so the two always match.
// Usage: node build/build_case_study.js   (run from the repository root; needs the `docx` npm package)
// Page: A4, 15 mm margins, one column, CMU Serif (Computer Modern) 10 pt, all text black.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, ExternalHyperlink, AlignmentType,
  LevelFormat, BorderStyle, LineRuleType,
} = require(process.env.DOCX_MODULE || "docx");

const ROOT = process.cwd();
const INK = "000000";      // all text and rules are black
const FONT = "CMU Serif";
const BODY = 20;            // half-points: 10 pt
const LINE = Number(process.env.LINE_EXACT || 228);  // twentieths of a point: 228 = 11.4 pt

// ---------------------------------------------------------------- content
// A run is a plain string, or {b}, {i}, or {link, url}.
const LINKS = {
  repo: "https://github.com/craigouma/llm-underwriting-injection",
  paper: "https://craigouma.github.io/llm-underwriting-injection/",
  scholar: "https://scholar.google.com/citations?user=hI6OXwsAAAAJ&hl=en",
  handbook: "https://www.habitat.org/sites/default/files/15.45203.HMF_.Handbook_P1.MNL_.pdf",
};

const C = {
  title: "Reading loan files by hand: keeping the officer in charge",
  byline: "Craig Carlos Ouma, data and systems engineer, Nairobi",
  framing: [
    { i: "A proposed design built on my published study. Not deployed at Habitat or any lender. The user test is a plan." },
  ],
  sections: [
    {
      heading: "The problem",
      blocks: [
        { p: [
          "Housing microfinance lenders make small loans that fund building in stages. Many clients earn informally and have no steady, verifiable income, so approval rests on an officer’s judgement of their cash flow and character ",
          { link: "(Habitat for Humanity handbook, 2015, p. 18)", url: LINKS.handbook },
          ". Each file is read, compared and judged by a person, so officer time is the limit.",
        ] },
      ],
    },
    {
      heading: "The redesign",
      blocks: [
        { img: true },
        { p: [
          "The AI reads the documents and lists each field with the place it came from. Code then raises a review flag for a missing field, a value outside the normal range for the client’s group, values that disagree across documents, or low reading confidence. The officer checks the flags against the source, visits where needed, and sees a recommendation from a simple scorecard (a short table of points) with its reasons. The officer decides and can override. The AI never makes the decision, because in my study that is where it was easiest to steer.",
        ] },
      ],
    },
    {
      heading: "Evidence from my own study",
      blocks: [
        { p: [
          "In my study, planted text won an approval in 41.8% and 65.0% of attacks when a model decided, against 2.7% and 2.0% when the model only read fields and a scorecard decided. Falsified documents passed the scorecard in 16.7% to 19.8% of cases, and an error-free reader passed 19.7% to 19.8%, so reading is not verification. Code checks about halved that (10.1% with an error-free reader) but sent more clean files to a person (32.3% to 56.1% against 15.5% to 17.5%), mostly misread fields. Caveats: synthetic consumer-credit documents, small models, no human reviewers.",
        ] },
      ],
    },
    {
      heading: "Responsible AI choices",
      blocks: [
        { bullets: [
          [{ b: "The loan officer decides. " }, "The AI reads and flags, the scorecard recommends, the officer can always override, and the system never declines anyone. Every applicant can ask for a person to handle the file."],
          [{ b: "Review flags are set in code. " }, "The four checks run in code, not in a prompt, and each recommendation shows the fields it used and where each came from."],
          [{ b: "The applicant is protected. " }, "Consent first, only needed fields kept, overrides logged and reviewed monthly."],
          [{ b: "Three risks, each with a response. " }, "Officers may trust the screen (show sources, require reasons, treat zero overrides as a warning). Falsified documents that no model detects alone (keep visits and independent checks). Unfair patterns across groups (measure by group before use, which my study did not)."],
        ] },
      ],
    },
    {
      heading: "How I would test it",
      blocks: [
        { p: [
          { b: "Planned, not yet run. " },
          "Eight to twelve loan officers each assess matched synthetic housing loan files twice, the current way and with the redesign. Some files carry planted problems, including plausible AI misreadings, to see if officers catch them. I would measure time per file, agreement with the scorecard and an expert reference, overrides and their reasons, planted problems caught, and officers’ trust and confusion. Pass rules are set first.",
        ] },
      ],
    },
    {
      heading: "What this shows I can do",
      blocks: [
        { p: [
          "It shows I can map a document-heavy workflow, redesign it so AI reads and a person decides, and turn results from my own study into design rules and a test plan written for non-technical teams.",
        ] },
      ],
    },
    {
      heading: "Links",
      blocks: [
        { p: [
          { link: "Study repository: github.com/craigouma/llm-underwriting-injection", url: LINKS.repo },
          "  ·  ",
          { link: "Paper page", url: LINKS.paper },
          "  ·  ",
          { link: "Google Scholar profile", url: LINKS.scholar },
        ] },
      ],
    },
  ],
};

// ---------------------------------------------------------------- markdown
function mdRuns(runs) {
  return runs.map((r) => {
    if (typeof r === "string") return r;
    if (r.b) return `**${r.b.trim()}**` + (r.b.endsWith(" ") ? " " : "");
    if (r.i) return `*${r.i}*`;
    if (r.link) return `[${r.link}](${r.url})`;
    return "";
  }).join("");
}

function toMarkdown() {
  const out = [`# ${C.title}`, "", C.byline, "", mdRuns(C.framing), ""];
  for (const s of C.sections) {
    out.push(`## ${s.heading}`, "");
    for (const b of s.blocks) {
      if (b.p) out.push(mdRuns(b.p), "");
      if (b.img) out.push("![Side-by-side diagram of the current and redesigned loan assessment workflows. The AI reads, code flags, a scorecard recommends and the loan officer decides.](diagram/workflow.png)", "");
      if (b.bullets) { b.bullets.forEach((x) => out.push(`- ${mdRuns(x)}`)); out.push(""); }
    }
  }
  return out.join("\n");
}

// ---------------------------------------------------------------- docx
const run = (text, extra = {}) => new TextRun({ text, font: FONT, size: BODY, ...extra });

function docxRuns(runs) {
  return runs.map((r) => {
    if (typeof r === "string") return run(r);
    if (r.b) return run(r.b, { bold: true });
    if (r.i) return run(r.i, { italics: true });
    if (r.link) {
      return new ExternalHyperlink({
        link: r.url,
        children: [new TextRun({ text: r.link, font: FONT, size: BODY, color: INK, underline: {} })],
      });
    }
    return run("");
  });
}

const spacing = (before, after) => ({ before, after, line: LINE, lineRule: LineRuleType.EXACT });

function build() {
  const png = fs.readFileSync(path.join(ROOT, "diagram", "workflow.png"));
  const WIDTH_PX = 680;                       // 180 mm at 96 dpi
  const HEIGHT_PX = Math.round(WIDTH_PX * 450 / 1000);

  const children = [
    new Paragraph({
      spacing: { before: 0, after: 20, line: 340, lineRule: LineRuleType.EXACT },
      children: [new TextRun({ text: C.title, font: FONT, size: 33, bold: true, color: INK })],
    }),
    new Paragraph({
      spacing: spacing(0, 10),
      children: [run(C.byline, { color: INK, smallCaps: false })],
    }),
    new Paragraph({ spacing: spacing(0, 20), alignment: AlignmentType.LEFT, children: docxRuns(C.framing) }),
  ];

  for (const s of C.sections) {
    children.push(new Paragraph({
      keepNext: true,
      spacing: { before: 110, after: 30, line: 250, lineRule: LineRuleType.EXACT },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: INK, space: 1 } },
      children: [new TextRun({ text: s.heading, font: FONT, size: 21, bold: true, color: INK })],
    }));
    for (const b of s.blocks) {
      if (b.p) {
        children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: spacing(0, 0), children: docxRuns(b.p) }));
      }
      if (b.img) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 30, after: 50, line: 240, lineRule: LineRuleType.AUTO },
          children: [new ImageRun({
            type: "png",
            data: png,
            transformation: { width: WIDTH_PX, height: HEIGHT_PX },
            altText: {
              name: "Workflow diagram",
              title: "Current and redesigned loan assessment workflow",
              description: "Seven aligned rows. Today, people read, compare and judge, and a manager decides. In the redesign an AI reads the documents, code raises review flags, the officer checks them, a scorecard recommends and the loan officer decides and can override. Overrides are logged and refine the checks.",
            },
          })],
        }));
      }
      if (b.bullets) {
        for (const item of b.bullets) {
          children.push(new Paragraph({
            numbering: { reference: "bul", level: 0 },
            alignment: AlignmentType.JUSTIFIED,
            spacing: spacing(0, 0),
            children: docxRuns(item),
          }));
        }
      }
    }
  }

  return new Document({
    creator: "Craig Carlos Ouma",
    title: "Reading loan files by hand: keeping the officer in charge",
    description: "One-page design case study. A proposed design built on a published study. Not deployed at any lender. The user test is planned.",
    hyphenation: { autoHyphenation: true, consecutiveHyphenLimit: 2 },
    styles: {
      // The generator ships blue defaults for headings, titles and links. Set them black so that
      // text added later in Word is black too.
      default: {
        document: { run: { font: FONT, size: BODY, language: { value: "en-GB" } } },
        title: { run: { font: FONT, color: INK } },
        heading1: { run: { font: FONT, color: INK } },
        heading2: { run: { font: FONT, color: INK } },
        heading3: { run: { font: FONT, color: INK } },
        heading4: { run: { font: FONT, color: INK } },
        heading5: { run: { font: FONT, color: INK } },
        heading6: { run: { font: FONT, color: INK } },
        hyperlink: { run: { color: INK, underline: { type: "single" } } },
      },
    },
    numbering: {
      config: [{
        reference: "bul",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 300, hanging: 220 } }, run: { font: FONT, color: INK } },
        }],
      }],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 850, right: 850, bottom: 850, left: 850, header: 0, footer: 0 },
        },
      },
      children,
    }],
  });
}

(async () => {
  fs.writeFileSync(path.join(ROOT, "case_study.md"), toMarkdown());
  const buf = await Packer.toBuffer(build());
  fs.writeFileSync(path.join(ROOT, "case_study.docx"), buf);
  console.log("wrote case_study.md and case_study.docx");
})();
