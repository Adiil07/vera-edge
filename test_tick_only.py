import requests
import json

BASE_URL = 'http://localhost:8000'

# Post contexts
contexts = [
    {
        "scope": "category",
        "context_id": "dentists",
        "version": 1,
        "payload": {
            "slug": "dentists",
            "peer_stats": {"avg_ctr": 0.035, "avg_calls": 42, "avg_leads": 15},
            "digest": [{"title": "JIDA Oct Issue", "source": "JIDA", "date": "2026-09-15"}],
            "offer_catalog": [{"service": "Teeth Whitening", "price": "₹8,000"}]
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    },
    {
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
            "signals": ["ctr_below_peer"],
            "offers": [],
            "subscription": {"status": "active", "plan": "pro", "days_remaining": 45},
            "review_themes": ["friendly_doctor"]
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    },
    {
        "scope": "trigger",
        "context_id": "trg_001_dentist_ctr",
        "version": 1,
        "payload": {
            "trigger_id": "trg_001_dentist_ctr",
            "merchant_id": "m_001_drmeera",
            "kind": "performance_alert",
            "urgency": 4,
            "scope": "merchant",
            "suppression_key": "perf:m_001_drmeera:2026-w18",
            "payload": {
                "alert_type": "ctr_below_peer",
                "metric": "ctr",
                "value": 0.021,
                "peer_median": 0.035
            },
            "expires_at": "2026-05-07T23:59:59Z"
        },
        "delivered_at": "2026-05-01T10:00:00Z"
    }
]

for ctx in contexts:
    requests.post(f'{BASE_URL}/v1/context', json=ctx)

# Run tick
resp = requests.post(f'{BASE_URL}/v1/tick', json={
    "now": "2026-05-01T10:30:00Z",
    "available_triggers": ["trg_001_dentist_ctr"]
})

data = resp.json()
actions = data.get('actions', [])

if actions:
    a = actions[0]
    print('=== ACTION 1 ===')
    print('Body:', a.get('body', ''))
    print('CTA:', a.get('cta', ''))
    print('Template:', a.get('template_name', ''))
    print('Rationale:', a.get('rationale', ''))
    print('Body length:', len(a.get('body', '')))
else:
    print('No actions returned')