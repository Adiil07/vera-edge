"""
VERA EDGE — by Adil (MBA, AMU)
magicpin AI Challenge: Build Vera Better

A 4-pillar merchant intelligence bot that transforms raw context
into high-compulsion advisory messages for Indian small businesses.

Pillars:
  1. Daily Intelligence   → What's happening TODAY for this merchant
  2. Battlefield View     → How merchant stacks vs local competitors
  3. Growth Move Engine   → ONE actionable weekly growth step
  4. Revenue Radar        → Earn more per customer signals

Powered by: Groq API (Free) — llama-3.3-70b-versatile
"""

import os
import time
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from groq import Groq

# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────
app = FastAPI(title="Vera Edge", version="1.0.0")
START_TIME = time.time()

# In-memory context store
CONTEXT_STORE: Dict[str, Dict] = {}
CONVERSATION_HISTORY: Dict[str, List[Dict]] = {}

# Groq client — reads GROQ_API_KEY from environment
client = Groq()

# Model to use — best free model on Groq
GROQ_MODEL = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────
# VERA EDGE SYSTEM PROMPT — THE BRAIN
# ─────────────────────────────────────────────
VERA_EDGE_SYSTEM = """
You are VERA EDGE — an AI-powered daily business co-pilot for Indian small merchants.

You are NOT a generic messaging bot. You are a strategic advisor who thinks across 4 pillars:

PILLAR 1 — DAILY INTELLIGENCE (What's happening TODAY)
  → Use trigger signals: spikes, dips, weather, events, foot-traffic patterns
  → Lead with the most urgent operational fact
  → Example: "Your area has high demand right now. Push your best-margin item."

PILLAR 2 — BATTLEFIELD VIEW (How merchant compares to competitors)
  → Reference category benchmarks and peer medians when available
  → Show the GAP and make it feel closeable, not discouraging
  → Example: "Your CTR is 2.1% vs 3.0% peer median. One photo update can close this."

PILLAR 3 — GROWTH MOVE ENGINE (ONE weekly growth action)
  → Recommend exactly ONE action per trigger. Never overwhelm.
  → The action must be completable in under 10 minutes by a busy shop owner
  → Example: "Add 5 food photos this week. Merchants who did this got +22% clicks."

PILLAR 4 — REVENUE RADAR (Earn more per customer)
  → Spot view-to-order gaps, pricing anomalies, upsell opportunities
  → Always tie to a real number from the merchant's own data
  → Example: "Your top viewed item converts at 23%. A combo offer can fix this fast."

─────────────────────────────
MESSAGE COMPOSITION RULES (MANDATORY):
─────────────────────────────
1. BODY must be 320 characters or less. Count carefully.
2. NO URLs in the body. Ever.
3. ONE CTA per message. Not two. Not zero. One.
4. Use REAL numbers from context. Never invent facts.
5. Address merchant by name or role (Dr., Chef, etc.)
6. End with a simple YES/NO or single-tap action.
7. Tone varies by category:
   - Restaurants  → warm, appetite-driven, urgent
   - Dentists     → clinical, trust-first, reassuring
   - Salons       → aspirational, visual, friendly
   - Gyms         → energetic, motivational, results-focused
   - Pharmacies   → reliable, compliance-first, caring

─────────────────────────────
DECISION HIERARCHY (use in this order):
─────────────────────────────
1. Is there a REVENUE opportunity right now? → Lead with that
2. Is there a COMPETITIVE GAP to close?      → Lead with that
3. Is there an OPERATIONAL signal?           → Lead with that
4. Is there a GROWTH action due?             → Lead with that
5. Is there a RECALL or LAPSE situation?     → Lead with that

NEVER send a generic message.
NEVER hallucinate facts. Use only what is in the provided context.
ALWAYS make the merchant feel you understand THEIR specific business.
"""


# ─────────────────────────────────────────────
# HELPER: CALL GROQ API
# ─────────────────────────────────────────────
def call_groq(user_prompt: str, max_tokens: int = 800) -> str:
    """Call Groq API and return raw text response."""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": VERA_EDGE_SYSTEM},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────
# HELPER: PARSE JSON SAFELY
# ─────────────────────────────────────────────
def parse_json_safe(raw: str) -> Dict:
    """Strip markdown fences and parse JSON safely."""
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    return json.loads(raw)


