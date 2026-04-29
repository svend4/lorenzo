# 2. The Double-Triangle Architecture

## 2. The Double-Triangle Architecture

### 2.1. Topology

We formalize the architecture using two triangles sharing a common 
vertex:

**Lower triangle** (per human Node N):

```
                    N
                  / | \
                 /  |  \
                /   |   \
             A_1  A_2   A_3
```

where `A_1, A_2, A_3` are AI assistants personalized to N's work. 
N conducts the triangle: tasks flow downward from N to assistants, 
results flow upward from assistants to N for integration.

**Upper triangle** (per team or project T):

```
                   M
                  / | \
                 /  |  \
                /   |   \
             N_1   N_2   N_3
```

where `M` is a meta-agent (AI or human-augmented-AI) and 
`N_1, N_2, N_3` are human participants. M conducts the upper 
triangle: tasks flow downward from M to humans, deliverables flow 
upward from humans to M for integration.

**Composition.** Each human N is **simultaneously** the vertex of 
a lower triangle (their own) and a base node of an upper triangle 
(their team's). Superimposing the two around this shared vertex 
produces a six-pointed star:

```
                    M
                  / | \
                 /  |  \
              N_1  [N]  N_3
                  / | \
                 /  |  \
              A_1  A_2  A_3
```

We refer to this as the **Star of David topology**, after the 
hexagram figure. The metaphor is deliberate: two superimposed 
triangles pointing in opposite directions, sharing common vertices.

### 2.2. Fractal Self-Similarity

The architecture is fractal: the meta-agent M itself participates 
as a Node in a higher-level upper triangle (e.g., at the 
organization level). M has its own lower triangle of assistants 
supporting its coordination work. Recursively, any scale of 
organization can be represented as stacked Star-of-David topologies.

Formally, if `Star(k)` is the topology at level `k`:
- `Star(0)`: individual human + personal assistants (lower triangle only, no upper)
- `Star(1)`: individual embedded in team (full Star, as depicted)
- `Star(2)`: team lead embedded in organization (full Star at higher scale)
- `Star(n)`: recursively

This fractal property means the protocol for inter-layer 
communication scales naturally: the same three protocols 
(introduced in §3) apply at every level.

### 2.3. Six Architectural Invariants

A system implementing the Double-Triangle Architecture must 
satisfy six invariants:

**Invariant 1 — Dual Identity.** Each human Node maintains two 
separate identity contexts: *personal context* (their 
work-in-progress, drafts, notes, private patterns) and *team 
context* (their accepted deliverables, public roles, shared 
outputs). Personal context is richer; team context is filtered.

**Invariant 2 — Assistant Autonomy, Node Authority.** Lower 
triangle assistants have broad autonomy to execute tasks within 
their scope, but the human Node retains final authority on what 
propagates upward to team context. Assistants cannot 
unilaterally publish to team-visible space.

**Invariant 3 — Meta-Agent Transparency, Not Omniscience.** The 
meta-agent M can see all team-context data from all Nodes, but 
cannot see personal-context data of any Node. Its decisions must 
be explainable in terms of team context alone.

**Invariant 4 — Multi-Level Consensus.** Conflicts can be resolved 
at three levels: within a Node's lower triangle (between their 
assistants), between Nodes at the upper triangle, or at escalation 
points that involve human judgment. Each level uses the same 
consensus mechanism with different parameters.

**Invariant 5 — Distributed Audit Trail.** Every cross-triangle 
communication is logged in at least two locations: the originating 
triangle and the receiving triangle. This enables reconstruction 
of decision chains without centralized logging.

**Invariant 6 — Fractal Compatibility.** Any protocol valid at one 
level of the hierarchy must remain valid at all levels. This 
ensures the architecture scales from small teams (Star(1)) to 
large organizations (Star(n)) without protocol changes.

---
