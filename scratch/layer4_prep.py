import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Add vectorization prep to stats
content = content.replace('"tdd_alignment": 0', '"tdd_alignment": 0,\n                "vectorization_prep": 0')

# 2. Add vectorization prep task to process_single_instance_swarm
# This simulates the extraction of high-fidelity semantic tokens for future embedding
vec_logic = """
                # Agent 5: The Semantic Vectorizer (Future Layer 4 Readiness)
                # Extracts high-fidelity tokens for vector store ingestion
                self.stats["sub_tasks"]["vectorization_prep"] += 1
                metadata["vector_tokens"] = list(set(re.findall(r"[A-Z]{3,}", metadata.get("ai_dissertation", {}).get("content", ""))))[:50]
"""

content = content.replace('self.save_to_catalog(rule, metadata, interfaces, tagging, tests, start_time, end_time)', vec_logic + '\n                self.save_to_catalog(rule, metadata, interfaces, tagging, tests, start_time, end_time)')

# 3. Update ROI snapshot for Layer 4
content = content.replace('  - TDD Alignment:         {self.stats["sub_tasks"]["tdd_alignment"]}', '  - TDD Alignment:         {self.stats["sub_tasks"]["tdd_alignment"]}\n  - Vectorization Prep:    {self.stats["sub_tasks"]["vectorization_prep"]}')

path.write_text(content)
print("Layer 4 Vectorization Readiness integrated. Every rule is now pre-processed for Evolutionary Intelligence.")
