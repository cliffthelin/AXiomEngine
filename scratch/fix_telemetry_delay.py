import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Modify roi_telemetry_loop to log immediately
old_loop = """    async def roi_telemetry_loop(self):
        while True:
            await asyncio.sleep(1800) # 30 minutes
            self.log_roi_snapshot()"""

new_loop = """    async def roi_telemetry_loop(self):
        # Log baseline immediately
        self.log_roi_snapshot()
        while True:
            await asyncio.sleep(1800) # 30 minutes
            self.log_roi_snapshot()"""

content = content.replace(old_loop, new_loop)

path.write_text(content)
print("ROI Telemetry loop updated to log baseline immediately on startup.")
