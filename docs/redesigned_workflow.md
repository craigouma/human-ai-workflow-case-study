# Redesigned workflow: AI reads and flags, code checks, a person decides

**Status: a proposed design.** It is not deployed at Habitat or at any lender, and no loan officer has used it. It builds on Craig's published, preregistered study (`docs/evidence.md`). It redesigns the generic workflow in `docs/current_workflow.md`. The diagram is in `diagram/workflow.svg` and `diagram/workflow.png`.

## The idea in four sentences

1. The AI does the reading. It turns each document into a short list of fields and records where in the document each value came from.
2. Code does the checking. Four triggers written in code send any doubtful file to a person.
3. A simple scorecard recommends. It shows the fields it used and why it reached its recommendation.
4. The loan officer decides. They can approve, change the terms, decline or send the file to a committee, and they can override the recommendation in either direction. The system never declines anyone.

## Why the AI stays away from the decision

In the study, planted instructions in synthetic applicant documents won an approval in 41.8% and 65.0% of attacked cases when a model made the decision (Phi-4-mini and Olmo-3 7B). When the same models only read fields and a scorecard decided, the figures were 2.7% and 2.0% (`docs/evidence.md`, section 3). The reason is structural. The model's output has no field that can carry a decision, so text planted in a document has nothing to steer.

## The eight steps

| Step | Who or what does it | What the human does | Control that protects the person |
|---|---|---|---|
| **1. Intake and consent** | Loan officer, with a simple on-screen form | Explains in plain words what the AI will read and why, and asks for consent. Offers the choice of a person-only route. | Consent is recorded. Only the fields the checks and the scorecard need are kept (data minimisation). An applicant who prefers no AI gets the same decision rights. They are told the wait may be longer. |
| **2. Collect documents** | Applicant and loan officer (unchanged) | Collects identity papers, income evidence, the builder's cost estimate and land evidence. Accepts the kinds of evidence informal earners actually have. | The officer can mark "no formal record" for a document type. A missing formal document never causes an automatic decline. |
| **3. AI reads the documents** | AI model | Nothing required here. Any field can be corrected in step 5. | The model writes only a fixed list of fields, each with the place it came from in the document. It has no decision field. Output that fails the format check, or cannot be read, becomes "needs a person". Text inside a document is treated as data. |
| **4. Code checks and review triggers** | Code (no AI) | Nothing required here. Flags arrive in step 5. | Four triggers, written in code and out of reach of anything written in a document: a missing field, a value outside the plausible range for the client's group, values that disagree across documents, and low reading confidence. Any trigger routes the file to a person. |
| **5. Officer reviews flags and checks fields** | Loan officer, with the on-screen view | Checks each flagged field against the highlighted source, fixes misreadings, resolves each flag by looking at the document, phoning the applicant or visiting, and decides whether a visit is needed. The visit and the judgement of cash flow and character stay with the officer. | Every flag needs a recorded resolution. Every correction is logged. The source sits beside each value. No recommendation becomes final while a flag is open. |
| **6. Scorecard recommends** | Simple points-based scorecard (code) | Reads the reasons and the fields used. May disagree. | The scorecard shows each field it used, where that value came from and how many points it added. It recommends approve, refer or decline as a suggestion only. A "decline" suggestion always goes to a person. The scorecard is built and validated on the lender's own data and checked for group differences before use. |
| **7. Loan officer decides** | Loan officer. Manager or committee where the lender's rules require it. | Approves, changes the terms, declines with reasons, or refers. Can override the recommendation in either direction. | Only a person can decline. The applicant hears the reasons in plain words and can ask for a second person to look again. Every override needs a reason, chosen from a short list plus free text. |
| **8. Log and learn** | System log, reviewed by a team lead | Reviews overrides, corrections and flags each month. Looks at patterns by group. | Overrides, reasons and corrections are stored. An override rate close to zero is treated as a warning that officers may be trusting the screen. Error rates, flag rates, referral rates and waiting times are compared across groups. |

## What changes against today

| Today | Redesigned |
|---|---|
| Step 3: the officer reads and types fields | The AI reads and records the source of each value. The officer checks instead of typing. |
| Step 4: the officer compares documents by eye | Code compares them every time and flags conflicts. |
| Step 5 and 6: visit and judgement | Unchanged. They stay with the officer. |
| Step 7: officer recommends, approver decides | A scorecard adds a visible recommendation. The decision stays with a person. |
| Step 8: little feedback | Overrides and reasons are logged and reviewed. |

## Design principles, and where each shows up

| Principle | How the design applies it | Steps |
|---|---|---|
| **The loan officer decides.** | The AI reads and flags. The scorecard recommends. The officer approves, changes or declines and can always override. | 5, 6, 7 |
| **Keep the AI away from the decision.** | This is architecture B or C from the study. The model extracts fields and code decides. | 3, 4, 6 |
| **Review triggers live in code.** | Four triggers, listed below. | 4 |
| **Show the reasoning.** | Each recommendation lists the fields used and the place each came from, so the officer can check it in seconds. | 5, 6 |
| **Log overrides.** | Every override and its reason is recorded and reviewed monthly. | 7, 8 |
| **Protect the applicant.** | Consent, data minimisation, no automated declines, and a route to a person for every applicant. | 1, 2, 6, 7 |
| **Name the risks.** | Automation bias, falsified documents and unfair patterns across groups, with a design response for each (below). | 5, 8 |

