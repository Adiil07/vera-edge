# Vera Edge 🧠
### magicpin AI Challenge Submission

**Team:** Adil
**Model:** llama-3.3-70b-versatile (Groq Free)
**Version:** 1.0.0

---

## The Big Idea

Most message bots ask: *"What should I say?"*

Vera Edge asks: *"What does THIS merchant need to hear RIGHT NOW to grow?"*

That shift — from generic composer to strategic advisor — is the entire philosophy.

---

## The 4-Pillar Framework

Every message Vera Edge composes runs through four thinking layers:

### 🌅 Pillar 1: Daily Intelligence
Real-time operational signals — demand spikes, weather, local events, foot traffic patterns.
Ramesh shouldn't just get a message. He should feel like Vera watched his street overnight.

### 🏆 Pillar 2: Battlefield View
How does this merchant compare to peers in their locality?
Not to discourage — to show the gap is closeable with one specific action.

### 📈 Pillar 3: Growth Move Engine
One action. Every week. Completable in under 10 minutes.
Overwhelm kills adoption. One clear move builds habit.

### 💰 Pillar 4: Revenue Radar
View-to-order gaps, pricing anomalies, upsell opportunities.
Every message connects to a real number from the merchant's own data.

---

## Decision Hierarchy

When composing, Vera Edge evaluates signals in this order:

```
1. Revenue opportunity now?     → Lead with that
2. Competitive gap to close?    → Lead with that
3. Operational signal?          → Lead with that
4. Weekly growth action due?    → Lead with that
5. Recall / lapse situation?    → Lead with that
```

This hierarchy ensures every message is the HIGHEST value action, not just any action.

---

## Technical Approach

- **Framework:** FastAPI (Python)
- **LLM:** Claude Sonnet via Groq API (Free)
- **Context storage:** In-memory (fast, stateful per session)
- **Composition:** Single-prompt with structured JSON output
- **Fallback:** Graceful degradation — never crashes, always responds

### Why single-prompt over RAG/retrieval?

The challenge context is structured JSON — not unstructured docs.
A well-designed system prompt with clear decision rules outperforms retrieval
for structured merchant data. Retrieval adds latency without adding accuracy here.

---

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /v1/context` | Receive + store context (idempotent by version) |
| `POST /v1/tick` | Compose messages for all merchants against available triggers |
| `POST /v1/reply` | Handle merchant replies with conversation history |
| `GET /v1/healthz` | Liveness check with context counts |
| `GET /v1/metadata` | Team identity |

---

## What Makes This Different From Other Submissions

1. **Philosophy before features** — Vera Edge is a named framework, not a prompt hack
2. **Merchant psychology built-in** — tone rules per category, decision hierarchy
3. **Conversation memory** — `/v1/reply` tracks full conversation history per session
4. **Hard constraints enforced in code** — 320 char cap, no URL check, one CTA rule
5. **Graceful fallbacks** — judge harness never gets a 500 error

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Groq API (Free) key
export ANTHROPIC_API_KEY=your_key_here

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Test health
curl http://localhost:8000/v1/healthz
```

---

## The Merchant We're Building For

Ramesh Kumar. Runs a small dhaba in Lajpat Nagar.
Wakes at 8 AM. Closes at 11 PM. No marketing team.
Dreams of being the #1 restaurant in his area.

Vera Edge is built for Ramesh — not for dashboards.
