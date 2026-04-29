# 2. What Cowork Provides That InGit Doesn't Need to Build

## 2. What Cowork Provides That InGit Doesn't Need to Build

If InGit positions to complement Cowork rather than replace 
it, several substantial features can be removed from InGit's 
roadmap. These are now **provided by Cowork**, and InGit 
should not duplicate them.

### 2.1. Agentic Task Execution

Cowork's core capability: agentic multi-step task execution. 
Claude in Cowork can:
- Read multiple files, synthesize information
- Make decisions about approach
- Execute shell commands in isolated VM
- Iterate based on results
- Coordinate sub-agents for parallel work
- Self-verify outputs before reporting

InGit was not planning to build this anyway, but Cowork 
provides the agentic layer that makes structured workspace 
much more valuable.

### 2.2. Persistent Memory Across Sessions

Cowork Projects have scoped memory. Claude remembers within a 
Project across sessions. Sensitive data is excluded. User can 
view, edit, delete remembered content.

This is something InGit might have eventually wanted. Not 
needed now.

### 2.3. UI for Knowledge Work

Cowork provides the user interface for interacting with the 
Project. Files visible. Tasks visible. Memory visible. 
Permission prompts for sensitive operations.

InGit's roadmap originally included Desktop GUI with 
Electron + React. With Cowork as primary interface, **this 
becomes unnecessary**. Saves substantial development effort.

### 2.4. Connector Ecosystem

Cowork integrates with Gmail, Drive, Slack, GitHub, Notion, 
many others. Through MCP, custom connectors can be added.

InGit was not planning to build connectors itself, but 
Cowork's existing ecosystem means an InGit Project can use 
external services freely.

### 2.5. Computer Use Capability

When connectors are unavailable, Cowork can navigate the 
desktop and browser through computer use. This is research 
preview but functional.

For InGit Project workflows, this means even systems without 
APIs can be accessed. This was beyond InGit's planning.

### 2.6. Scheduled Recurring Tasks

Cowork can run scheduled tasks: weekly reports, daily email 
checks, monthly archives. Defined once, executed automatically.

This addresses what InGit's roadmap referred to as "auto-
generated reports."

### 2.7. Cross-Platform Availability

Cowork runs on macOS and Windows (Linux likely eventually). 
Mobile app for task assignment via Dispatch.

InGit's plan to build Desktop GUI for cross-platform support 
becomes unnecessary if Cowork is the primary interface.

### 2.8. What This Removes from InGit Roadmap

If Cowork provides the above, InGit's original roadmap can 
be substantially reduced:

**Remove or defer**:
- Desktop GUI (Electron + React)
- Web UI for project management
- Mobile app
- Persistent memory layer
- Agent execution infrastructure
- Connector framework
- Auto-report generation system

**Keep and focus on**:
- File structure conventions
- YAML metadata as code
- Git-native versioning
- Validation hooks
- Encryption for sensitive data
- Migration tools (from other systems)
- MCP server for InGit operations

This reduces InGit from a full application to a **specialized 
substrate**. Substrate is a much more achievable scope for an 
individual developer or small team.

---
