---
name: inspection-ai-base-iteration
description: Continue an inspection AI base or inspection knowledge-base build
  that is already in staged progress (for example A-9 to A-12). Use when the
  user says "继续推进" and the workspace already contains prior stage deliverables
  such as sample CSVs, master drafts, validation maps, or stage memos. The skill
  helps inventory the latest stage, identify the real next move, merge
  overlapping system objects, convert question-hit maps into formal validation
  cards, and produce a concise stage deliverable without reopening solved
  boundary debates.
description_zh: 迎检AI底座阶段推进
description_en: Inspection AI Base Iteration
agent_created: true
---

# inspection-ai-base-iteration

## When to use
- The user asks to continue an already-running inspection AI base / inspection knowledge-base /迎检助手 project.
- The workspace already has staged outputs such as A-8/A-9/A-10/A-11 files, CSV tables, validation questions, or stage memos.
- The real task is not brainstorming from scratch, but pushing the next concrete stage forward.
- Typical triggers:
  - “继续推进”
  - “继续前面的工作”
  - “往下做下一步”
  - “把现在这批收口一下再往前推”

## Steps
1. **Read the latest stage artifacts first**
   - Read the latest stage summary markdown before doing anything else.
   - Read the key CSV / table files that define current reality, not just narrative docs.
   - Identify what is already done, what is still draft-only, and what the last explicit next step was.

2. **Name the real next move in one sentence**
   - Do not reopen solved scope debates.
   - Convert the current state into one concrete next move, such as:
     - merge system objects
     - backfill first real samples
     - turn hit maps into validation cards
     - stabilize a master table

3. **Prefer structural outputs over more prose**
   - If the current weakness is missing data structure, output CSV / table artifacts.
   - If the current weakness is testing readiness, output validation cards.
   - If the user asks for a quick recap, output one short HTML or markdown summary page.
   - Avoid writing another long abstract plan when structured artifacts are now the bottleneck.

4. **When merging stages, apply this retention rule**
   - Stable, reusable, cross-project objects → keep as master objects.
   - Single-project remediation chains → demote to project-specific or scene-specific objects.
   - Mixed objects with both platform ability and product scene → split them: keep platform/master object, retain scene object in question/project layer.

5. **When creating validation cards, include at least**
   - question id / original question
   - primary object
   - supporting systems
   - must-hit fields
   - linked project fields
   - recommended cards
   - forbidden answer boundary
   - current missing fields
   - suggested answer skeleton

6. **If validation is starting, run a document-level dry run before claiming readiness**
   - For each validation question, check four things: route stability, field completeness, boundary stability, and whether the primary object is actually the right object type.
   - Output a structured result file with statuses such as: pass / conditional pass / fail.
   - Separate two kinds of problems:
     - missing fields on the right object
     - wrong object layer entirely (for example, a directory-governance question incorrectly routed to a content-safety object)
   - Also output a prioritized fix list (P0/P1/P2) so the next move is obvious.

7. **If the object layer is fixed but answers are still thin, create evidence-slot tables before rerunning validation**
   - When A-stage work has already repaired the wrong-object problem, do not jump straight into another abstract discussion.
   - Add structured evidence fields for the relevant special objects / scene objects, such as:
     - submission record / acceptance status / responsibility chain
     - directory update record / identification basis / approver
     - attachment version / maintainer / stats caliber / coverage rate
     - retest result / standard-difference note / sample details / fix rate
   - Output at least one table that tells the next validation round what evidence values are still missing.

