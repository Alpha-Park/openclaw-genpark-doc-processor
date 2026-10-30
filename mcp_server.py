# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Doc Processor MCP Server
FastMCP standard interface for recursive document chunking and hierarchy DAG synthesis.
"""

import json
from typing import Dict, Any, List
from client import OpenClawGenParkDocProcessor

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("openclaw-genpark-doc-processor")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("openclaw-genpark-doc-processor")

processor = OpenClawGenParkDocProcessor()

@mcp.tool()
def partition_document_by_sliding_window(
    text: str,
    chunk_size_words: int = 200,
    overlap_words: int = 40
) -> str:
    """
    Partitions text into overlapping sliding-window chunks with SHA-256 fingerprints.
    """
    res = processor.partition_document_by_sliding_window(text, chunk_size_words, overlap_words)
    return json.dumps(res, indent=2)

@mcp.tool()
def parse_markdown_header_hierarchy_dag(markdown_text: str) -> str:
    """
    Parses Markdown text into a directed hierarchical DAG of sections (H1 -> H2 -> H3).
    """
    res = processor.parse_markdown_header_hierarchy_dag(markdown_text)
    return json.dumps(res, indent=2)

@mcp.tool()
def compute_lexical_token_budget_packing(
    chunks: List[Dict[str, Any]],
    max_context_budget_words: int = 800
) -> str:
    """
    Greedy first-fit bin-packing of document chunks into context windows.
    """
    res = processor.compute_lexical_token_budget_packing(chunks, max_context_budget_words)
    return json.dumps(res, indent=2)

def main():
    sample = "# Header 1\nIntro text\n## Subheader\nDetailed specifications."
    print("Testing Doc Processor:")
    print(partition_document_by_sliding_window(sample, 10, 2))

if __name__ == "__main__":
    main()
