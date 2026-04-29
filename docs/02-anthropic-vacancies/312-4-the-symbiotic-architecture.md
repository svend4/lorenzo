# 4. The Symbiotic Architecture

## 4. The Symbiotic Architecture

The combination of InGit and Cowork creates an architecture 
neither alone provides.

### 4.1. Layer Decomposition

Working from substrate up:

```
LAYER 0 — Hardware and OS
  Local computer, optionally NAS
                ↓
LAYER 1 — File System
  Operating system file storage
                ↓
LAYER 2 — InGit Substrate
  Structured folders (00_inbox through 90_exports)
  YAML metadata schemas
  Git-native versioning conventions
  Validation hooks
  Encryption for sensitive folders
                ↓
LAYER 3 — Cowork Agent
  Persistent memory scoped to Project
  Multi-step task execution
  MCP connector integration
  Computer use capability
  Scheduled recurring tasks
                ↓
LAYER 4 — User and External Tools
  User direct interaction with files
  External services (GitHub, Notion, etc.)
  Other AI tools when needed
  Other team members (limited; Cowork is local)
```

Each layer has clear responsibilities. Each layer provides 
abstractions to layers above.

### 4.2. How They Interact

A typical workflow combines them:

**1. User opens Cowork Project pointing at InGit folder.**

**2. User states intent**: "Write a draft section on X based 
on existing materials."

**3. Cowork agent begins**:
- Reads InGit Project structure (knows convention)
- Searches `80_wiki/` for relevant existing knowledge
- Reads referenced documents in `30_documents/`
- Drafts new content following InGit document template
- Adds appropriate YAML metadata
- Validates through InGit MCP server (if configured) or 
  inline
- Saves to appropriate location
- Updates timeline in `20_timeline/` if convention requires
- Commits with conventional commit message

**4. User reviews**:
- Sees draft in correct location
- Reviews metadata
- Approves or requests revisions

**5. Iteration continues** with Cowork remembering context 
between sessions.

This is fundamentally different from either:
- Chat alone: no persistence beyond chat, no structure
- Cowork alone with generic folder: no structure conventions
- InGit alone: no agent intelligence

### 4.3. Where Each Operates

InGit Substrate operates whenever:
- Files are read or written
- Git operations occur
- Validation runs
- Encryption applies
- Structure conventions enforced

Cowork Agent operates whenever:
- Multi-step tasks execute
- AI synthesis happens
- External services accessed
- Memory recalled
- Scheduled tasks run

User operates whenever:
- Intent expressed
- Outputs reviewed
- Decisions made
- Direct edits performed
- Strategy set

The three operate concurrently. None requires the others' 
constant presence (offline operation continues without Cowork; 
Cowork can work with non-InGit folders; user delegates to 
both).

### 4.4. Shared State

Critical implementation point: shared state between InGit and 
Cowork must be **deterministic and recoverable**.

**Determinism**: Given the same project state and same Cowork 
instructions, results should be predictable. Validation 
prevents Cowork from creating malformed artifacts.

**Recoverability**: All state lives in files (Git tracked). 
Even if Cowork session is lost, Project state recoverable from 
filesystem. Memory can be rebuilt by replaying Git history 
through Cowork.

This is why Git-native is important: Git provides authoritative 
state. Cowork memory is convenience, not authority.

---
