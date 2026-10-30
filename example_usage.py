# -*- coding: utf-8 -*-
from client import OpenClawGenParkDocProcessor

proc = OpenClawGenParkDocProcessor()

doc = """# Agentic Commerce Protocol
Autonomous trading network built upon Model Context Protocol.

## Architecture
The system employs decentralized smart contracts and off-chain state channels.
Agents communicate via standardized JSON-RPC protocols.

### Security
Zero-knowledge proofs verify execution state without revealing trade secrets.
Multi-signature escrows lock collateral securely.
"""

# 1. Markdown Hierarchy DAG
dag = proc.parse_markdown_header_hierarchy_dag(doc)
print(f"Hierarchy DAG: {dag['total_sections']} sections parsed (Max depth={dag['max_header_depth']})")
for s in dag['sections']:
    print(f"  Level {s['level']}: {s['title']} ({s['word_count']} words)")

# 2. Sliding Window Chunking
chunks_res = proc.partition_document_by_sliding_window(doc, chunk_size_words=15, overlap_words=3)
print(); print(f"Sliding Window: {chunks_res['total_chunks']} chunks generated (Overlap={chunks_res['overlap_retention_ratio']})")

# 3. Context Budget Packing
packing = proc.compute_lexical_token_budget_packing(chunks_res['chunks'], max_context_budget_words=25)
print(); print(f"Token Budget Packing: {packing['total_windows']} windows (Avg Utilization: {packing['average_utilization_pct']}%)")
