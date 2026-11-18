# Review log (Phase 6)

Reviewed text: `case_study.md`, which `build/build_case_study.js` also uses to make the DOCX and PDF.

## What was checked

| Check | How | Result |
|---|---|---|
| Every sentence traced to evidence | Table below. Each claim is matched to `docs/evidence.md`, `docs/sources.md` or a design document. | Pass. Two items are premises from the brief, not evidence, and are labelled. |
| Every number on the page | Script pulled all numbers from `case_study.md` and compared them with the figures approved for the page (E1 to E3). | Pass. 12 of 12 approved figures used. The only other numbers are "2015" and "p. 18" (source S3). |
| Banned style | Script searched for em dashes, en dashes, "not X but Y", "rather than", "not just" and "not only", and buzzwords (leverage, synergy, transformative, seamless, holistic, empower, robust, unlock and others). | None found in `case_study.md`, the README or the landing page content. In `docs/` the only hits are the real title of a CGAP post that `docs/sources.md` cites, and the ordinary word "Robustness" in a heading of `docs/evidence.md` about the study's robustness checks. |
| Plain language | Readability score and a jargon check (below). | Pass, with one judgement call noted. |
| One A4 page | `build/build.sh` stops with an error unless `pdfinfo` reports one page. | Pass. |
| DOCX integrity | The DOCX skill's schema validator, and a ZIP test. | "All validations PASSED". No folder entries in the ZIP. |
| DOCX keeps one page without the font | Rendered the DOCX in a LibreOffice profile with no Computer Modern installed. | One page, in the embedded Computer Modern. Before the fonts were embedded this render spilled to two pages. |

## Where each sentence comes from

Type: **Evidence** is a figure from the study (`docs/evidence.md`). **Source** is a public source (`docs/sources.md`). **Design** is a choice in `docs/redesigned_workflow.md`. **Plan** is `docs/test_plan.md`. **Premise** is the brief's description of the case and is not measured.

| Section | Claim | Backed by | Type |
|---|---|---|---|
| Title | "Reading loan files by hand: keeping the officer in charge" | Names the current step (reading by hand) and the design goal. It makes no claim about time. | Design |
| Framing | A proposed design, not deployed, user test is a plan. | Honesty rule 1. `docs/test_plan.md` status line. | Design |
| Problem | Housing microfinance lenders make small loans that fund building in stages. | S2, S3 | Source |
| Problem | Many clients earn informally and have no steady, verifiable income, so approval rests on an officer's judgement of cash flow and character. | S3, page 18 ("loan approval process... based on an assessment of the applicant's ability to pay (cash flow) and assumed willingness to pay (character assessment)", clients "do not have steady and verifiable income") | Source |
| Problem | Each file is read, compared and judged by a person, so officer time is the limit. | `docs/current_workflow.md`. S5 supports the officer-time point with a CGAP model that uses assumed inputs. | **Premise** |
| Redesign | The AI reads the documents and lists each field with the place it came from. | `docs/redesigned_workflow.md`, step 3 | Design |
| Redesign | Code raises a review flag for a missing field, a value outside the normal range for the client's group, values that disagree across documents, or low reading confidence. | `docs/redesigned_workflow.md`, step 4 and the four triggers. The last trigger is a design addition that the study did not test. | Design |
| Redesign | The officer checks the flags against the source, visits where needed, and sees a recommendation from a simple scorecard with its reasons. | Steps 5 and 6 | Design |
| Redesign | The officer decides and can override. | Step 7 | Design |
| Redesign | The AI never makes the decision, because in my study that is where it was easiest to steer. | E1: the deciding model was steered in 41.8% and 65.0% of attacks, against 2.7% and 2.0% when it only read fields | Evidence |
| Evidence | Planted text won an approval in 41.8% and 65.0% of attacks when a model decided, against 2.7% and 2.0% when it only read fields and a scorecard decided. | E1: Table 4, recomputed from the decision files | Evidence |
| Evidence | Falsified documents passed the scorecard in 16.7% to 19.8% of cases, and an error-free reader passed 19.7% to 19.8%, so reading is not verification. | E2: Tables 4 and 6, recomputed | Evidence |
| Evidence | Code checks about halved that (10.1% with an error-free reader). | E3: 19.7% to 10.1% is a 49% fall | Evidence |
| Evidence | The checks sent more clean files to a person (32.3% to 56.1% against 15.5% to 17.5%), mostly misread fields. | E3: Table 3 total referrals. 90.4% to 97.1% of flagged files held a reading error, recomputed | Evidence |
| Evidence | Caveats: no human reviewers, so the officer's role is untested, plus synthetic consumer-credit documents and small models. | E6 and `docs/evidence.md`, sections 6 and 7 | Evidence |
| Responsible AI | The loan officer decides, can always override, the system never declines anyone, every applicant can ask for a person. | Steps 1, 6 and 7 | Design |
| Responsible AI | The four checks run in code, not in a prompt. Each recommendation shows the fields used and where each came from. | Steps 4 to 6 | Design |
| Responsible AI | Consent first, only needed fields kept, overrides logged and reviewed monthly. | Steps 1 and 8 | Design |
| Responsible AI | Three risks with responses. "Which my study did not" measure by group. | `docs/redesigned_workflow.md` risk table. `docs/ethics.md` of the study: no fairness analysis was done. | Design, Evidence |
| Test | Eight to twelve officers, matched synthetic housing loan files, current way and redesign, planted problems including plausible AI misreadings, the listed measures, pass rules set first. | `docs/test_plan.md` | Plan |
| What this shows | Maps a workflow, redesigns it so AI reads and a person decides, turns study results into design rules and a test plan written for non-technical teams. | The work in this repository. | Design |
| Links | Repository, paper page, Scholar profile. | The brief | n/a |

