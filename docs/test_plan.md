# Test plan: how the redesign would be tested with loan officers

**Status: a plan. No test has been run.** There are no results, and the case study page says "planned". If a test is ever run, its results go in `docs/test_results.md`, exactly as they come out, including negative ones. That file does not exist today.

## What the test must answer

| # | Question | Why it matters |
|---|---|---|
| Q1 | Does the redesign shorten the time to assess a file? | Officer time is the capacity limit (see `docs/sources.md`, S5). |
| Q2 | Do officers reach decisions as good as today, or better? | Speed means little if decisions get worse. |
| Q3 | Do officers catch errors when the screen is wrong? | This is automation bias. The study never tested human reviewers, so it is the largest open question. |
| Q4 | Do the review triggers send a manageable number of files, and do they point at real problems? | In the study the checks sent many more files to a person, mostly because small models misread fields. |
| Q5 | Do officers understand the screen, trust it to a sensible degree, and know how to override it? | A recommendation that officers cannot explain will either be ignored or trusted blindly. |

## Who

- **8 to 12 loan officers** from one or two lenders that make small housing or home-improvement loans. At least 3 with under two years in the job and at least 3 with five years or more.
- **2 to 3 senior officers or credit managers** who set the reference decision for every test file before the test starts, and who review the override log afterwards.
- **No applicants.** All files are synthetic.

Why this size: it is enough to see large differences in time and the main points of confusion. It is too small to measure small effects, and the results will say so. Each officer acts as their own comparison, which makes the most of a small group.

## Materials

- **Two matched sets of 6 synthetic file sets** (12 files in all), matched by difficulty and by the problems planted in them. A file set holds the documents a real file would hold: identity details, income evidence, a builder's cost estimate and land evidence. No real applicant or real document is used.
- **Planted problems.** In each set, 3 files are clean, 1 is genuine but messy (an unusual layout, a figure that is net pay instead of gross pay) and 2 carry a planted problem. Planted problems are adapted from the falsification types in the study: income raised in one document, an omitted late payment or debt, a wrong currency or unit, a cost estimate that does not fit the loan amount, two documents that disagree.
- **Silent AI misreadings.** In the redesign condition, one file per set carries a field the AI reads wrongly in a believable way, with no trigger firing. This tests whether officers check the source or trust the screen.
- **A clickable prototype.** The AI readings are prepared in advance and shown as if the AI produced them ("Wizard of Oz"). This controls which errors appear. The test measures the design of the workflow and the screen. It does not measure the quality of any one model. A later run with a live model would test that.
- **Reference decisions** written by the senior officers before any participant sees the files.

## Design

- **Within-officer comparison.** Each officer assesses one set in the current way (paper or spreadsheet, reading and comparing by hand) and the other set with the redesign.
- **Counterbalanced.** Half the officers do the current way first, half do the redesign first. Half see set 1 in the current way, half see set 2. This spreads out learning and tiredness.
- **Two sessions of about 90 minutes** per officer, including a short training on the screen and a short interview at the end.
- **Think-aloud** on 3 files per officer in the redesign condition, with permission.

## Tasks

For each file the officer assesses it, records one of approve, change terms, refer or decline, writes the reasons, and says what they would check next. In the redesign condition they also resolve each flag and may override the recommendation, with a reason.

## What is measured

| Measure | How it is measured | Question |
|---|---|---|
| **Time per file** | Time from opening the file to recording the decision, taken from the prototype log and a stopwatch in the current condition. Median per officer and condition. | Q1 |
| **Agreement with the reference decision** | Share of files where the officer's decision matches the reference set by the senior officers. | Q2 |
| **Agreement with the scorecard** | Share of files where the officer's decision matches the scorecard's recommendation (redesign condition). Read next to agreement with the reference. High agreement with the scorecard shows good alignment or over-trust, and the reference tells which. | Q2, Q3 |
| **Overrides** | Number of overrides, their reasons, and whether the scorecard was right or wrong according to the reference. | Q3 |
| **Planted document problems caught** | Share of planted problems the officer flagged or acted on, in both conditions. | Q2, Q3 |
| **Silent AI misreadings caught** | Share of misreadings with no flag that the officer fixed (redesign condition only). | Q3 |
| **Corrections per file** | Fields the officer corrected (redesign). Typing mistakes against the true values (current). | Q2 |
| **Flag load and flag quality** | Flags per file. Share of flags that pointed at a planted problem or a misreading. Share of planted problems that raised at least one flag. | Q4 |
| **Trust and confusion** | 5-point ratings for "I understood why each flag appeared", "I trusted the recommendation" and "I knew how to override it". Count of screen elements an officer could not explain. Interview notes. | Q5 |

**Not measured in this test:** differences across applicant groups. A synthetic test cannot answer that. It belongs in the shadow pilot, with the lender's own data.

## Pass and stop rules

These are proposals. They are judgements and not facts, so the lender and Craig should agree them **before** any test is run and should not change them afterwards.

- **Proceed to a shadow pilot** only if all of these hold:
  1. Median time per file is at least a quarter lower in the redesign than in the current way.
  2. Planted document problems caught are no lower in the redesign.
  3. Agreement with the reference decision is no lower in the redesign.
  4. At least 70% of silent AI misreadings are caught.
  5. No screen element is one that more than a third of the officers cannot explain.
- **Change the screen and test again** if fewer than half of the silent AI misreadings are caught. Changes would include showing the source first and requiring a check of every field that no flag covers.
- **Stop** if officers accept more silent AI errors in the redesign than they make typing errors in the current way. The redesign would then add risk and not remove it.

## Analysis

Paired comparison for each officer, with medians, ranges and every officer's own result shown. With this sample the descriptive results are the main output, and significance tests would add little. Interview notes and think-aloud are coded for confusion by two people working separately. All results are reported, including ones that go against the design.

## Ethics and safety

- Participation is voluntary and informed. Officers can stop at any time.
- No real applicant data is used.
- Individual results are anonymous and are not shared with employers in an identifiable form. The test measures the design and does not rate the officers.

## What the test cannot show

- It cannot show how the design performs on real files, with real clients or on a live model. A shadow pilot (the AI runs alongside, officers decide the old way and the lender compares) is the next step. It needs the lender's agreement and the applicants' consent.
- Synthetic files with planted problems are artificial. Real problems are less tidy.
- Eight to twelve officers from one or two lenders cannot represent all lenders.
- It cannot show whether the scorecard is fair. That needs the lender's data and a fairness analysis (`docs/redesigned_workflow.md`).

## After the test

1. **Shadow pilot.** The AI and the checks run on real files, with consent and with the lender's approval. Officers decide as they do today. The team compares reading accuracy, flag rate, referral rate and group-level patterns.
2. **Limited live use.** Officers decide with the screen on a small share of files. The pass rules above are reviewed again, and the monthly override review starts.

## Optional small test (not agreed, not run)

Craig could run a small test with 3 to 5 volunteers, using synthetic applications from the study's generator, to compare the old and redesigned steps. Limits to state if it happens: the generator makes consumer-credit documents (payslip, bank statement, application form) and has no builder's estimates or land evidence, and volunteers are not loan officers. Such a run would test whether the screen is understandable. It would say little about how loan officers assess housing loans. Craig has not agreed to it, so none was run, and the page says the test is planned.