8. **After a second batch of closure values, prefer semi-live rehearsal over endless backfill**
   - If the project already has: object-layer repair + evidence-slot tables + at least one or two batches of real values, do not keep extending tables forever.
   - Switch the next move to a small rehearsal set (for example 3-5 representative questions), so the remaining gaps come from actual追问 pressure rather than speculation.
   - Pick a mixed set: a few relatively稳的题 and a few最容易在追问里露薄点的题.
   - For each rehearsal question, output at least:
     - opening answer skeleton
     - 1-2 likely follow-up questions
     - safe answer boundary
     - the exact breakpoint where the answer becomes thin
     - whether it is fit for internal rehearsal only or already stable enough for broader use
  - If the user says “继续” again after this stage, prefer converting the rehearsal set into:
    - a live role-play script for regulator / responder / observer
    - a score sheet that forces observations to field-level breakpoints instead of vague comments
  - If the user says “继续” again after the script stage, do not jump straight back into abstract analysis.
    Instead, output a small rehearsal-operations pack:
    - a live session record template
    - an observer note template focused on exact overclaim / breakpoint sentences
    - a post-rehearsal gap tracker that turns exposed weak points into next-round fill tasks
  - If the user says “继续” again after the operations-pack stage, prefer turning those templates into a prefilled round-1 rehearsal pack:
    - a session packet with recommended order, timebox, and stop-rules
    - a prefilled observer log for the chosen questions
    - a first-round triage board with likely breakpoint fields and P0/P1 priorities
  - If the user says “继续” again after the prefilled round-1 pack stage, do not stall on the absence of real logs.
    Instead, output a prefilled post-rehearsal closure pack:
    - a field-level gap list v1 for the chosen questions
    - a by-question routing note that says where each weak point should be filled or downgraded
    - a script-revision queue that marks which sentences must be softened before the next round
  - If the user says “继续” again after the prefilled post-rehearsal closure pack stage, and still has not provided real rehearsal records, do not fake a completed rehearsal.
    Instead, output a live-writeback draft of the same three artifacts:
    - a gap list with columns for actual stable sentence / actual overclaim sentence / actual regulator follow-up / post-live priority
    - a by-question routing note with direct writeback slots for the real rehearsal outcome
    - a script-revision queue that is explicitly marked "待真实回写"
  - If the user says “继续” again after the live-writeback draft stage but still has no real rehearsal records, do not reopen analysis and do not invent new object layers.
    Instead, compress the current execution pack into a one-page moderator pocket version:
    - a direct-read opening reminder
    - a strict timebox / question order table
    - per-question stop-rules and forbidden overclaim sentence reminders
    - a 10-minute post-live closure checklist mapped to the writeback files
  - If the user says “继续” again after the moderator pocket version stage but still has no real rehearsal records, do not duplicate the moderator view.
    Instead, compress the observer-side flow into a one-page observer pocket version:
    - a four-line recording rule (stable sentence / dangerous sentence / breakpoint field / action)
    - a by-question danger-type and must-watch-field table
    - a quick P0/P1/P2 rule
    - a fixed writeback order mapped to the three A-24 files
  - If the user says “继续” again after the observer pocket version stage but still has no real rehearsal records, do not cycle back to moderator or observer formatting.
    Instead, compress the responder-side flow into a one-page responder pocket version:
    - a small set of safe opening / follow-up answer skeletons
    - a dangerous sentence → safer replacement table
    - per-question stop-rules tied to exact formal fields
    - a few fixed closure phrases for when the answer must stop before overclaiming

9. **Explicitly decide whether the user should test now**
   - If master table and validation cards are both ready, say it is time for first-round validation.
   - If not, explain exactly what is still missing before testing.
   - After the first validation run, explicitly say whether the project should continue validating or pause to repair the object layer first.

10. **Always finish with a stage deliverable**
   - Produce a stage summary file that says:
     - what this stage solved
     - what files were created
     - what remains unresolved
     - what the next move is

11. **Update memory**
   - Append the stage result to the daily project memory.
   - If the stage materially changes the project baseline, update the long-term project memory too.

## Pitfalls
- Do not keep writing abstract方案 after the project has already entered real data / real verification phase.
- Do not let A-stage legacy objects and new master objects coexist without an explicit merge decision.
- Do not call scene-specific remediation chains “system masters” just because they look system-like in project notes.
- Do not ask the user to test too early.
- Do not forget to say when the project has actually reached first-round validation readiness.
- During validation, do not confuse “the field is thin” with “the object is wrong.” Wrong-object routing is a P0 structural problem, not a minor field gap.
- If scene objects exist only in prose and not in a table, say so explicitly; otherwise validation may look passable on paper but fail at runtime.
- After fixing object-layer problems, do not rerun validation with only narrative notes; first turn the P1 evidence gaps into explicit fields or evidence-slot tables.
- After a second batch of closure values, do not stay trapped in infinite table backfill; switch to a small semi-live rehearsal set so the next gaps come from real追问 pressure.
- In semi-live rehearsal, do not mistake a problem-pool count for a fix rate, and do not mistake generic support materials for the formal special attachment being asked about.
- After producing role-play scripts, do not leave the next step as “just go rehearse”; also give the team a way to record exact breakpoint sentences and convert them into a structured post-rehearsal fill list.
- After producing rehearsal-operation templates, do not stop at blank forms if the user keeps pushing forward; prefill the first round so the team can start immediately instead of spending energy on setup.
- After producing a prefilled round-1 pack, do not get stuck waiting for perfect live records; first prefill the likely post-rehearsal gap list and script-revision queue so the team knows how to close the loop the moment rehearsal ends.
- If the user still keeps pushing after the prefilled post-rehearsal pack but no actual rehearsal record exists yet, do not pretend the rehearsal already happened; convert the pack into a live-writeback draft that is one edit away from real use.
- After producing a live-writeback draft, do not reopen broad analysis if the user still says “继续”; first consider compressing the execution flow into a moderator pocket version that can be read aloud or printed for the real session.
- After producing a moderator pocket version, do not keep reformatting the same主持内容 if the user still says “继续”; first consider whether the missing piece is the observer-side pocket version that can capture exact sentences and map them into the writeback files.
- After producing an observer pocket version, do not bounce back to more observer formatting if the user still says “继续”; first consider whether the missing piece is the responder-side pocket version that helps the speaker stop before overclaiming.

## Verification
- A new stage file exists and clearly names the current stage.
- At least one structured artifact was produced (CSV / validation card / mapping file / HTML summary).
- The final reply clearly states whether testing should start now.
- Daily memory is updated; long-term memory is updated if the baseline changed.