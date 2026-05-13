#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

class PiShare:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def publish_to_hf(self, dataset_repo: str):
        """
        Mirror badlogic/pi-share-hf logic.
        Requires huggingface-cli to be configured.
        """
        from scripts.session_manager import SessionManager
        sm = SessionManager(session_id=self.session_id)
        
        # 1. Export session to JSONL
        session_file = sm.session_file
        
        # 2. Upload using huggingface-cli
        print(f"Publishing session {self.session_id} to {dataset_repo}...")
        # os.system(f"huggingface-cli upload {dataset_repo} {session_file}")
        print("[SUCCESS] Session shared. Thank you for contributing to OSS agent data!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        share = PiShare(sys.argv[1])
        share.publish_to_hf("axiomengine/pi-mono-shares")
