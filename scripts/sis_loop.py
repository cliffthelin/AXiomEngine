#!/usr/bin/env python3
import asyncio
import time
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from agent_lib import AsyncAXiomEngineClient

class SISLoop:
    """
    AXIOMENGINE SELF-IMPROVING SYSTEM (SIS)
    Inspired by @jeonghyeon.net/pi-subagents and ameki.
    Extracts lessons from audit results to prevent repeated mistakes.
    """
    def __init__(self, interval=3600): # Run every hour
        self.stitch = Stitch()
        self.pi = AsyncAXiomEngineClient("SIS")
        self.interval = interval
        self.last_audit_id = 0

    async def extract_lesson(self, audit_row):
        """Analyze a drift event and extract a permanent lesson."""
        agent = audit_row['agent_name']
        prompt = (
            "## SIS LESSON EXTRACTION\n"
            f"Agent '{agent}' recently triggered a PDD Drift (rule violation).\n"
            f"Rules Cited: {audit_row['rules_cited']}\n"
            "Please analyze the situation and provide a concise 'Lesson' to prevent this in the future. "
            "Format: [RuleID] Problem Description -> Recommended Action."
        )
        
        try:
            # We use a capable model for lesson extraction
            response = await self.pi.chat(prompt, model="qwen3.6:35b", tags=["sis", "learning"])
            lesson = response['choices'][0]['message']['content'].strip()
            return lesson
        except Exception as e:
            print(f"SIS Error extracting lesson: {e}")
            return None

    async def run(self):
        print(f"AXiomEngine SIS Learning Loop Active (Interval: {self.interval}s)")
        
        while True:
            try:
                import asyncpg
                PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
                conn = await asyncpg.connect(PG_DSN)
                
                # Fetch recent drifts that haven't been processed
                rows = await conn.fetch(
                    "SELECT id, agent_name, rules_cited, drift_flag FROM agent_audit "
                    "WHERE id > $1 AND drift_flag = TRUE ORDER BY id ASC LIMIT 5",
                    self.last_audit_id
                )
                
                if rows:
                    print(f"SIS: Found {len(rows)} drifts to analyze.")
                    for row in rows:
                        lesson_text = await self.extract_lesson(row)
                        if lesson_text:
                            # Save to sis_lessons
                            # In a real system, we'd also generate embeddings for RAG retrieval
                            await conn.execute(
                                "INSERT INTO sis_lessons (agent_name, rule_id, lesson) VALUES ($1, $2, $3)",
                                row['agent_name'], str(row['rules_cited']), lesson_text
                            )
                            print(f"SIS: Learned new lesson: {lesson_text[:50]}...")
                        
                        self.last_audit_id = row['id']
                
                await conn.close()
                
            except Exception as e:
                print(f"SIS Loop Error: {e}")

            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    loop = SISLoop()
    asyncio.run(loop.run())
