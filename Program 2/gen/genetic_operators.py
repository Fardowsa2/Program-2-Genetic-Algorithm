"""
Genetic operators for the scheduling algorithm.
Includes crossover and mutation functions.
"""
import random
from gen.models import Schedule
from gen.constants import ALL_ACTIVITIES


def perform_single_point_crossover(parent_1: Schedule, parent_2: Schedule) -> Schedule:
    """
    Create child schedule using single-point crossover.

    Args:
        parent_1: First parent schedule
        parent_2: Second parent schedule

    Returns:
        New child schedule
    """
    # Random crossover point
    crossover_point = random.randint(0, len(ALL_ACTIVITIES) - 1)

    # Create child assignments
    child_assignments = {}

    for index, activity_name in enumerate(ALL_ACTIVITIES):
        if index <= crossover_point:
            # Take from first parent
            child_assignments[activity_name] = parent_1.assignments[activity_name].copy()
        else:
            # Take from second parent
            child_assignments[activity_name] = parent_2.assignments[activity_name].copy()

    return Schedule(child_assignments)


def perform_uniform_crossover(parent_1: Schedule, parent_2: Schedule,
                              crossover_probability: float = 0.5) -> Schedule:
    """
    Create child schedule using uniform crossover.

    Args:
        parent_1: First parent schedule
        parent_2: Second parent schedule
        crossover_probability: Probability of taking from second parent

    Returns:
        New child schedule
    """
    child_assignments = {}

    for activity_name in ALL_ACTIVITIES:
        if random.random() < crossover_probability:
            # Take from second parent
            child_assignments[activity_name] = parent_2.assignments[activity_name].copy()
        else:
            # Take from first parent
            child_assignments[activity_name] = parent_1.assignments[activity_name].copy()

    return Schedule(child_assignments)


def apply_mutation(schedule: Schedule, mutation_probability: float = 0.01) -> Schedule:
    """
    Mutate a schedule by randomly changing room, time, or facilitator.

    Args:
        schedule: Schedule to mutate (modified in place)
        mutation_probability: Probability of mutating each attribute

    Returns:
        The mutated schedule (same object)
    """
    from gen.constants import ROOMS_WITH_CAPACITIES, ALL_TIME_SLOTS, ALL_FACILITATORS

    for activity_name in schedule.assignments:
        assignment = schedule.assignments[activity_name]

        # Mutate room with given probability
        if random.random() < mutation_probability:
            assignment.room = random.choice(list(ROOMS_WITH_CAPACITIES.keys()))

        # Mutate time slot with given probability
        if random.random() < mutation_probability:
            assignment.time = random.choice(ALL_TIME_SLOTS)

        # Mutate facilitator with given probability
        if random.random() < mutation_probability:
            assignment.facilitator = random.choice(ALL_FACILITATORS)

    # Clear cached fitness since schedule changed
    schedule.fitness = None

    return schedule