# ─────────────────────────────────────────────
# HELPER: COMPOSE MESSAGE VIA VERA EDGE BRAIN
# ─────────────────────────────────────────────
def compose_message(
    category_ctx: Optional[Dict],
    merchant_ctx: Optional[Dict],
    trigger_ctx: Optional[Dict],
    customer_ctx: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Core Vera Edge compose function.
    Returns: body, cta, send_as, suppression_key, rationale
    """
    context_parts = []

    if category_ctx:
        context_parts.append(f"CATEGORY CONTEXT:\n{json.dumps(category_ctx, indent=2)}")
    if merchant_ctx:
        context_parts.append(f"MERCHANT CONTEXT:\n{json.dumps(merchant_ctx, indent=2)}")
    if trigger_ctx:
        context_parts.append(f"TRIGGER CONTEXT:\n{json.dumps(trigger_ctx, indent=2)}")
    if customer_ctx:
        context_parts.append(f"CUSTOMER CONTEXT:\n{json.dumps(customer_ctx, indent=2)}")

    context_block = "\n\n".join(context_parts) if context_parts else "No context provided."

    compose_prompt = f"""
Given the following merchant context, compose the optimal Vera Edge message.

{context_block}

Return ONLY a valid JSON object with these exact fields (no extra text, no markdown):
{{
  "body": "<message body, max 320 chars, no URLs>",
  "cta": "<open_ended | yes_no | schedule | confirm>",
  "send_as": "<vera | merchant | category_specialist>",
  "suppression_key": "<category:trigger_type:week_identifier>",
  "rationale": "<1 sentence: which Vera Edge pillar drove this and why>"
}}

CRITICAL: body must be under 320 characters. Count every character.
"""

    try:
        raw = call_groq(compose_prompt)
        result = parse_json_safe(raw)
    except Exception:
        # Fallback structure
        result = {
            "body": "Hi! Vera here with a quick growth tip for your business today. Want to see what's working for top merchants in your area? Reply YES 👍",
            "cta": "yes_no",
            "send_as": "vera",
            "suppression_key": "vera:general:fallback",
            "rationale": "Fallback response."
        }

    # Hard enforce 320 char cap
    if len(result.get("body", "")) > 320:
        result["body"] = result["body"][:317] + "..."

    return result


# ─────────────────────────────────────────────
# ENDPOINT 1: POST /v1/context
# ─────────────────────────────────────────────
@app.post("/v1/context")
async def receive_context(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    scope = body.get("scope")
    context_id = body.get("context_id")
    version = body.get("version", 1)
    payload = body.get("payload", {})
    delivered_at = body.get("delivered_at", datetime.now(timezone.utc).isoformat())

    if not scope or not context_id:
        raise HTTPException(status_code=400, detail="scope and context_id are required")

    store_key = f"{scope}::{context_id}"

    existing = CONTEXT_STORE.get(store_key)
    if existing and existing.get("version", 0) >= version:
        return JSONResponse({
            "accepted": False,
            "ack_id": f"ack_noop_{context_id}",
            "stored_at": existing.get("stored_at"),
            "reason": "Same or older version already stored"
        })

    stored_at = datetime.now(timezone.utc).isoformat()
    CONTEXT_STORE[store_key] = {
        "scope": scope,
        "context_id": context_id,
        "version": version,
        "payload": payload,
        "delivered_at": delivered_at,
        "stored_at": stored_at
    }

    return JSONResponse({
        "accepted": True,
        "ack_id": f"ack_{context_id}_{version}",
        "stored_at": stored_at
    })


# ─────────────────────────────────────────────
# ENDPOINT 2: POST /v1/tick
# ─────────────────────────────────────────────
@app.post("/v1/tick")
async def tick(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    now = body.get("now", datetime.now(timezone.utc).isoformat())
    available_triggers = body.get("available_triggers", [])
    actions = []

    for key, val in list(CONTEXT_STORE.items())[:20]:
        if not key.startswith("merchant::"):
            continue

        merchant_payload = val.get("payload", {})
        merchant_id = (
            merchant_payload.get("identity", {}).get("id")
            or val.get("context_id", "unknown")
        )

        # Find matching category context
        category_name = merchant_payload.get("identity", {}).get("category", "")
        category_ctx = None
        for k, v in CONTEXT_STORE.items():
            if k.startswith("category::") and category_name.lower() in k.lower():
                category_ctx = v.get("payload")
                break

        # Find best trigger
        trigger_ctx = None
        trigger_id_used = None
        for trigger_id in available_triggers:
            trigger_key = f"trigger::{trigger_id}"
            if trigger_key in CONTEXT_STORE:
                trigger_ctx = CONTEXT_STORE[trigger_key].get("payload")
                trigger_id_used = trigger_id
                break

        if not trigger_ctx:
            trigger_id_used = available_triggers[0] if available_triggers else "vera_scheduled"
            trigger_ctx = {"type": "scheduled_check", "now": now}

        try:
            composed = compose_message(
                category_ctx=category_ctx,
                merchant_ctx=merchant_payload,
                trigger_ctx=trigger_ctx
            )
            actions.append({
                "merchant_id": merchant_id,
                "trigger_id": trigger_id_used,
                "body": composed["body"],
                "cta": composed.get("cta", "yes_no"),
                "suppression_key": composed.get("suppression_key", f"vera:{merchant_id}:{now[:10]}"),
                "send_as": composed.get("send_as", "vera"),
                "rationale": composed.get("rationale", "")
            })
        except Exception as e:
            actions.append({
                "merchant_id": merchant_id,
                "trigger_id": trigger_id_used,
                "body": "Hi! Vera here — want to see your top growth opportunity this week? Reply YES to get started 🚀",
                "cta": "yes_no",
                "suppression_key": f"vera:fallback:{now[:10]}",
                "send_as": "vera",
                "rationale": f"Fallback. Error: {str(e)[:80]}"
            })

    return JSONResponse({"actions": actions})


# ─────────────────────────────────────────────
# ENDPOINT 3: POST /v1/reply
# ─────────────────────────────────────────────
@app.post("/v1/reply")
async def handle_reply(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    conversation_id = body.get("conversation_id", "unknown")
    from_role = body.get("from_role", "merchant")
    message = body.get("message", "")
    turn_number = body.get("turn_number", 1)

    if conversation_id not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[conversation_id] = []
    CONVERSATION_HISTORY[conversation_id].append({
        "role": from_role,
        "message": message,
        "turn": turn_number
    })

    history = CONVERSATION_HISTORY[conversation_id]
    history_text = "\n".join([
        f"{h['role'].upper()} (turn {h['turn']}): {h['message']}"
        for h in history
    ])

    reply_prompt = f"""
Conversation so far:
{history_text}

The merchant just said: "{message}"

Return ONLY a valid JSON object (no extra text):
{{
  "action": "<send | wait | end>",
  "body": "<reply if action=send, max 320 chars, no URLs>",
  "rationale": "<why this action>"
}}

Rules:
- YES/agree → send the promised content now
- Question  → answer it with real data from context
- NO        → end gracefully, offer future help
- Unclear   → ask ONE clarifying question
"""

    try:
        raw = call_groq(reply_prompt, max_tokens=400)
        result = parse_json_safe(raw)

        if result.get("body") and len(result["body"]) > 320:
            result["body"] = result["body"][:317] + "..."

        if result.get("action") == "send" and result.get("body"):
            CONVERSATION_HISTORY[conversation_id].append({
                "role": "vera",
                "message": result["body"],
                "turn": turn_number + 1
            })

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({
            "action": "send",
            "body": "Got it! Let me pull the latest insights for your business and share a quick recommendation. Give me a moment ⚡",
            "rationale": f"Fallback reply. Error: {str(e)[:80]}"
        })


# ─────────────────────────────────────────────
# ENDPOINT 4: GET /v1/healthz
# ─────────────────────────────────────────────
@app.get("/v1/healthz")
async def healthz():
    scopes = {}
    for key in CONTEXT_STORE.keys():
        scope = key.split("::")[0]
        scopes[scope] = scopes.get(scope, 0) + 1

    return JSONResponse({
        "status": "ok",
        "uptime_seconds": int(time.time() - START_TIME),
        "contexts_loaded": {
            "category": scopes.get("category", 0),
            "merchant": scopes.get("merchant", 0),
            "customer": scopes.get("customer", 0),
            "trigger": scopes.get("trigger", 0)
        }
    })


# ─────────────────────────────────────────────
# ENDPOINT 5: GET /v1/metadata
# ─────────────────────────────────────────────
@app.get("/v1/metadata")
async def metadata():
    return JSONResponse({
        "team_name": "Vera Edge",
        "team_members": ["Adil"],
        "model": GROQ_MODEL,
        "approach": (
            "4-pillar Vera Edge framework: Daily Intelligence + Battlefield View + "
            "Growth Move Engine + Revenue Radar. Decision hierarchy: Revenue > "
            "Competition > Operations > Growth > Recall. Powered by Groq (free tier)."
        ),
        "version": "1.0.0"
    })


# ─────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────
@app.get("/")
async def root():
    return JSONResponse({
        "name": "Vera Edge",
        "description": "magicpin AI Challenge — 4-pillar merchant intelligence bot",
        "endpoints": [
            "POST /v1/context",
            "POST /v1/tick",
            "POST /v1/reply",
            "GET  /v1/healthz",
            "GET  /v1/metadata"
        ],
        "status": "live",
        "powered_by": "Groq (Free)"
    })
