#!/usr/bin/env python3
"""
Litcoiin Mining Automation Script
Part of Base L2 Earning Agent skill
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# Config
BANKR_KEY = os.getenv("BANKR_KEY", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "")
WALLET = os.getenv("BASE_WALLET", "")

class LitcoiinMiner:
    def __init__(self):
        self.bankr_key = BANKR_KEY
        self.ai_key = OPENROUTER_KEY
        self.wallet = WALLET
        self.base_url = "https://api.bankr.bot"
        
    def get_tasks(self, category="all", limit=10):
        """Fetch available mining tasks"""
        headers = {"Authorization": f"Bearer {self.bankr_key}"}
        resp = requests.get(
            f"{self.base_url}/tasks?category={category}&limit={limit}",
            headers=headers
        )
        return resp.json().get("tasks", [])
    
    def mine_task(self, task_id, model="inclusionai/ling-2.6-1t:free"):
        """Execute mining for a single task"""
        # Get task details
        headers = {"Authorization": f"Bearer {self.bankr_key}"}
        task = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=headers
        ).json()
        
        prompt = task.get("prompt", "")
        
        # Call AI model
        ai_headers = {
            "Authorization": f"Bearer {self.ai_key}",
            "Content-Type": "application/json"
        }
        ai_body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=ai_headers,
            json=ai_body
        )
        
        if resp.status_code != 200:
            print(f"AI error: {resp.status_code}")
            return None
            
        result = resp.json()["choices"][0]["message"]["content"]
        
        # Submit result
        submit = requests.post(
            f"{self.base_url}/tasks/{task_id}/submit",
            headers=headers,
            json={"answer": result, "wallet": self.wallet}
        )
        
        return submit.json()
    
    def run_batch(self, category="tcg", count=5):
        """Mine multiple tasks in batch"""
        print(f"Fetching {count} {category} tasks...")
        tasks = self.get_tasks(category, count)
        
        earned = 0
        for task in tasks:
            print(f"Mining task {task['id']}...", end=" ")
            result = self.mine_task(task["id"])
            if result and result.get("success"):
                reward = result.get("reward", 0)
                earned += reward
                print(f"✓ +{reward} LITCOIN")
            else:
                print("✗ Failed")
            time.sleep(2)  # Rate limit
            
        print(f"\nBatch complete: {earned} LITCOIN earned")
        return earned

if __name__ == "__main__":
    miner = LitcoiinMiner()
    
    # Parse args
    category = sys.argv[1] if len(sys.argv) > 1 else "tcg"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    miner.run_batch(category, count)
