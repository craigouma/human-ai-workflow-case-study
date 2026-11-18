# Current workflow: a typical document-based loan assessment

**This is a generic, simplified model.** It is built from public sources (listed in `docs/sources.md`) and from Craig's general understanding of lending work. It does not describe any specific lender or any Habitat process. A real lender will differ in the order of steps, the documents it asks for and who does what.

**How to read the "evidence" column.**
- **Sourced** means a public source in `docs/sources.md` supports the point. The source number is given.
- **Typical, not measured** means the point is a common feature of manual document work that I have not measured and no source here measures. These are the points the test plan (`docs/test_plan.md`) is designed to check.

No time per step is given, because no verified source gives one.

## The eight steps

| # | Step | Who does it | What they use | Where it is slow or error-prone | Evidence |
|---|---|---|---|---|---|
| 1 | **Intake.** The applicant states what they want to build and how much they need. | Loan officer, with the applicant | Paper or app form, notes | Details are written by hand and typed again later. Gaps in the form are found late. | Typical, not measured |
| 2 | **Collect documents.** Identity papers, income records (a payslip, business records, a statement), a builder's cost estimate, and evidence about the land or plot. | Applicant and loan officer | Photocopies, phone photos, a paper file | Many clients earn in cash or in the informal economy and have no steady, verifiable income records, so the officer accepts whatever evidence exists. Clients may need several trips to complete the file. | Sourced: S3 (page 18), S6 for cash income. Number of trips: typical, not measured |
| 3 | **Read the documents and type the fields.** The officer reads each document and enters the figures that matter (income, existing debts, cost estimate, identity details) into the loan system or a spreadsheet. | Loan officer or back-office clerk | The documents, the loan system or a spreadsheet | Reading and typing are manual. Every employer, shop and builder uses a different layout. Digits are mistyped or the wrong line is read (for example net pay entered as gross pay). Officers differ in which figures they treat as the income. | Typical, not measured |
| 4 | **Cross-check the documents.** The officer compares documents with each other and with the application. Does the name match? Do the income figures agree? Does the builder's cost estimate fit the loan amount? | Loan officer | The same documents, memory and experience | Done by eye, so it depends on attention and experience. Conflicts are found late. A changed figure or a forged document is hard to see by eye. | Cost-estimate check: sourced, S3 (page 46). Rest: typical, not measured |
| 5 | **Verify in person.** The officer visits the home or the business, speaks to the applicant, and checks land security. | Loan officer | A visit, questions, local knowledge | Travel takes officer time. CGAP describes a required on-site visit as "a significant slowdown" in an otherwise streamlined process, and it adds cost. | Visits and land checks: sourced, S3 (pages 18, 45 and 46). On-site slowdown: sourced, S5 (it describes loan renewals). Officer time overall: S5 gives a model with assumed inputs, not a measurement |
| 6 | **Judge ability and willingness to pay.** The officer builds a picture of household cash flow and weighs the applicant's character. | Loan officer | Notes from steps 2 to 5, the lender's rules of thumb | Judgement differs between officers and between days. The reasoning stays in the officer's head and in short notes, so it is hard to explain or check later. The work leans on a few experienced officers. | Method: sourced, S3 (page 18). Differences between officers and reliance on a few experienced officers: typical, not measured |
| 7 | **Recommend and approve.** The officer recommends. A manager or committee approves, changes the terms or declines. | Loan officer, then manager or committee | The file, the officer's notes | Files wait in a queue for the approver. Approvers see the officer's summary more than the documents. Reasons for changes are rarely written down in a consistent way. | Typical, not measured |
| 8 | **Record and disburse.** The file is stored and, if approved, the loan is paid out. | Loan officer, back office | The loan system, the paper file | Reasons for the decision are brief. Corrections and overrides are not collected, so the lender and its officers learn little from them. | Typical, not measured |

## Where the pain concentrates

1. **Steps 3 and 4 are reading and comparing.** They are repetitive, they are done by hand, and an AI system can help with them. These are the steps the redesign changes.
2. **Steps 5 and 6 are human judgement.** They rely on a visit and on knowing the client. The redesign leaves them with the officer.
3. **Step 7 is the decision.** It stays with people. The redesign gives the decision-maker better evidence and records why decisions change.
4. **Step 8 is the missing feedback loop.** The redesign adds a log of overrides and reasons.

## What this model leaves out

- Loan products with a group guarantee, mobile-money lending and repeat loans. Each has its own flow.
- Regulatory checks and sanctions screening, which differ by country.
- Anything about how long each step takes. The test plan includes a plan to measure time per file.

## Source tags

S3, S5 and S6 refer to `docs/sources.md`.
- S3: Habitat for Humanity International, *Housing Microfinance Product Development: A Handbook, Part 1* (2015).
- S5: CGAP, *Building value in microfinance through digitization* (2023). Its officer-time figures come from a model with assumed inputs.
- S6: CGAP blog, *Can Platform Data Expand Access to Transformative Credit?* (2022).
