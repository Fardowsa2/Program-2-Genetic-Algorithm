"""
Constant definitions for the SLA scheduling problem.
Contains all static data: rooms, activities, facilitators, time slots, and special rules.
"""

# ============================================================================
# AVAILABLE RESOURCES
# ============================================================================

ALL_FACILITATORS = [
    "Lock", "Glen", "Banks", "Richards", "Shaw",
    "Singer", "Uther", "Tyler", "Numen", "Zeldin"
]

ALL_TIME_SLOTS = [
    "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"
]

ROOMS_WITH_CAPACITIES = {
    "Beach 201": 18,
    "Beach 301": 25,
    "Frank 119": 95,
    "Loft 206": 55,
    "Loft 310": 48,
    "James 325": 110,
    "Roman 201": 40,
    "Roman 216": 80,
    "Slater 003": 32,
}

# ============================================================================
# ACTIVITY DEFINITIONS
# ============================================================================

ACTIVITY_DEFINITIONS = {
    "SLA101A": {
        "expected_enrollment": 40,
        "preferred_facilitators": ["Glen", "Lock", "Banks"],
        "acceptable_facilitators": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA101B": {
        "expected_enrollment": 35,
        "preferred_facilitators": ["Glen", "Lock", "Banks"],
        "acceptable_facilitators": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA191A": {
        "expected_enrollment": 45,
        "preferred_facilitators": ["Glen", "Lock", "Banks"],
        "acceptable_facilitators": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA191B": {
        "expected_enrollment": 40,
        "preferred_facilitators": ["Glen", "Lock", "Banks"],
        "acceptable_facilitators": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA201": {
        "expected_enrollment": 60,
        "preferred_facilitators": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "acceptable_facilitators": ["Richards", "Uther", "Shaw"],
    },
    "SLA291": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "acceptable_facilitators": ["Richards", "Uther", "Shaw"],
    },
    "SLA303": {
        "expected_enrollment": 25,
        "preferred_facilitators": ["Glen", "Zeldin"],
        "acceptable_facilitators": ["Banks"],
    },
    "SLA304": {
        "expected_enrollment": 20,
        "preferred_facilitators": ["Singer", "Uther"],
        "acceptable_facilitators": ["Richards"],
    },
    "SLA394": {
        "expected_enrollment": 15,
        "preferred_facilitators": ["Tyler", "Singer"],
        "acceptable_facilitators": ["Richards", "Zeldin"],
    },
    "SLA449": {
        "expected_enrollment": 30,
        "preferred_facilitators": ["Tyler", "Zeldin", "Uther"],
        "acceptable_facilitators": ["Zeldin", "Shaw"],
    },
    "SLA451": {
        "expected_enrollment": 90,
        "preferred_facilitators": ["Lock", "Banks", "Zeldin"],
        "acceptable_facilitators": ["Tyler", "Singer", "Shaw", "Glen"],
    },
}

# List of all activity names for iteration
ALL_ACTIVITIES = list(ACTIVITY_DEFINITIONS.keys())

# ============================================================================
# SPECIAL RULE CONSTANTS
# ============================================================================

# Pairs for section spacing rules
SLA101_SECTIONS = ("SLA101A", "SLA101B")
SLA191_SECTIONS = ("SLA191A", "SLA191B")

# Cross-pairs between SLA101 and SLA191 sections
CROSS_SECTION_PAIRS = [
    ("SLA101A", "SLA191A"),
    ("SLA101A", "SLA191B"),
    ("SLA101B", "SLA191A"),
    ("SLA101B", "SLA191B"),
]

# ============================================================================
# EQUIPMENT CONSTANTS (Optional)
# ============================================================================

ACTIVITY_EQUIPMENT_REQUIREMENTS = {
    "SLA304": {"requires_lab": True, "requires_projector": False},
    "SLA303": {"requires_lab": True, "requires_projector": True},
    "SLA191A": {"requires_lab": True},
    "SLA191B": {"requires_lab": True},
    "SLA291": {"requires_lab": True},
    "SLA449": {"requires_projector": True},
    "SLA451": {"requires_lab": True, "requires_projector": True},
}

ROOM_EQUIPMENT_AVAILABILITY = {
    "Beach 201": {"has_lab": False, "has_projector": True},
    "Beach 301": {"has_lab": True, "has_projector": True},
    "Loft 310": {"has_lab": True, "has_projector": False},
    "Frank 119": {"has_lab": True, "has_projector": True},
    "Roman 216": {"has_lab": True, "has_projector": True},
    "Slater 003": {"has_lab": True, "has_projector": True},
    "James 325": {"has_lab": True, "has_projector": True},
    # Default equipment for other rooms
    "Loft 206": {"has_lab": False, "has_projector": False},
    "Roman 201": {"has_lab": False, "has_projector": False},
}