## The four review triggers

| Trigger | What it catches | What the study shows |
|---|---|---|
| **Missing field** | A required field is empty, unreadable or fails the format check. | The range and missing-field group of checks lowered the success of falsified documents by 5.6, 3.2 and 8.3 points for the three models (Table 7). Olmo-3 7B left the deposits field empty for some bundles, and almost all of its flagged clean bundles had this flag. |
| **Value outside the plausible range for the segment** | An income, debt ratio, balance or cost estimate far outside what is normal for the client's group. This includes a wrong currency or unit. | A payslip in the wrong currency passed the scorecard in 60.0% to 92.0% of cases and passed the currency check in 0.0% (`docs/evidence.md`, section 4). The plausible-band check on its own added only 0.3 to 0.6 points of protection for 1.0 to 1.7 points of extra review, so the bands need careful setting. |
| **Conflicting values across documents** | The declared income disagrees with the payslip or the statement. A builder's estimate does not fit the loan amount. | The cross-document checks gave the largest drop in success (7.6, 3.4 and 2.6 points) and the largest rise in review work, because reading errors also create conflicts. Habitat's handbook lists "verifying cost estimates with the approved loan amount" as a standard check (S3, page 46). |
| **Low reading confidence** | The AI reports that it is unsure about a field. | **Design addition. The study did not test this trigger.** I have no evidence yet on how well it finds real misreadings. The test plan checks it. It supplements the other three and never replaces them. |

## What the officer sees

- A list of fields, each with the value, the highlighted place in the document, and a flag where a trigger fired.
- Flags first, in plain words (for example "Income on the form is 40,000 and the payslip says 32,000").
- The scorecard's recommendation after the fields, with the points each field added.
- A decision panel with approve, change terms, decline and refer, and a required reason when the decision differs from the recommendation or when a flagged file is approved.

## What is logged

For each file: the fields as the AI read them, every correction the officer made, each flag and how it was resolved, the scorecard's recommendation, the decision, and the reason for any override. Time spent on the file is recorded for the test. Documents are kept only for the period the lender needs them.

## The three named risks and the design response

| Risk | Why it matters here | Design response |
|---|---|---|
| **Automation bias.** Officers trust the screen and stop checking. | The study never tested human reviewers. It counts a referral to a person as a stopped attack and assumes the person catches the problem. Whether that happens is open. | Show the source beside each value. Show flags before the recommendation. Require a reason for every approval of a flagged file and for every override. Treat an override rate near zero as a warning. Mix known test files with planted errors into the monthly queue and measure how many are caught. The test plan measures this before any live use. |
| **Falsified documents that no model can detect alone.** | In the study, falsified documents passed the scorecard in 16.7% to 19.8% of cases. A perfect reader passed them in 19.7% to 19.8%. Code checks about halved that to 10.1% with a perfect reader. What remains is values that appear in one document only and forgeries that agree across documents. | Keep the visit, the phone call and independent sources where the lender can get them, such as a credit bureau report. Keep the cross-document checks. Never present the AI's reading as verification. |
| **Unfair patterns across groups.** | The study did not measure fairness. Plausible mechanisms are untested: the AI may read some documents worse (handwriting, phone photos, other languages), and the checks may flag genuine but unusual documents, such as informal income records, more often. The scorecard may also carry bias from its training data. | Before any use, measure reading accuracy, flag rate, referral rate, waiting time and decision rate by gender, age band, location and income type on the lender's own data, and repeat monthly. Agree a limit for gaps in advance. A gap above the limit pauses the AI step for that group and sends the files to people. Review scorecard inputs for stand-ins for protected traits. |

## Costs and open points

1. **More files go to a person.** In the study the checks raised total referrals on clean files from 15.5% to 17.5% (scorecard alone) to 32.3% to 56.1%. Most flagged files held a reading error (90.4% to 97.1%). With a perfect reader the checks flagged only 1.5% to 2.0% of clean files. The study's readers were three small open-weight models, and real documents are messier. A pilot must measure the flag rate on the lender's own documents.
2. **The scorecard must be built for this use.** The study's scorecard is a research model trained on 2011 US consumer credit data. It is not for use on real applicants. A scorecard for housing microfinance needs the lender's own data, validation and a fairness check.
3. **The documents differ.** The study used payslips, bank statements and application forms. Housing microfinance files also hold builder's estimates and land evidence, and many clients have no payslip. The reading step needs testing on those documents. The study contains none.
4. **Consent and data handling rules differ by country.** I have not verified the legal requirements for Kenya or any other country, and the design states its choices as design choices, not as legal conclusions.
5. **No human has used the design.** Every statement about officers is a design intention until the test in `docs/test_plan.md` is done.

## Source tags

S3 refers to `docs/sources.md`: Habitat for Humanity International, *Housing Microfinance Product Development: A Handbook, Part 1* (2015). Table numbers refer to the paper.
