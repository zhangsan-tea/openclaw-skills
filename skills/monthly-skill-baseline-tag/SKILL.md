---
name: monthly-skill-baseline-tag
description: Create a monthly annotated Git baseline tag for the self-authored
  skills repository only when the run date is the first Monday of the month,
  after verifying main/origin alignment, fetching latest refs, requiring a clean
  working tree, summarizing skill changes since the prior baseline, pushing the
  tag safely, and sending a Feishu alert to Lee on blocking failures.
description_zh: 月度 Skill 基线标签
description_en: Monthly skill baseline tag
agent_created: true
---

# monthly-skill-baseline-tag

## When to use
- A scheduled backup workflow needs to create one monthly rollback baseline tag for a Git repository that stores self-authored skills.
- The run happens weekly, but actual tag creation must occur only on the first Monday of the month.
- The workflow must stop on dirty working trees, existing monthly tags, push failures, or other blocking Git errors.
- Failures must trigger a direct Feishu IM notification to Lee with the failed automation name, failed step, reason, and current state.

## Steps
1. Read the automation memory file for the specific automation run and note prior outcomes before taking action.
2. Determine whether today is the first Monday of the current month. If not, record a short skip summary and stop without touching the repository.
3. In the target repository, verify the active branch is `main` and the configured remote is `origin`.
4. Fetch `origin/main` and tags before making any decision. Then require a clean working tree. If there are uncommitted changes, stop and report instead of tagging a dirty state.
5. Generate the monthly tag name with the fixed format `skills-backup-YYYY-MM`.
6. Check whether the tag already exists locally or remotely. If it already exists, stop and report `本月基线标签已存在`. If the existence looks abnormal, treat it as a failure that needs Feishu notification.
7. Build an annotated tag message that states it is the monthly self-authored Skill backup baseline. When possible, summarize changed skill names since the previous baseline by diffing paths under the skills repository between the prior baseline tag and current `main` HEAD.
8. Create the annotated tag on the current `main` HEAD only. Do not retarget older commits unless the user explicitly requests that behavior.
9. Push only that tag to `origin`. Never force push. If push fails, keep the local tag and report that local state clearly.
10. On any blocking failure that matches the automation policy, send Lee a Feishu IM containing: failed automation name, failed step, failure reason, and current state such as whether the local tag was retained.
11. Write a brief high-level execution summary back to the automation memory file and append a concise note to the workspace daily memory file.

## Pitfalls
- Do not create or push tags when the date is not the first Monday.
- Do not tag from a dirty working tree.
- Fetch before checking tag existence, otherwise stale local refs can produce false negatives.
- Treat locally existing tags and remotely existing tags consistently; check both before deciding a new tag is needed.
- If tag push fails, keep the local annotated tag and report that it was retained.
- Feishu failure messages must go to Lee directly and must include automation name, failed step, reason, and current state.
- Do not delete remote content and do not use force push.

## Verification
- Confirm the date gate result is correct.
- If skipped, confirm no Git state was changed.
- If tagged successfully, confirm the new annotated tag points to `main` HEAD and exists on `origin`.
- If failed after local tag creation, confirm the report explicitly states whether the local tag was retained.
- Confirm both automation memory and workspace daily memory were updated.
