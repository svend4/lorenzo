# 3. What InGit Provides That Cowork Lacks

## 3. What InGit Provides That Cowork Lacks

Equally important: where does InGit add value that Cowork 
alone doesn't provide?

### 3.1. Structured File Organization

Cowork Projects can point at any folder. The folder structure 
is up to the user. Without convention, structures vary 
arbitrarily.

InGit provides **canonical structure** (00_inbox through 
90_exports). This means:
- Cowork agent can rely on consistent layout
- Knowledge work flows to predictable locations
- New users encounter familiar patterns
- Templates can be shared
- Cross-project comparison is meaningful

This is substantial. Cowork's effectiveness scales with 
quality of workspace structure. InGit provides the structure.

### 3.2. Metadata as Code

Cowork can read and write any file format. But unstructured 
files limit what Cowork can do. Without metadata, tasks have 
no status, documents have no provenance, artifacts have no 
relationships.

InGit's YAML metadata as code provides:
- Task definitions Cowork can parse and update
- Document headers with version, author, status
- Relationships between artifacts (depends-on, references, 
  derives-from)
- Validation schemas Cowork can enforce
- Timeline of changes through Git history

This metadata layer dramatically increases what Cowork can 
do meaningfully with InGit Projects compared to generic 
folders.

### 3.3. Git-Native Versioning

Cowork can use Git through shell commands. But Cowork doesn't 
inherently structure work as Git history. Each Cowork session 
might commit, might not. Commit messages might be informative, 
might not.

InGit provides **conventions** that make Git history meaningful:
- Commit message format
- Pre-commit hooks for validation
- Branching strategy for project work
- Tag structure for releases
- Hook integration with task status

This makes Git history **navigable as project history**, not 
just as code change log.

### 3.4. Validation and Quality Control

Cowork might create files with errors. Generic Cowork has no 
domain knowledge to validate.

InGit's validation hooks ensure:
- YAML conforms to schema
- Required metadata fields present
- File naming conventions followed
- No large files committed by accident
- Encryption applied to sensitive folders

If exposed through MCP, Cowork uses these validations 
automatically. Cowork's outputs become reliably structured.

### 3.5. Encryption for Sensitive Content

Cowork has security model (isolated VM, permissions) but does 
not provide content encryption. Sensitive content sits in 
plaintext (subject to permission system).

InGit's encryption layer (age, SQLCipher) provides:
- File-level encryption for sensitive folders
- Project-level encryption for whole projects
- Key management
- Decryption on access

This matters for legal work, financial data, health information 
— exactly the categories Anthropic recommends Cowork not be 
used with currently.

### 3.6. Offline-First Operation

Cowork requires Claude Desktop running. While Claude Desktop 
can work with local files, Cowork itself depends on Anthropic's 
infrastructure.

InGit Projects work entirely offline. Even without Cowork, 
the Project structure, files, Git history, validation — all 
work. When Cowork available, additional capabilities; when 
not, baseline still functional.

This matters for: travel, locations with poor connectivity, 
privacy-sensitive work, situations where dependence on 
external infrastructure is undesirable.

### 3.7. Portability Between AI Platforms

Cowork is Anthropic-specific. If you use Cowork extensively 
and later need to switch platforms (Gemini, GPT, local models), 
Cowork-specific patterns don't transfer.

InGit's structure is platform-agnostic. Same project works 
with any AI that has appropriate MCP server or plugin. This 
prevents lock-in to specific AI provider.

### 3.8. Migration and Interoperability

Cowork has connectors to specific services but not migration 
tools to convert between project structures.

InGit can include migration tools:
- Import from Notion (preserve structure where possible)
- Import from Obsidian (preserve linking)
- Import from GitHub Issues + Wiki
- Export to standard formats (Markdown + YAML)

This makes InGit useful as **interoperability hub** for users 
working across multiple systems.

### 3.9. What This Means

InGit's value when paired with Cowork is concentrated in:
- Structured workspace conventions
- Metadata as code
- Git-native versioning conventions
- Validation infrastructure
- Encryption layer
- Offline operation
- Cross-platform portability

These are exactly the "substrate" qualities. InGit is the 
ground on which Cowork operates effectively.

---
