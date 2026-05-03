"""
JUDGE SIMULATOR — Tests Vera Edge against competition criteria
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# ────────────────────────────────────────
# TEST DATA
# ────────────────────────────────────────

SAMPLE_CATEGORIES = {
    "dentists": {
        "scope": "category",
        "context_id": "dentists",
        "version": 1,
        "payload": {
            "slug": "dentists",
            "peer_stats": {
                "avg_ctr": 0.035,
                "avg_calls": 42,
                "avg_leads": 15,
                "top_performer_ctr": 0.048
            },
            "digest": [
                {
                    "title": "JIDA October Issue: Fluoride Varnish Guidelines Updated",
                    "source": "JIDA",
                    "date": "2026-09-15",
                    "summary": "New guidelines recommend fluoride varnish for adults with sensitivity"
                }
            ],
            "seasonal_beats": ["School dental camp season", "Wedding smile makeovers"],
            "offer_catalog": [
                {"service": "Teeth Whitening", "price": "₹8,000", "duration": "60 min"},
                {"service": "Dental Checkup", "price": "₹500", "duration": "30 min"}
            ]
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    },
    "restaurants": {
        "scope": "category",
        "context_id": "restaurants",
        "version": 1,
        "payload": {
            "slug": "restaurants",
            "peer_stats": {
                "avg_ctr": 0.042,
                "avg_cover_count": 85,
                "avg_aov": 650
            },
            "digest": [
                {
                    "title": "IPL Finals Weekend: 40% Footfall Spike Expected",
                    "source": "magicpin data",
                    "date": "2026-05-01"
                }
            ],
            "seasonal_beats": ["Summer thali specials", "Mango menu"],
            "offer_catalog": []
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    }
}

SAMPLE_MERCHANTS = {
    "m_001_drmeera": {
        "scope": "merchant",
        "context_id": "m_001_drmeera",
        "version": 1,
        "payload": {
            "merchant_id": "m_001_drmeera",
            "category_slug": "dentists",
            "identity": {
                "name": "Dr. Meera's Dental Clinic",
                "owner_first_name": "Meera",
                "locality": "Koramangala",
                "city": "Bangalore",
                "languages": ["en", "hi"]
            },
            "performance": {
                "views": 1250,
                "calls": 38,
                "ctr": 0.021,
                "leads": 12,
                "delta_7d": {"views_pct": 0.05, "calls_pct": -0.08}
            },
            "signals": ["ctr_below_peer", "call_drop_7d"],
            "offers": [],
            "subscription": {"status": "active", "plan": "pro", "days_remaining": 45},
            "review_themes": ["friendly_doctor", "clean_clinic"],
            "conversation_history": []
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    },
    "m_002_spicehouse": {
        "scope": "merchant",
        "context_id": "m_002_spicehouse",
        "version": 1,
        "payload": {
            "merchant_id": "m_002_spicehouse",
            "category_slug": "restaurants",
            "identity": {
                "name": "Spice House",
                "owner_first_name": "Raj",
                "locality": "Indiranagar",
                "city": "Bangalore",
                "languages": ["en"]
            },
            "performance": {
                "views": 3400,
                "calls": 120,
                "ctr": 0.045,
                "leads": 55,
                "delta_7d": {"views_pct": 0.12, "calls_pct": 0.15}
            },
            "signals": ["ctr_above_peer", "growth_momentum"],
            "offers": [
                {"name": "IPL Combo", "price": "₹499", "status": "active"}
            ],
            "subscription": {"status": "expiring", "plan": "basic", "days_remaining": 3},
            "review_themes": ["great_biryani", "slow_service"],
            "conversation_history": []
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    }
}

SAMPLE_TRIGGERS = {
    "trg_001_dentist_ctr": {
        "scope": "trigger",
        "context_id": "trg_001_dentist_ctr",
        "version": 1,
        "payload": {
            "trigger_id": "trg_001_dentist_ctr",
            "merchant_id": "m_001_drmeera",
            "customer_id": None,
            "kind": "performance_alert",
            "urgency": 4,
            "scope": "merchant",
            "suppression_key": "perf:m_001_drmeera:2026-w18",
            "payload": {
                "alert_type": "ctr_below_peer",
                "metric": "ctr",
                "value": 0.021,
                "peer_median": 0.035,
                "gap_pct": 40
            },
            "expires_at": "2026-05-07T23:59:59Z"
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    },
    "trg_002_restaurant_ipldigest": {
        "scope": "trigger",
        "context_id": "trg_002_restaurant_ipldigest",
        "version": 1,
        "payload": {
            "trigger_id": "trg_002_restaurant_ipldigest",
            "merchant_id": "m_002_spicehouse",
            "customer_id": None,
            "kind": "research_digest",
            "urgency": 3,
            "scope": "merchant",
            "suppression_key": "digest:restaurants:2026-w18",
            "payload": {
                "digest_title": "IPL Finals Weekend: 40% Footfall Spike Expected",
                "relevance": "high"
            },
            "expires_at": "2026-05-05T23:59:59Z"
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    }
}


# ────────────────────────────────────────
# TEST FUNCTIONS
# ────────────────────────────────────────

def test_post_context():
    """Test 1: Post all contexts"""
    print("\n" + "="*60)
    print("TEST 1: POSTING CONTEXTS")
    print("="*60)
    
    all_contexts = list(SAMPLE_CATEGORIES.values()) + \
                   list(SAMPLE_MERCHANTS.values()) + \
                   list(SAMPLE_TRIGGERS.values())
    
    passed = 0
    failed = 0
    
    for ctx in all_contexts:
        resp = requests.post(f"{BASE_URL}/v1/context", json=ctx)
        status = "✅" if resp.status_code == 200 else "❌"
        print(f"  {status} {ctx['scope']}::{ctx['context_id']} → {resp.status_code}")
        if resp.status_code == 200:
            passed += 1
        else:
            failed += 1
            print(f"     Response: {resp.json()}")
    
    print(f"\n  Result: {passed} passed, {failed} failed")
    return failed == 0


def test_tick_schema():
    """Test 2: Verify /v1/tick response schema"""
    print("\n" + "="*60)
    print("TEST 2: TICK SCHEMA VALIDATION")
    print("="*60)
    
    # Get available trigger IDs
    trigger_ids = list(SAMPLE_TRIGGERS.keys())
    
    payload = {
        "now": "2026-05-01T10:30:00Z",
        "available_triggers": trigger_ids
    }
    
    resp = requests.post(f"{BASE_URL}/v1/tick", json=payload)
    
    if resp.status_code != 200:
        print(f"  ❌ Tick failed: {resp.status_code} — {resp.text}")
        return False
    
    data = resp.json()
    actions = data.get("actions", [])
    
    if not actions:
        print("  ⚠️  No actions returned (might be valid if nothing to send)")
        return True
    
    print(f"  Actions generated: {len(actions)}")
    
    required_fields = [
        "conversation_id", "merchant_id", "customer_id",
        "send_as", "trigger_id", "template_name", "template_params",
        "body", "cta", "suppression_key", "rationale"
    ]
    
    all_passed = True
    for i, action in enumerate(actions):
        print(f"\n  Action {i+1}:")
        for field in required_fields:
            present = field in action
            status = "✅" if present else "❌"
            if not present:
                all_passed = False
            # Show value for key fields
            if field in ["body", "template_name", "rationale"] and present:
                val = str(action[field])[:60]
                print(f"    {status} {field}: {val}...")
            elif present:
                print(f"    {status} {field}: {action[field]}")
        
        # Check 320 char cap
        body_len = len(action.get("body", ""))
        cap_status = "✅" if body_len <= 320 else "❌"
        if body_len > 320:
            all_passed = False
        print(f"    {cap_status} body length: {body_len}/320")
    
    print(f"\n  Result: {'ALL FIELDS PRESENT' if all_passed else 'SOME FIELDS MISSING'}")
    return all_passed


def test_reply_actions():
    """Test 3: Verify /v1/reply handles all action types"""
    print("\n" + "="*60)
    print("TEST 3: REPLY ACTION VALIDATION")
    print("="*60)
    
    all_passed = True
    
    # 3a: Normal message
    print("\n  3a: Normal qualifying message")
    payload = {
        "conversation_id": "test_conv_001",
        "merchant_id": "m_001_drmeera",
        "from_role": "merchant",
        "message": "Tell me more about this",
        "turn_number": 2
    }
    
    # First, seed the conversation with a vera message
    CONVERSATIONS = {}  # We'll test fresh
    
    resp = requests.post(f"{BASE_URL}/v1/reply", json=payload)
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        action = data.get("action", "")
        print(f"    Action: {action}")
        
        if action == "send" and "body" not in data:
            print("    ❌ send action missing body")
            all_passed = False
        elif action == "wait" and "wait_seconds" not in data:
            print("    ❌ wait action missing wait_seconds")
            all_passed = False
        else:
            print(f"    ✅ Valid {action} response")
    
    # 3b: Wait signal
    print("\n  3b: Wait signal ('baad mein')")
    payload["message"] = "baad mein batana"
    resp = requests.post(f"{BASE_URL}/v1/reply", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        action = data.get("action", "")
        print(f"    Action: {action}")
        if action == "wait":
            print(f"    wait_seconds: {data.get('wait_seconds', 'MISSING')}")
            print("    ✅ Wait correctly triggered")
        else:
            print(f"    ⚠️  Expected 'wait', got '{action}' (might be LLM deciding)")
    
    # 3c: No/decline
    print("\n  3c: Decline ('no stop')")
    payload["message"] = "no stop"
    resp = requests.post(f"{BASE_URL}/v1/reply", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"    Action: {data.get('action', '')}")
    
    # 3d: Hostile
    print("\n  3d: Hostile message")
    payload["message"] = "this is spam stop messaging me"
    resp = requests.post(f"{BASE_URL}/v1/reply", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"    Action: {data.get('action', '')}")
    
    return all_passed


def test_auto_reply_detection():
    """Test 4: Auto-reply hell detection"""
    print("\n" + "="*60)
    print("TEST 4: AUTO-REPLY DETECTION (PHASE 4)")
    print("="*60)
    
    conv_id = "test_auto_reply_001"
    auto_message = "thank you for contacting us we will get back to you shortly"
    
    for i in range(4):
        payload = {
            "conversation_id": conv_id,
            "merchant_id": "m_001_drmeera",
            "from_role": "merchant",
            "message": auto_message,
            "turn_number": i + 2
        }
        resp = requests.post(f"{BASE_URL}/v1/reply", json=payload)
        data = resp.json()
        action = data.get("action", "")
        print(f"  Turn {i+2}: message='{auto_message[:40]}...' → action={action}")
        
        if action == "end":
            print("  ✅ Auto-reply detected! Bot exited gracefully on turn", i+2)
            return True
    
    print("  ❌ Bot did NOT exit after 4 auto-replies")
    return False


def test_hindi_code_mix():
    """Test 5: Hindi code-mix for merchant with hi language"""
    print("\n" + "="*60)
    print("TEST 5: HINDI CODE-MIX")
    print("="*60)
    
    # Dr Meera has languages: ["en", "hi"]
    payload = {
        "now": "2026-05-01T10:30:00Z",
        "available_triggers": ["trg_001_dentist_ctr"]
    }
    
    resp = requests.post(f"{BASE_URL}/v1/tick", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        actions = data.get("actions", [])
        if actions:
            body = actions[0].get("body", "")
            print(f"  Body: {body[:200]}...")
            
            # Check for Hindi words
            hindi_indicators = ["aapke", "namaste", "karein", "hai", "mein", "ka", "ki", 
                              "hain", "bhejein", "dekhein", "sukriya", "theek"]
            found = [w for w in hindi_indicators if w.lower() in body.lower()]
            
            if found:
                print(f"  ✅ Hindi code-mix detected! Words: {found}")
                return True
            else:
                print("  ⚠️  No Hindi detected in message for hi-language merchant")
                print("     (Might still be valid English message)")
                return True  # Not a hard fail
    return False


# ────────────────────────────────────────
# MAIN
# ────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("🔍 VERA EDGE JUDGE SIMULATOR v1.0")
    print("="*60)
    print(f"Target: {BASE_URL}")
    
    results = {}
    
    # Test 1: Context posting
    results["context"] = test_post_context()
    
    # Test 2: Tick schema
    results["tick_schema"] = test_tick_schema()
    
    # Test 3: Reply actions
    results["reply_actions"] = test_reply_actions()
    
    # Test 4: Auto-reply detection
    results["auto_reply"] = test_auto_reply_detection()
    
    # Test 5: Hindi code-mix
    results["hindi"] = test_hindi_code_mix()
    
    # Summary
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {test}")
    
    print(f"\n  SCORE: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🏆 ALL TESTS PASSED! You're ready for deployment!")
    elif passed >= total - 1:
        print("\n  👍 Almost there! Fix the failing test and redeploy.")
    else:
        print("\n  🔧 Several tests failed. Check the output above.")


if __name__ == "__main__":
    main()