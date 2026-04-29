# 4. Proposed Infrastructure

<!-- summary -->
> OKWF infrastructure consists of six interlocking layers. Each

---



## 4. Proposed Infrastructure

OKWF infrastructure consists of six interlocking layers. Each 
layer has reference implementation (open source), operational 
component (foundation-staffed), and community component 
(contributor-governed).

### 4.1. Technical Substrate: Nautilus Portal Protocol

**Reference implementation**: `github.com/svend4/nautilus` (v1.1)

**What it provides**:
- Federated knowledge storage across heterogeneous formats
- Adapter-based access to diverse knowledge sources
- Unified coordinate space (Q6) for concepts
- Consensus model for conflict resolution
- REST API, SDK, MCP integration
- Open specification enabling alternative implementations

**Why Nautilus over alternatives**:
- Already exists and demonstrably works
- Zero external dependencies (auditable, portable)
- Federation-over-merging principle aligns with foundation values
- Humanities extension in development
- Author-maintained and open source

**Extensions required for OKWF**:
- Agent registry (AI assistants and meta-agents as first-class 
  participants)
- Task protocol (formal task objects with lifecycle)
- Role protocol (first-class roles and scope)
- Identity and reputation extensions

Implementation timeline: 6-9 months from funding to production-ready 
for pilot.

### 4.2. Coordination Pattern: Double-Triangle Architecture

**Reference document**: `THE-DOUBLE-TRIANGLE-ARCHITECTURE.md` 
(available on request)

**What it provides**:
- Formal model for human-AI collaboration preserving human 
  agency
- Three inter-layer protocols (Human↔Assistants, 
  Meta-agent↔Human, Assistant↔Meta-agent negotiation)
- Fractal self-similarity supporting arbitrary organizational 
  scale
- Six architectural invariants ensuring dignified collaboration

**Why Double-Triangle for OKWF**:
- Explicitly designed for single contributors in distributed 
  teams
- Preserves contributor autonomy (lower triangle)
- Enables coordination at scale (upper triangle)
- Compatible with any AI capability level (degrades gracefully)

**Application to OKWF**:
- Each contributor = Node with personal AI assistants (lower 
  triangle)
- Guild-level coordination via meta-agent (upper triangle)
- Cross-guild coordination via higher-level meta-agents (fractal)
- Foundation staff provide meta-meta coordination where 
  required

### 4.3. Knowledge Layer: Pattern Library with Private Instances

**Reference document**: Described in Nautilus humanities 
extension and Double-Triangle document

**What it provides**:
- Two-tier knowledge structure: public patterns + private 
  instances
- Three bridge types: inheritance, citation, contribution
- Anonymization pipeline enabling privacy-preserving sharing
- Version control and update propagation

**Why pattern library is critical**:
- Compounds knowledge across contributors
- Enables specialized work without reinvention
- Preserves contributor intellectual property through 
  anonymization
- Creates foundation's unique asset over time

**Application to OKWF**:
- Public patterns maintained by foundation and guilds
- Private instances held by individual contributors
- Anonymization pipeline operated by foundation with contributor 
  consent
- Contribution credits toward reputation and bonuses

### 4.4. Community Layer: Guild Structure

**What it is**: Persistent professional communities organized 
by specialization.

**Proposed initial guilds**:
- **Legal Writing Guild** — German/EU social and disability 
  law documentation
- **Science Communication Guild** — arxiv paper translation 
  and summarization
- **Medical Documentation Guild** — healthcare system 
  documentation and translation
- **Technical Writing Guild** — software documentation, 
  educational materials
- **Code Review Guild** — open-source code review for specified 
  projects
- **Research Synthesis Guild** — literature review and synthesis

**Guild functions**:
- Skill validation and graduation
- Mentorship (senior contributors guide juniors)
- Quality assurance (peer review of outputs)
- Project formation (teams assemble for specific engagements)
- Community governance (guild-internal decisions)

**Graduation structure**:
- Level 0: Onboarding quests (2-4 weeks)
- Level 1: Simple structured tasks (3-6 months)
- Level 2: Specialized work (6-18 months)
- Level 3: Project participation (ongoing)
- Level 4: Project leadership (elected or merit-based)
- Level 5: Guild leadership (elected)

### 4.5. Economic Layer: Subsidiarity-Based Compensation

**Principles**:
- **Dignified baseline**: all active contributors receive 
  stipend meeting minimum threshold
- **Contribution bonuses**: measurable high-impact work 
  generates additional compensation
- **Long-term incentives**: reputation and credentials 
  translate into tangible benefits
- **No full-replacement income**: contributors retain other 
  life activities

**Proposed structure**:
- **Base stipend**: €500-1500/month for active contributors 
  (depending on region cost-of-living)
- **Project bonuses**: €500-5000/project for specific deliverables
- **Revenue sharing**: when projects serve paying clients, 
  substantial share flows to contributors
- **Milestone awards**: guild-level recognition with tangible 
  credentials

**Why subsidiarity is right model**:
- Below full-salary level preserves other life activities 
  (elders, disabled, caregivers)
- Above charity level preserves dignity and agency
- Predictable baseline allows planning
- Variable bonus allows excellence recognition

**Funding sources**:
- Corporate sponsorships (core unrestricted funds)
- Grant funding (project-specific)
- Client payments (commercial projects)
- Foundation endowment (eventual self-sustaining core)

### 4.6. Legal and Compliance Layer

**What it provides**:
- Single contractual interface for contributors (across 
  jurisdictions)
- Tax compliance infrastructure
- GDPR-compliant data handling
- Dispute resolution process
- Intellectual property framework

**Mechanism**:
- OKWF foundation provides EoR-equivalent services
- AI-assisted compliance automation reduces costs 10x vs. 
  existing platforms
- Modular legal templates for different engagement types
- Clear IP ownership model (default: contributor retains rights; 
  project-specific exceptions with transparent terms)

### 4.7. Integration

All six layers integrate:

- Contributors log in (community identity), pick up tasks 
  (guild structure, pattern library), execute work (Nautilus 
  substrate + Double-Triangle with assistants), receive 
  compensation (economic layer handled by legal layer).

Foundation staff operate:
- Technical infrastructure
- Initial pattern curation
- Legal and compliance
- Funding relationships

Community governance operates:
- Guild-level quality gates
- Mentorship programs
- Strategic input to foundation leadership

---
