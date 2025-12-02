"""
Functions for creating and managing populations of schedules.
"""
import random
from gen.models import Schedule, ActivityAssignment
from gen.constants import (
    ROOMS_WITH_CAPACITIES,
    ALL_TIME_SLOTS,
    ALL_FACILITATORS,
    ACTIVITY_DEFINITIONS
)


def generate_random_assignment():
    """
    Create a completely random assignment for one activity.

    Returns:
        ActivityAssignment with random room, time, and facilitator
    """
    random_room = random.choice(list(ROOMS_WITH_CAPACITIES.keys()))
    random_time = random.choice(ALL_TIME_SLOTS)
    random_facilitator = random.choice(ALL_FACILITATORS)

    return ActivityAssignment(random_room, random_time, random_facilitator)


def generate_random_schedule():
    """
    Create a complete schedule with random assignments for all activities.

    Returns:
        Schedule object with random assignments
    """
    assignments_collection = {}

    for activity_name in ACTIVITY_DEFINITIONS.keys():
        assignments_collection[activity_name] = generate_random_assignment()

    return Schedule(assignments_collection)


def create_initial_population(population_size=250):
    """
    Create the initial population for the genetic algorithm.

    Args:
        population_size: Number of schedules in the population (must be ≥ 250)

    Returns:
        List of Schedule objects
    """
    if population_size < 250:
        raise ValueError(f"Population size must be at least 250, got {population_size}")

    population = []

    for _ in range(population_size):
        population.append(generate_random_schedule())

    return population


def get_population_statistics(population):
    """
    Calculate basic statistics for a population.

    Args:
        population: List of Schedule objects

    Returns:
        Dictionary with population statistics
    """
    if not population:
        return {
            "size": 0,
            "has_fitness": False,
            "fitness_range": (None, None)
        }

    fitness_scores = [s.fitness for s in population if s.fitness is not None]

    return {
        "size": len(population),
        "has_fitness": len(fitness_scores) > 0,
        "fitness_range": (min(fitness_scores) if fitness_scores else None,
                          max(fitness_scores) if fitness_scores else None),
        "with_fitness_count": len(fitness_scores)
    }
