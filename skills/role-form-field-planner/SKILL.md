---
name: role-form-field-planner
description: Plan or redesign a role-oriented form, registry, or field
  dictionary when the user has an existing draft/table but wants cleaner fields
  based on role responsibilities, operating logic, and related ledger/schema
  knowledge. Best for cases where a current form mixes person fields, project
  fields, process records, and review outputs, and the real task is to separate
  layers, keep only decision-useful fields, and propose grouped fields with
  requiredness.
description_zh: 角色表单字段规划
description_en: Role Form Field Planner
agent_created: true
---

# role-form-field-planner

## When to use
Use this skill when most of the following are true:
1. The user has an existing form, table, register, card, or field list and is dissatisfied with it.
2. The user wants to redesign the **fields**, not yet build the actual table/page.
3. The form is tied to a role, mechanism, or team workflow, such as observers, experts, PM support, trainees, or operational records.
4. The correct answer depends on combining multiple anchors: role responsibilities, prior ledger/data-model work, and the current draft form.
5. A common hidden problem is that one sheet mixes different entities, such as person registry + single-project records + review outputs.

Typical triggers:
- “这个登记表我不满意，你帮我梳理应该有哪些字段”
- “先不做表格，先把字段定清楚”
- “结合职责文档和以前的台账字段，重提一版字段”
- “这个档案卡到底该记录人还是记录项目”

## Steps
1. Read the current form or draft first.
   - If it is a `doc.weixin.qq.com` link and WeCom CLI is available, prefer the WeCom path.
   - Extract the current field structure exactly enough to diagnose what it is trying to do.

2. Read the role anchor and the schema anchor.
   - Role anchor: latest role memo / boundary doc / responsibility note.
   - Schema anchor: prior ledger-field notes, data-model docs, or related topic/source notes.
   - Pull only the sections that affect field design: role定位, what to observe, what to record, what should be excluded, and prior schema principles.

3. Diagnose the current form before proposing new fields.
   - Explicitly test whether it is mixing:
     - person registry fields
     - project/case fields
     - process/现场记录 fields
     - review/复盘/沉淀 fields
   - If mixed, say so directly and propose a split instead of polishing the wrong structure.

4. Decide the target artifact type.
   - Is this primarily:
     - a people registry / roster
     - a single-case observation record
     - a ledger entry
     - a training record
     - a post-action handoff memo / role submission template
     - a hybrid that should be split into A/B forms
   - Be careful: a form named after a role (for example “observer card”) is not always a people registry. Sometimes it is really the material that role should submit after joining a project.
   - Name the target clearly before listing fields.

5. Propose grouped fields, not a flat dump.
   For each group, explain what decision it supports.
   Common groups:
   - basic identity
   - capability / support scope
   - participation history / light ledger
   - role-specific observation fields
   - training / talent discovery
   - operational status
   - fields that should be moved to another form

6. Mark field priority.
   - Separate into `必填 / 建议补充 / 后补` or similar layers.
   - Keep first version lightweight; avoid heavy scoring unless the user explicitly wants it.

7. Make the split rule explicit.
   - List which fields belong in the current form.
   - List which fields should move into another form (for example single-project observation record).
   - If the current target is already the “project/case” side after an A/B split, test one more boundary: which fields belong in the single-case card, and which should stay only in the multi-project internal operations dashboard.
   - This is often the real value of the task.

8. Deliver a concise memo.
   Include:
   - top-line judgment on the old form
   - design principles
   - grouped field recommendation
   - what to remove or relocate
   - one-line summary of what this form should become

## Pitfalls
- Do not treat the task as cosmetic editing of field names when the real problem is wrong entity boundaries.
- Do not dump all possible fields into one table; if people-registry and project-record goals conflict, split them.
- Do not assume a role-named form is evaluating that person. It may actually be a post-project memo the role submits after participating, and the right split may be “project basic info card + role submission memo” rather than “people table + project table”.
- Even after an A/B split, do not let the project/case form absorb all internal-operations fields; keep full to-do tracking, version logs, resource scheduling, and heavy file-management fields in the internal dashboard instead of the single-case card.
- Do not import heavy HR/performance fields unless the user explicitly wants formal assessment.
- Do not over-quantify soft judgments like support quality or talent potential in the first version.
- Do not lose the link between role memo and field design; the best fields are direct operational translations of responsibilities.

## Verification
A good result should satisfy all checks:
1. The current form's main structural problem has been diagnosed explicitly.
2. The proposed fields are grouped by purpose, not listed as a flat brainstorm.
3. The result explains which fields stay and which fields move to another form.
4. The field set supports real decisions such as dispatch, matching, review, or training.
5. The first version remains lightweight enough to operate instead of becoming another dead form.
