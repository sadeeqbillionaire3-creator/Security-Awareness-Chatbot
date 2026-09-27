"""
Emergency contacts directory for the Security Awareness Chatbot.

IMPORTANT: Every number here MUST be independently verified before this
app is shown to real users. Numbers were pulled from news reports and
can change, be misreported, or be tied to a specific event (e.g. an
election period). Call each one yourself, or confirm with the issuing
agency's official website/social media, before publishing.

Structure: list of dicts so it's easy to render in a UI or feed to the
chatbot when a user asks "who do I call".
"""

EMERGENCY_CONTACTS = [
    {
        "name": "Nigeria Police Force - National Emergency Line",
        "number": "112",
        "notes": "National toll-free emergency number (police/fire/ambulance dispatch). Also try 199.",
        "verified": False,
        "source": "General public knowledge - VERIFY before publishing",
    },
    {
        "name": "Katsina State Police Command",
        "number": "08159677777",  # also reported as 08156977777 in another article - VERIFY
        "notes": "Reported by the Command's spokesperson for reporting suspicious activity. "
                 "A second source spelled this as 08156977777 - confirm the correct digit.",
        "verified": False,
        "source": "21stcenturychronicle.com / Peoples Gazette news reports, 2025-2026",
    },
    {
        "name": "Katsina State Police Command (alt line)",
        "number": "07072722539",
        "notes": "Reported alongside the number above in the same statements.",
        "verified": False,
        "source": "21stcenturychronicle.com / Peoples Gazette news reports, 2025-2026",
    },
    {
        "name": "Katsina State Police Command (alt line)",
        "number": "09022209690",
        "notes": "Reported alongside the numbers above.",
        "verified": False,
        "source": "21stcenturychronicle.com / Peoples Gazette news reports, 2025-2026",
    },
    {
        "name": "NSCDC Katsina State Command",
        "number": "",  # not confirmed as a standing line - fill in after verifying
        "notes": "News reports mention election-period call centre lines (07088882268, "
                 "08135277779) but these may not be permanent. Contact NSCDC Katsina "
                 "directly to confirm a standing public line.",
        "verified": False,
        "source": "Gazette NGR news reports, 2025-2026",
    },
    {
        "name": "NSCDC Katsina State Command - Emergency",
        "number": "08038038313",
        "notes": "Cited as the official state number released by NSCDC HQ for Katsina, "
                 "per a Meta AI Business Assistant response - cross-check but not yet "
                 "independently confirmed by a direct call.",
        "verified": False,
        "source": "Meta AI Business Assistant (WhatsApp) response, 2026 - VERIFY by calling",
    },
    {
        "name": "NSCDC National Operational Hotline",
        "number": "08060003181",
        "notes": "Second hotline reported: 08032898909.",
        "verified": False,
        "source": "Meta AI Business Assistant (WhatsApp) response, 2026 - VERIFY by calling",
    },
    {
        "name": "NSCDC National Toll-Free Line",
        "number": "0800-CALL-NSCDC",
        "notes": "Commonly cited NSCDC toll-free format - verify the exact digits with NSCDC's official site.",
        "verified": False,
        "source": "General public knowledge - VERIFY",
    },
]

# LGA-level contacts (local vigilante groups, DPOs, etc.) - add as you verify them.
# Keeping this structured makes it easy to expand without touching app logic.
LGA_CONTACTS = {
    # "Katsina": [{"name": "...", "number": "...", "notes": "...", "verified": False}],
    # "Funtua": [],
    # "Daura": [],
    # ... fill in per LGA as you gather verified info
}


def get_verified_contacts():
    """Return only contacts marked verified=True - use this in production
    so unverified numbers never reach a real user by accident."""
    return [c for c in EMERGENCY_CONTACTS if c["verified"]]