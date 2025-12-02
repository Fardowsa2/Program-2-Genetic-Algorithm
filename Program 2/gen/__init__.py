"""
Genetic Algorithm Scheduler Package
"""

# Version information
__version__ = "1.0.0"
__author__ = "SLA Scheduling Team"
__description__ = "Genetic algorithm for optimizing SLA activity scheduling"

# Import key components for easier access
from gen.models import Schedule, ActivityAssignment
from gen.constants import (
    ALL_FACILITATORS,
    ALL_TIME_SLOTS,
    ROOMS_WITH_CAPACITIES,
    ACTIVITY_DEFINITIONS
)
from gen.algorithm_engine import execute_genetic_algorithm
from gen.fitness_evaluator import fitness_calculator

# Define what gets imported with "from gen import *"
__all__ = [
    'Schedule',
    'ActivityAssignment',
    'execute_genetic_algorithm',
    'fitness_calculator',
    'ALL_FACILITATORS',
    'ALL_TIME_SLOTS',
    'ROOMS_WITH_CAPACITIES',
    'ACTIVITY_DEFINITIONS'
]
