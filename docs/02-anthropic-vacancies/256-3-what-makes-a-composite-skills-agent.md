# 3. What Makes a Composite Skills Agent

<!-- summary -->
> We define the type with precision.

---
<!-- tags: rag, ingestion, architecture, self-improve -->




## 3. What Makes a Composite Skills Agent

We define the type with precision.

### 3.1. Defining Properties

A Composite Skills Agent has eight defining properties.

**Property 1 — Configurable Sub-Agent Set.** The composite 
agent draws on a specified set of narrow-specialist sub-agents, 
selected by the principal (with possible AI assistance) from a 
larger registry. The set is the configuration.

**Property 2 — Sub-Agents Are Individually General.** Each 
sub-agent in the configuration is a Type 1-style Professional 
Colleague Agent for a narrow specialization, shared across 
all principals who need that specialization. Sub-agents are 
not built per-principal.

**Property 3 — Configuration Is Individually Specific.** While 
each sub-agent is general, the specific combination belongs to 
the principal. A different principal would have a different 
configuration even within the same general profession.

**Property 4 — Coordinated Single-Surface Interaction.** The 
principal interacts with the composite agent as a coherent 
whole, not with each sub-agent separately. The composite agent's 
job is to route, coordinate, and integrate.

**Property 5 — Transparent Source Attribution.** When outputs 
draw on specific sub-agents, the principal can see which 
sub-agents contributed what. Attribution is preserved, not 
hidden.

**Property 6 — Disagreement Surfacing.** When sub-agents 
disagree (which is normal and informative), the composite agent 
surfaces the disagreement to the principal rather than masking 
it through averaging or arbitration.

**Property 7 — Configuration Evolution.** The principal can 
add or remove sub-agents over time as their specializations 
develop. The configuration is not static.

**Property 8 — Principal Authorship Preserved.** Despite drawing 
on many sub-agents, the principal remains the author of their 
work. Sub-agents inform; the principal decides and produces.

### 3.2. What a Composite Skills Agent Does

The composite agent provides four core functions:

**Function 1 — Routing.** When the principal poses a question 
or task, the composite agent determines which sub-agents are 
relevant. Some questions need only one sub-agent. Others need 
several in combination. Some need a specific sequence (one 
sub-agent's output feeds into another).

**Function 2 — Synthesis.** When multiple sub-agents contribute 
to a response, the composite agent integrates their outputs 
into a coherent whole — without obscuring which sub-agent 
contributed what.

**Function 3 — Disagreement Management.** When sub-agents 
provide conflicting recommendations, the composite agent 
presents the disagreement clearly to the principal: "Sub-agent 
A recommends X for these reasons; sub-agent B recommends Y for 
these reasons." The principal decides.

**Function 4 — Configuration Maintenance.** Over time, the 
composite agent helps the principal evaluate their configuration: 
which sub-agents are most used, which are underutilized, which 
specializations might be worth adding given the principal's 
work patterns.

### 3.3. What a Composite Skills Agent Does NOT Do

Like other agent types, what the composite agent **does not do** 
is equally important.

**Not invent specializations.** The composite agent does not 
create new sub-agents. It draws from the existing registry. 
Sub-agent creation is a separate process involving expert 
curation.

**Not replace principal judgment.** When sub-agents disagree, 
the composite agent does not decide. The principal decides, 
informed by visible disagreement.

**Not hide its workings.** The composite agent does not present 
synthesized outputs as if from a single source. Attribution 
is preserved.

**Not build permanent fixed configurations.** The configuration 
is meant to evolve. The composite agent does not lock the 
principal into an unchangeable set.

**Not act externally.** Like Professional Colleague Agents, the 
composite agent works inside the principal's professional 
practice. External representation is the role of Representative 
Agents (Type 4).

### 3.4. The Twenty-Sub-Agents Constraint

The yoga metaphor suggests around twenty as a meaningful number. 
Why?

A configuration of two or three sub-agents is too narrow — it 
duplicates what specialized Professional Colleague Agents 
already do.

A configuration of fifty or a hundred sub-agents becomes 
unmanageable — coordination overhead exceeds benefit.

Empirically, complex skilled practice typically draws on between 
ten and thirty specializations. This range matches the 
cognitive bandwidth of human practitioners and the operational 
capacity of coordinating layers.

We suggest twenty as a reasonable working constraint: 
configurations under five are probably better served by Type 1; 
configurations over forty are probably indicating a need for 
narrower focus or different agent type.

### 3.5. The Coordinator-Within-Configuration Pattern

A subtle architectural point: the composite agent itself is 
**not** another specialist sub-agent. It is a coordinator.

This means:
- The coordinator does not have profession-specific expertise
- The coordinator's expertise is in routing, synthesis, 
  disagreement management
- Different principals can use the same coordinator with 
  different configurations
- The coordinator is general; the configurations it manages 
  are specific

This is analogous to how an orchestra conductor is not another 
musician with their own instrument. The conductor's expertise 
is coordination of musicians, not playing music. Composite 
agents inherit this distinction.

---
