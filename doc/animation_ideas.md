# Animation Ideas

100 ideas for teaching animations, grouped by topic. Each is one short
self-contained explainer in the spirit of `syscall.py` and `clock.py`.

## Operating Systems — kernel & process model (10)

1. **fork** — duplicating a process, copy-on-write pages, parent/child diverging on the return value of `fork()`.
2. **exec** — replacing the current image: argv/envp passed to the new program, file descriptors that survive.
3. **wait / zombie / orphan** — exit codes parked in the process table, reaped by the parent, adopted by init.
4. **signals** — kernel queues a signal, delivers it on the next return to user space, default vs custom handler.
5. **pipes** — kernel buffer with a read end and a write end, blocking when full or empty.
6. **page table walk** — virtual address split into PGD/PUD/PMD/PTE indices, MMU walking each level to find a physical frame.
7. **TLB hit and miss** — fast path through the TLB cache vs the slow page-table walk on a miss.
8. **page fault** — invalid PTE → trap → kernel loads the page from disk → restart the faulting instruction.
9. **copy-on-write after fork** — both processes share read-only pages until one writes, then the kernel duplicates that page.
10. **mmap vs read** — file-backed mapping, lazy paging in, vs the explicit syscall + buffer copy.

## Operating Systems — concurrency & scheduling (10)

11. **race condition** — two threads incrementing a counter, the lost-update problem, machine-code interleaving.
12. **mutex** — atomic test-and-set lock, the queue of waiters, hand-off on unlock.
13. **semaphore** — counting permits, producers and consumers, blocking when the counter hits zero.
14. **deadlock** — four philosophers, each holding one chopstick and waiting for the next.
15. **priority inversion** — low-priority task holds a lock that a high-priority task needs, fixed by priority inheritance.
16. **CFS (Linux scheduler)** — red-black tree keyed on virtual runtime, picking the leftmost task.
17. **context switch cost** — saving registers, switching page tables, flushing the TLB, refilling the cache.
18. **kernel vs user threads** — m:n model, what the kernel sees vs what the runtime sees.
19. **futex** — fast user-space lock, only enters the kernel when there is actual contention.
20. **read-copy-update (RCU)** — readers never block, writers publish a new version atomically, old versions reclaimed later.

## Operating Systems — I/O & filesystems (8)

21. **VFS dispatch** — the same `read()` going to ext4, NFS, or `/proc` via the file_operations table.
22. **inode vs dentry** — the on-disk metadata vs the in-memory name cache.
23. **block I/O scheduler** — requests merged and reordered by the elevator before reaching the disk.
24. **direct I/O vs page cache** — the page cache layer between user buffers and the disk, and what `O_DIRECT` skips.
25. **journaling filesystem** — write-ahead log entry, then the actual blocks, recovery after a crash.
26. **inotify** — kernel watch on an inode, events queued and delivered to user-space.
27. **epoll** — readiness-based event loop, the interest list and the ready list, edge vs level triggered.
28. **io_uring** — submission and completion queues shared between user and kernel, no syscall per I/O.

## Operating Systems — memory (6)

29. **virtual memory layout** — text, data, BSS, heap growing up, stack growing down, mmap region in the middle.
30. **slab allocator** — per-size caches of pre-built objects, avoiding fragmentation for fixed-size kernel allocations.
31. **buddy allocator** — splitting and coalescing power-of-two blocks of physical pages.
32. **swapping** — least-recently-used pages evicted to disk, brought back on the next fault.
33. **OOM killer** — scoring processes by memory pressure and killing the worst offender.
34. **NUMA** — CPU cores with their own local memory banks, the cost of accessing a remote node.

## Networking — protocols (8)

35. **TCP three-way handshake** — SYN, SYN-ACK, ACK, with sequence numbers visible.
36. **TCP congestion control** — slow start, congestion avoidance, the sawtooth window.
37. **TCP retransmission** — an ACK never arrives, the timer fires, the segment is sent again.
38. **DNS resolution** — recursive resolver walking the root, TLD, and authoritative servers.
39. **TLS handshake** — client hello, key exchange, certificate, change cipher spec.
40. **NAT traversal** — private IPs rewritten by the home router, port mapping table, return path.
41. **IP fragmentation** — a packet larger than the path MTU split, reassembled at the destination.
42. **packet through the stack** — Ethernet → IP → TCP → socket buffer → application read.

## C — language mechanics (10)

