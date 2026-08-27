# Pattern taxonomy

Sixteen patterns, each with one discriminator, the patterns it is genuinely confused with, the
elements that decide correctness, and a template. Element ids come from
[`docs/state-schema.md`](../../docs/state-schema.md) and are global, so a missing `base-case` on
`dp-2d` and a missing `base-case` on `prefix-sum` land in the same bank column.

| pattern | discriminator | tier |
|---|---|---|
| [two-pointers](two-pointers.md) | Does the order let one end move so the objective changes monotonically, making the discarded end permanently safe to drop? | A |
| [sliding-window](sliding-window.md) | Is the answer contiguous, and does extending right make the constraint monotonically harder, so shrinking left is the only repair? | A |
| [binary-search-on-answer](binary-search-on-answer.md) | Is there a predicate over the candidate range that flips from false to true exactly once? | A |
| [hashing](hashing.md) | Can each element be reduced to a key that recovers everything the answer needs about earlier elements in constant time? | A |
| [graph-bfs](graph-bfs.md) | Does the answer depend on the fewest edges to reach something, with every edge costing the same? | A |
| [graph-dfs](graph-dfs.md) | Must a node's answer wait for everything reachable below it, or does the question only need the reachable set enumerated? | A |
| [dp-1d](dp-1d.md) | Is the answer at `i` a function of a bounded set of earlier positions, with no memory of how those were reached? | A |
| [heap-top-k](heap-top-k.md) | Does the algorithm need the current extreme repeatedly while never using the full ordering? | A |
| [prefix-sum](prefix-sum.md) | Is the range quantity a difference of two cumulative values at the endpoints, under an invertible operation? | B |
| [monotonic-stack](monotonic-stack.md) | Does each answer depend only on the nearest neighbour beating it on one side, so nothing between them can ever be an answer? | B |
| [intervals](intervals.md) | Is each input a pair of endpoints on one axis, with the answer depending only on how endpoints interleave? | B |
| [linked-list-pointers](linked-list-pointers.md) | Is position `k` unreachable without `k` steps, forcing the answer to be built from a fixed number of cursors? | B |
| [topological-sort](topological-sort.md) | Are all constraints of the form "A before B", with any respecting order acceptable? | B |
| [union-find](union-find.md) | Is the relation an equivalence that only ever gains members, with queries interleaved between additions? | B |
| [backtracking](backtracking.md) | Does the answer need the candidate objects themselves, each extending by one choice from a shrinking option set? | B |
| [dp-2d](dp-2d.md) | Do two quantities vary independently, so fixing either alone leaves the answer undetermined? | B |

Tier A is eight patterns with the highest question frequency and the widest transfer to patterns
outside the list. Tier B is the remaining eight: still common, but each is closer to a single family
of problem shapes.

## Discriminator, not recognition cue

A recognition cue is a surface feature of the input: sorted array, contiguous substring, tree.
Cues are cheap to memorise and they misfire in both directions. A sorted array appears in problems
where sorting was incidental, and the property that actually licenses two pointers shows up in
arrays nobody sorted.

A discriminator is a falsifiable question about the problem's structure. "Is there a predicate over
the index range that flips from false to true exactly once?" has an answer that can be checked
against the problem before any code is written, and checking it wrong is visible immediately rather
than twenty lines in. Each entry here states one discriminator, then a **Confusable with** table
naming the two or three neighbouring patterns and the test that separates them, because most wrong
answers are a near neighbour rather than a random pattern.

## Interleaving over blocked practice

Blocked practice runs several problems of one pattern in a row. The pattern is already known before
the problem is read, so the only work being done is implementation, and the discriminator is never
exercised. Accuracy inside a block is high and rises across it, which reads as mastery and is
mostly the fluency of a recently repeated motion.

Interleaved practice never places two reps of the same pattern back to back. Every problem starts
with the selection step, which is the step that fails in an interview where nothing announces the
pattern. In-session accuracy drops relative to blocked practice, and retention and transfer both
improve. The rep scheduler in this repo enforces the constraint rather than leaving it to
preference, since the practice that feels worse is the one that measures what an interview measures.
