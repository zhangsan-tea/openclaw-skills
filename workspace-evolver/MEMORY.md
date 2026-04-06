# MEMORY.md - System Evolution Lessons

## Hard Lessons (Never Repeat)

### 🚫 Never Fabricate External Links Without Verification
**Context**: When providing repository URLs or external links, always verify they actually exist before presenting them to the user.

**Root Cause**: Assumed directory structure from README files matches actual repository contents without validation.

**Correct Approach**: 
1. Always test URLs with web_fetch or equivalent before providing them
2. If a resource only exists locally, clearly state this instead of creating fake remote links  
3. When in doubt, provide local paths and ask if user wants to sync to remote repository

**Verification Checklist**:
- [ ] Does the URL return HTTP 200?
- [ ] Does the directory actually contain the expected files?
- [ ] Are there any 404 errors when accessing subdirectories?
- [ ] If it's a GitHub repo, does `git ls-tree` show the expected structure?

### 🔍 Always Validate Assumptions Against Reality
**Context**: Don't assume file system structure matches documentation or README descriptions.

**Correct Approach**:
1. Use `find`, `ls`, or API calls to discover actual file structure
2. Cross-reference multiple sources of truth (local files + remote repos)
3. When discrepancies are found, investigate rather than assume

### 📋 Provide Accurate Source Attribution
**Context**: Clearly distinguish between local-only resources and remotely available ones.

**Correct Format**:
- **Local Only**: "Available in local directory: /path/to/skill/"
- **Remote Available**: "Available at: https://github.com/..."
- **Mixed**: "Local version available at /path/, remote version at https://..."

## Patterns to Watch

### Directory vs Repository Mismatch
When a README describes a skill set but the actual repository contains fewer skills than documented, always verify each individual skill's existence before providing links.

### README as Documentation vs README as Current State
README files often describe intended/planned functionality rather than current implementation. Always treat README as aspirational unless verified against actual code.