## Changes made because of the review

1. **Scope line restored.** The evidence paragraph had dropped "consumer-credit". Required scope line E6 says the study used consumer-credit documents, which differ from housing loan files. The caveat now reads "synthetic consumer-credit documents, small models, no human reviewers".
2. **"Triggers" changed to "review flags" on the page.** The redesign paragraph said "flag" and a bullet said "triggers". A non-technical reader could take them for two things. The documents keep "trigger" as the technical term.
3. **"A test plan that non-technical teams can use" changed to "written for non-technical teams".** The first form claims a result nobody has tested.
4. **"Attacked cases" changed to "attacks".** Plainer, and shorter.
5. **The DOCX now embeds its font.** See the table above.
6. **Title shortened** and its time claim removed (see decision 1).
7. **All text set in black**, in the PDF, the DOCX and the diagram (see decision 6).

## Read of the live page by an outside reviewer

An outside reader reviewed the published page. Three points, each checked:

1. **The key finding overreached.** It opened with "let the AI read the documents and let a person decide". The study had a scorecard make the decision and tested no human reviewers, so the loan officer is the design's addition and not a tested result. The web page now says so ("The redesign adds a loan officer, which the study did not test"). The PDF caveat says the same ("no human reviewers, so the officer's role is untested").
2. **The 10.1% figure.** It is in the paper, in Table 6 (Section 5.3), as the oracle ASR of C: 10.1% for Qwen and Phi and 9.7% for the smaller Olmo run. Recomputed from the decision files: 203 of 2,006 attacks. It does not appear in the paper's abstract or on the study's landing page, so the tile on the web page now cites Table 6.
3. **The PDF.** One A4 page. Body text is 10 pt, headings 10.5 pt, title 16.5 pt. The diagram is 180 mm wide and prints its text between 6.1 pt and 8.7 pt: step titles 7.7 pt, detail lines and legend 6.9 pt, the AI and CODE tags and the loop label 6.1 pt. All text is black.

## Plain-language check

- Readability of the running text, by a simple syllable count: average sentence 16 words, Flesch reading ease about 58, grade level about 9. The percentage figures raise the grade level. This is an indicative number, not a verdict.
- Terms a non-technical reader might not know:

| Term on the page | Treatment |
|---|---|
| scorecard | Defined in place: "a short table of points". |
| review flag | Defined by the four things it flags, in the same paragraph. |
| error-free reader | Plain phrase for the study's "oracle extractor". |
| planted text, attacks | Plain phrases for prompt injection and attack success. |
| override | Plain English. It is used in context ("can override"). |
| AI | Common word. |

- Terms kept off the page: LLM, extraction, AUROC, preregistered, oracle, model names, ASR.
- **Judgement call:** the evidence paragraph still has a long sentence (38 words) with several percentages. I kept it because every figure was approved, and splitting it would push the page past one sheet. A hiring manager can skim it for the two contrasts (decider against reader, and falsified documents with and without checks).

## Decisions and open items

1. **Title.** Shortened to "Reading loan files by hand: keeping the officer in charge". The earlier title ("take too long to read") rested on the brief's premise and not on a measurement. The new one makes no claim about time.
2. **Author name.** "Craig Carlos Ouma", as on the paper and the Scholar profile.
3. **Optional figures not used.** E4 (the currency check) and E5 (decision quality) are in `docs/evidence.md` and the design documents, and left off the page.
4. **No seventh source.** No Kenya data-protection source was added, so the design states consent and minimisation as design choices and makes no legal claim.
5. **Optional real test.** Not run. The page says the test is planned.
6. **Text colour.** All text on the page is black. Navy is used only for box fills and rules in the diagram.
7. **Publishing.** The repository is public and the page is served by GitHub Pages from `main`.
