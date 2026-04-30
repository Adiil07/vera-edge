"""
Local test script for Vera Edge bot.
Run this BEFORE deploying to verify all endpoints work correctly.

Usage:
  1. Start server: uvicorn main:app --port 8000
  2. Run tests:    python test_local.py
"""

import json
import time
import requests

BASE_URL = "http://localhost:8000"

def print_result(test_name, response):
    status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
    print(f"\n{status} — {test_name}")
    print(f"   Status: {response.status_code}")
    try:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=4)[:500]}")
    except:
        print(f"   Response: {response.text[:200]}")

print("=" * 60)
print("VERA EDGE — Local Endpoint Test Suite")
print("=" * 60)

# ── TEST 1: Health Check ──
print("\n[1/6] Testing /v1/healthz ...")
r = requests.get(f"{BASE_URL}/v1/healthz")
print_result("Health Check", r)

# ── TEST 2: Metadata ──
print("\n[2/6] Testing /v1/metadata ...")
r = requests.get(f"{BASE_URL}/v1/metadata")
print_result("Metadata", r)

# ── TEST 3: Load Category Context ──
print("\n[3/6] Testing /v1/context (category load) ...")
r = requests.post(f"{BASE_URL}/v1/context", json={
    "scope": "category",
    "context_id": "cat_dentists",
    "version": 1,
    "payload": {
        "name": "Dentists",
        "tone": "clinical, trust-first",
        "benchmark_ctr": 2.8,
        "benchmark_rating": 4.5,
        "offer_patterns": ["checkup package", "cleaning discount"],
        "example_hook": "190 people searching for dental checkups nearby"
    },
    "delivered_at": "2026-04-29T10:00:00Z"
})
print_result("Category Context Load", r)

# ── TEST 4: Load Merchant Context ──
print("\n[4/6] Testing /v1/context (merchant load) ...")
r = requests.post(f"{BASE_URL}/v1/context", json={
    "scope": "merchant",
    "context_id": "m_001_drmeera",
    "version": 3,
    "payload": {
        "identity": {
            "id": "m_001_drmeera",
            "name": "Dr. Meera Sharma",
            "business_name": "Smile Care Dental Clinic",
            "category": "dentists",
            "location": "Hauz Khas, South Delhi"
        },
        "performance": {
            "ctr": 2.1,
            "peer_median_ctr": 3.0,
            "rating": 4.2,
            "review_count": 67,
            "monthly_leads": 34
        },
        "offers": [
            {"name": "Dental Cleaning", "price": 299, "views": 145, "conversions": 28}
        ],
        "signals": {
            "last_review_reply_hours": 18,
            "listing_completeness": 0.72
        }
    },
    "delivered_at": "2026-04-29T10:00:00Z"
})
print_result("Merchant Context Load", r)

# ── TEST 5: Load Trigger + Run Tick ──
print("\n[5/6] Testing /v1/tick ...")
# First load trigger
requests.post(f"{BASE_URL}/v1/context", json={
    "scope": "trigger",
    "context_id": "trg_research_digest_dentists",
    "version": 1,
    "payload": {
        "type": "research_digest",
        "signal": "190 people searching for Dental Check Up in Hauz Khas",
        "search_volume": 190,
        "trend": "spike",
        "urgency": "high"
    },
    "delivered_at": "2026-04-29T10:00:00Z"
})

time.sleep(1)

r = requests.post(f"{BASE_URL}/v1/tick", json={
    "now": "2026-04-29T10:30:00Z",
    "available_triggers": ["trg_research_digest_dentists"]
})
print_result("Tick (Message Composition)", r)

# Check message quality
if r.status_code == 200:
    actions = r.json().get("actions", [])
    if actions:
        body = actions[0].get("body", "")
        print(f"\n   📨 COMPOSED MESSAGE:")
        print(f"   '{body}'")
        print(f"   📏 Length: {len(body)} chars (max 320)")
        print(f"   🎯 CTA: {actions[0].get('cta')}")
        print(f"   💡 Rationale: {actions[0].get('rationale', '')[:100]}")
        if len(body) <= 320:
            print("   ✅ Within 320 char limit")
        else:
            print("   ❌ EXCEEDS 320 char limit!")

# ── TEST 6: Reply Handling ──
print("\n[6/6] Testing /v1/reply ...")
r = requests.post(f"{BASE_URL}/v1/reply", json={
    "conversation_id": "conv_001",
    "from_role": "merchant",
    "message": "Yes, send me the patient message draft",
    "turn_number": 2
})
print_result("Reply Handling", r)

print("\n" + "=" * 60)
print("TEST SUITE COMPLETE")
print("=" * 60)
print("\nIf all tests passed, your bot is ready for deployment! 🚀")
print("Next step: Deploy to Railway or Render and submit your URL.")