43. **stack frame** — function call pushes a frame, locals laid out, return address saved, frame pointer chain.
44. **calling convention** — first six args in registers (System V), rest on the stack, return value in rax.
45. **pointer arithmetic** — `p + 1` advances by `sizeof(*p)`, not by one byte.
46. **array decay** — `int a[5]` decaying to `int *` when passed to a function, sizeof difference.
47. **strings as arrays** — character buffer with a null terminator, what happens without one.
48. **struct padding** — fields aligned to their size, padding bytes inserted, total size rounded up.
49. **union memory layout** — all members sharing the same bytes, the type punning idiom.
50. **bit fields** — packing flags into a single integer, endianness gotchas.
51. **function pointers** — pointer holding a code address, used as a vtable for polymorphism.
52. **variadic functions** — `va_list` walking the stack, the printf format string driving the walk.

## C — memory & undefined behavior (8)

53. **malloc and free** — the heap, free list, splitting and coalescing.
54. **buffer overflow** — writing past the array, smashing the saved return address, control-flow hijack.
55. **use-after-free** — pointer kept after the heap region was reused.
56. **double free** — corrupting the allocator's free list.
57. **dangling stack pointer** — returning the address of a local variable.
58. **strict aliasing** — why casting a `float *` to `int *` is undefined, and what the optimizer does with that.
59. **integer overflow** — signed wraparound is undefined; unsigned wraps cleanly.
60. **uninitialized read** — reading a local before assignment, what compilers may assume.

## Compilation & linking (6)

61. **preprocessor** — `#include` and macro expansion before the compiler ever sees C.
62. **compilation pipeline** — `.c` → preprocessed → assembly → object → executable.
63. **static vs dynamic linking** — symbols resolved at link time vs by the loader at start.
64. **PLT and GOT** — lazy symbol resolution at first call to a shared library function.
65. **ELF segments** — text, data, rodata, .bss; what the loader maps into memory.
66. **ASLR** — randomized base addresses for stack, heap, and shared libraries on each run.

## CPU & low-level (8)

67. **pipeline stages** — fetch, decode, execute, memory, writeback, instructions overlapping in flight.
68. **branch prediction** — guessing the direction of a conditional, the cost of a misprediction.
69. **out-of-order execution** — instructions issued in order, executed when their inputs are ready, retired in order.
70. **cache hierarchy** — L1, L2, L3, main memory, latency at each level.
71. **cache line and false sharing** — two threads writing different variables on the same line, ping-ponging it.
72. **memory ordering** — store buffer, why one CPU sees writes in a different order than another.
73. **atomic compare-and-swap** — building a lock-free counter on top of CAS.
74. **interrupt vs trap vs fault** — asynchronous external signal vs synchronous instruction-caused entry into the kernel.

## Data structures & algorithms (10)

75. **hash table collisions** — chaining vs open addressing, load factor and resize.
76. **B-tree insertion** — leaf split propagating up, why databases love it for disk.
77. **red-black tree rotations** — recoloring and rotating to restore the invariants after insert.
78. **heap (priority queue)** — sift-up on insert, sift-down on extract-min.
79. **union-find** — path compression and union by rank, near-constant amortized cost.
80. **bloom filter** — multiple hash functions, bit array, false positives but never false negatives.
81. **skip list** — randomized layered linked list, expected log-n search.
82. **trie** — prefix tree for autocomplete, edges labelled by characters.
83. **LRU cache** — doubly linked list plus hash map, O(1) get and put.
84. **consistent hashing** — keys and nodes on a ring, minimal reshuffling when a node joins or leaves.

## Big data & distributed systems (10)

85. **MapReduce** — input split, mapper output, shuffle, reducer aggregation.
86. **HDFS write** — client → NameNode for block placement → pipeline of DataNodes for replication.
87. **Spark RDD lineage** — lazy transformations forming a DAG, recomputed from the source on failure.
88. **Kafka log** — append-only partitioned log, offsets, consumer groups, retention.
89. **Paxos / Raft leader election** — terms, votes, log replication, commit when a majority acks.
90. **two-phase commit** — coordinator's prepare/commit phases, what blocks if the coordinator fails.
91. **CAP theorem** — partitioned network, choosing between consistency and availability with a worked example.
92. **vector clocks** — concurrent edits to the same key, how vector clocks detect conflicts.
93. **Merkle tree** — hash of hashes, used by Git, Cassandra, and Bitcoin to detect divergence cheaply.
94. **gossip protocol** — random peer selection, exponential spread of state through the cluster.

## Security (6)

95. **stack smashing protection (canaries)** — a known value before the saved return address, checked on return.
96. **return-oriented programming** — chaining gadgets ending in `ret` to bypass W^X.
97. **TOCTOU** — `access()` then `open()`, the attacker swaps the file in between.
98. **Diffie-Hellman key exchange** — public mixing of colors as the metaphor, shared secret without sending it.
99. **HMAC** — keyed hash for integrity, why a plain hash isn't enough.
100. **Spectre / branch-predictor side channel** — speculative load past a bounds check, leaving traces in the cache.
