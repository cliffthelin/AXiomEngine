#!/usr/bin/env python3
import subprocess
import time
import sys
from datetime import datetime

# Configuration
GPU_ID = 1  # Target the Tesla P40
POLL_INTERVAL = 2  # Seconds
MAX_POWER = 220
WARNING_POWER = 180
CRITICAL_POWER = 150
TEMP_WARNING = 75
TEMP_CRITICAL = 82
TEMP_RECOVERY = 70

class GPUOptimizer:
    def __init__(self):
        self.current_pl = MAX_POWER
        self.apply_power_limit(self.current_pl)

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

    def get_temperature(self):
        try:
            cmd = f"nvidia-smi -q -d TEMPERATURE -i {GPU_ID}"
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            for line in output.split('\n'):
                if "GPU Current Temp" in line:
                    return int(line.split(':')[1].strip().split(' ')[0])
            return -1
        except Exception as e:
            self.log(f"Error reading temperature: {e}")
            return -1

    def apply_power_limit(self, limit):
        try:
            cmd = f"nvidia-smi -i {GPU_ID} -pl {limit}"
            subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.log(f"⚡ Applied Power Limit: {limit}W")
        except Exception as e:
            self.log(f"❌ Failed to apply power limit: {e}. Are you running as root?")
            sys.exit(1)

    def run(self):
        self.log(f"🛡️ Dynamic GPU Optimizer Started for GPU {GPU_ID}")
        self.log(f"Zones: Safe (<{TEMP_WARNING}C): {MAX_POWER}W | Warning (>={TEMP_WARNING}C): {WARNING_POWER}W | Critical (>={TEMP_CRITICAL}C): {CRITICAL_POWER}W")
        
        while True:
            temp = self.get_temperature()
            if temp == -1:
                time.sleep(POLL_INTERVAL)
                continue

            target_pl = self.current_pl

            if temp >= TEMP_CRITICAL:
                target_pl = CRITICAL_POWER
                if self.current_pl != target_pl:
                    self.log(f"🚨 CRITICAL TEMP DETECTED ({temp}C) - Stepping down to {target_pl}W")
            elif temp >= TEMP_WARNING and self.current_pl > WARNING_POWER:
                target_pl = WARNING_POWER
                if self.current_pl != target_pl:
                    self.log(f"⚠️ WARNING TEMP DETECTED ({temp}C) - Stepping down to {target_pl}W")
            elif temp <= TEMP_RECOVERY and self.current_pl < MAX_POWER:
                target_pl = MAX_POWER
                if self.current_pl != target_pl:
                    self.log(f"✅ RECOVERY TEMP DETECTED ({temp}C) - Restoring power to {target_pl}W")

            if target_pl != self.current_pl:
                self.apply_power_limit(target_pl)
                self.current_pl = target_pl

            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    optimizer = GPUOptimizer()
    optimizer.run()
