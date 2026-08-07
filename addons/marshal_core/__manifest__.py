{
    "name": "Marshal Core",
    "summary": "Freight movement scheduling for exhibition venues",
    "description": """
Marshal Core
============
Schedules the movement of freight from loading dock to exhibition booth.

The two mechanics that must be exactly right:

1. THE BLOCKING RULE - a movement may enter a chokepoint only if the
   DOWNSTREAM buffer has space. Never occupy what you cannot clear.
2. THE CONTENTION COMPARATOR - seven tests evaluated in order, with a
   claim sequence number as the guaranteed final discriminator so the
   scheduler is reproducible.
""",
    "version": "16.0.1.4.0",
    "category": "Operations",
    "author": "Marshal.show",
    "website": "https://marshal.show",
    "license": "LGPL-3",
    "depends": ["base", "mail", "resource", "hr", "maintenance"],
    "data": [
        "security/marshal_security.xml",
        "security/ir.model.access.csv",
        "data/marshal_sequence.xml",
        "views/marshal_views.xml",
        "views/board_templates.xml",
    ],
    "application": True,
    "installable": True,
}
