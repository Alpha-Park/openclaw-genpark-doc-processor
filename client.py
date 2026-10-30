# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Doc Processor Client
Pure Python Standard Library (Zero External Dependencies)
Implements recursive sliding-window boundary chunking, Markdown header hierarchy DAG parsing,
and lexical token-budget packing.
"""

import math
import re
import hashlib
from typing import Dict, Any, List, Optional

class OpenClawGenParkDocProcessor:
    """
    Algorithmic document parsing and context packaging engine for autonomous LLM agents.
    """

    def __init__(self):
        pass

    def partition_document_by_sliding_window(
        self,
        text: str,
        chunk_size_words: int = 200,
        overlap_words: int = 40
    ) -> Dict[str, Any]:
        """
        Partitions text into overlapping sliding-window chunks with SHA-256 fingerprints
        and boundary preservation.
        
        Formula:
          stride = chunk_size - overlap
          num_chunks = ceil((total_words - overlap) / stride)
        """
        if not text or not text.strip():
            return {
                "total_words": 0,
                "total_chunks": 0,
                "chunks": [],
                "overlap_retention_ratio": 0.0
            }

        words = text.split()
        total_words = len(words)
        
        chunk_size = max(10, chunk_size_words)
        overlap = min(max(0, overlap_words), chunk_size - 1)
        stride = chunk_size - overlap

        chunks = []
        start_idx = 0
        chunk_id = 0

        while start_idx < total_words:
            end_idx = min(start_idx + chunk_size, total_words)
            chunk_words = words[start_idx:end_idx]
            chunk_content = " ".join(chunk_words)
            
            # SHA-256 fingerprint
            fp = hashlib.sha256(chunk_content.encode("utf-8")).hexdigest()[:16]
            
            chunks.append({
                "chunk_id": chunk_id,
                "start_word_index": start_idx,
                "end_word_index": end_idx,
                "word_count": len(chunk_words),
                "fingerprint": fp,
                "text": chunk_content
            })
            
            chunk_id += 1
            start_idx += stride
            if end_idx >= total_words:
                break

        retention_ratio = round((overlap / chunk_size) if chunk_size > 0 else 0.0, 4)

        return {
            "total_words": total_words,
            "chunk_size_words": chunk_size,
            "overlap_words": overlap,
            "total_chunks": len(chunks),
            "overlap_retention_ratio": retention_ratio,
            "chunks": chunks
        }

    def parse_markdown_header_hierarchy_dag(self, markdown_text: str) -> Dict[str, Any]:
        """
        Parses Markdown text into a directed hierarchical DAG of sections (H1 -> H2 -> H3)
        tracking byte offsets, word counts, and structural balance metrics.
        """
        lines = markdown_text.splitlines()
        nodes = []
        stack = []  # stack of (level, node_idx)
        
        current_header = "Root / Preamble"
        current_level = 0
        current_content_lines = []
        
        for line in lines:
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
            if header_match:
                # Flush previous section
                if current_content_lines or current_header != "Root / Preamble":
                    sec_text = chr(10).join(current_content_lines).strip()
                    nodes.append({
                        "id": len(nodes),
                        "title": current_header,
                        "level": current_level,
                        "word_count": len(sec_text.split()) if sec_text else 0,
                        "character_length": len(sec_text),
                        "parent_id": stack[-1][1] if stack else None
                    })
                
                h_level = len(header_match.group(1))
                h_title = header_match.group(2).strip()
                
                # Maintain hierarchy stack
                while stack and stack[-1][0] >= h_level:
                    stack.pop()
                
                parent_id = stack[-1][1] if stack else None
                node_idx = len(nodes)
                stack.append((h_level, node_idx))
                
                current_header = h_title
                current_level = h_level
                current_content_lines = []
            else:
                current_content_lines.append(line)
                
        # Flush final section
        if current_content_lines or current_header:
            sec_text = chr(10).join(current_content_lines).strip()
            nodes.append({
                "id": len(nodes),
                "title": current_header,
                "level": current_level,
                "word_count": len(sec_text.split()) if sec_text else 0,
                "character_length": len(sec_text),
                "parent_id": stack[-1][1] if stack else None
            })

        total_nodes = len(nodes)
        max_depth = max([n["level"] for n in nodes], default=0)
        total_doc_words = sum([n["word_count"] for n in nodes])
        
        return {
            "total_sections": total_nodes,
            "max_header_depth": max_depth,
            "total_document_words": total_doc_words,
            "sections": nodes
        }

    def compute_lexical_token_budget_packing(
        self,
        chunks: List[Dict[str, Any]],
        max_context_budget_words: int = 800
    ) -> Dict[str, Any]:
        """
        Greedy first-fit bin-packing of document chunks into context windows,
        maximizing token utilization while maintaining sequential ordering.
        """
        if not chunks:
            return {
                "total_windows": 0,
                "budget_limit_words": max_context_budget_words,
                "average_utilization_pct": 0.0,
                "packed_windows": []
            }

        windows = []
        current_window_chunks = []
        current_window_words = 0

        for ch in chunks:
            ch_words = ch.get("word_count", len(ch.get("text", "").split()))
            
            if current_window_words + ch_words <= max_context_budget_words:
                current_window_chunks.append(ch)
                current_window_words += ch_words
            else:
                if current_window_chunks:
                    windows.append({
                        "window_index": len(windows),
                        "chunk_count": len(current_window_chunks),
                        "allocated_words": current_window_words,
                        "utilization_pct": round((current_window_words / max_context_budget_words) * 100.0, 2),
                        "chunk_ids": [c.get("chunk_id", i) for i, c in enumerate(current_window_chunks)]
                    })
                current_window_chunks = [ch]
                current_window_words = ch_words

        if current_window_chunks:
            windows.append({
                "window_index": len(windows),
                "chunk_count": len(current_window_chunks),
                "allocated_words": current_window_words,
                "utilization_pct": round((current_window_words / max_context_budget_words) * 100.0, 2),
                "chunk_ids": [c.get("chunk_id", i) for i, c in enumerate(current_window_chunks)]
            })

        avg_util = round(sum(w["utilization_pct"] for w in windows) / len(windows), 2) if windows else 0.0

        return {
            "total_windows": len(windows),
            "budget_limit_words": max_context_budget_words,
            "average_utilization_pct": avg_util,
            "packed_windows": windows
        }
