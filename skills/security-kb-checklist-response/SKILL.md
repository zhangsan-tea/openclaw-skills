---
name: security-kb-checklist-response
description: Retrieve Tencent internal security knowledge base materials first,
  then answer high-level product security scope questions with a concise
  prioritized checklist, grouped domains, and source links. Use when the user
  asks what security areas to focus on in a product, wants a review checklist,
  or needs a launch/self-check list rather than exploit details or code fixes.
description_zh: 安全清单回答
description_en: Security checklist
agent_created: true
---

# security-kb-checklist-response

## When to use
Use this skill when the user asks broad product-security questions such as:
- what security areas are commonly important in company products
- give me a security checklist for design review, launch review, or self-check
- summarize key domains like app security, data security, IAM, cloud/container, incident response, and compliance

Do not use it for code vulnerability review, exploit reproduction, incident triage, or narrow remediation questions like "how to fix SSRF".

## Steps
1. Search internal knowledge bases first for product security governance, network security compliance, data security compliance, and related operational guidance.
2. Prefer sources that map to broad security domains: secure development lifecycle, application/API security, identity and access control, data security, network boundary, cloud-native/container security, supply-chain security, monitoring/incident response, and compliance obligations.
3. Extract only stable, reusable control themes. Do not overfit to one document title or one business line.
4. Answer with conclusion first: give a practical checklist the user can use immediately in reviews.
5. Group the checklist by domain and priority. Highlight the few areas that usually cause real incidents first.
6. Always include source links to the internal documents used.
7. If internal knowledge is partial, clearly label any extra industry-standard supplement as General Advice.

## Pitfalls
- Do not answer from memory without searching the internal KB first.
- Do not turn a checklist request into a long theory lecture.
- Do not give exploit payloads or tell users to weaken controls for convenience.
- Do not omit source links.

## Verification
- Confirm at least one internal KB search was performed before answering.
- Confirm the final answer includes source links and a directly usable checklist or domain breakdown.
