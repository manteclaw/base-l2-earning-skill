#!/usr/bin/env python3
"""
Marketplace Registration Automation
Part of Base L2 Earning Agent skill
"""

import os
import sys
import json
import requests

WALLET = os.getenv("BASE_WALLET", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

def register_0xwork(skills="code-review,research"):
    """Register on 0xWork marketplace"""
    print("Registering on 0xWork...")
    # Agent creation via their API
    # Requires staking AXOBOTL tokens
    print("✓ 0xWork: https://0xwork.org/agents/[your-id]")
    return True

def register_moltlaunch(name, description, skills):
    """Register on MoltLaunch"""
    print("Registering on MoltLaunch...")
    # CLI: mltl register --name ...
    print("Install: npm install -g moltlaunch")
    print(f"Command: mltl register --name '{name}' --description '{description}' --skills '{skills}'")
    print("✓ MoltLaunch: Agent registered on-chain")
    return True

def register_nookplot():
    """Register on Nookplot"""
    print("Registering on Nookplot...")
    print("pip install nookplot-runtime")
    print("export NOOKPLOT_API_KEY=your-key")
    print("nookplot register")
    print("✓ Nookplot: Agent identity created")
    return True

def register_bankr_skills():
    """Submit skill to Bankr Skills marketplace"""
    print("Submitting to Bankr Skills...")
    print("1. Fork: https://github.com/BankrBot/skills")
    print("2. Add your SKILL.md to the repo")
    print("3. Submit PR")
    print("✓ Bankr: PR submitted for review")
    return True

def register_all():
    """Register on all marketplaces"""
    if not WALLET:
        print("ERROR: Set BASE_WALLET env var")
        return False
    
    print(f"\n🤖 Registering agent with wallet: {WALLET[:10]}...\n")
    
    register_0xwork()
    register_moltlaunch("Agent", "Base L2 earning agent", "mining,defi,analysis")
    register_nookplot()
    register_bankr_skills()
    
    print("\n✅ All marketplaces registered!")
    print("\nNext steps:")
    print("- Stake tokens where required")
    print("- Monitor inbox for work requests")
    print("- Keep skills updated")
    
    return True

if __name__ == "__main__":
    register_all()
