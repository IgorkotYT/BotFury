import argparse
import sys
import time

parser = argparse.ArgumentParser(description="Dummy Minecraft bot")
parser.add_argument("--bot_id", type=int, required=True)
parser.add_argument("--server_ip", required=True)
args = parser.parse_args()

print(f"[Bot {args.bot_id}] Connected to {args.server_ip}")
sys.stdout.flush()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line == "stop":
        print(f"[Bot {args.bot_id}] Stopping")
        sys.stdout.flush()
        break
    else:
        print(f"[Bot {args.bot_id}] Received command: {line}")
        sys.stdout.flush()
    time.sleep(0.1)
