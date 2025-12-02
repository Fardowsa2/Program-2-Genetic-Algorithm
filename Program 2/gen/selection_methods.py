"""
Selection methods for parent selection in genetic algorithm.
"""
import math
import random
from typing import List, Tuple
from gen.models import Schedule


def calculate_softmax_probabilities(fitness_scores: List[float]) -> List[float]:
    """
    Convert fitness scores to selection probabilities using softmax.

    Args:
        fitness_scores: List of fitness values

    Returns:
        List of probabilities that sum to 1.0
    """
    if not fitness_scores:
        return []

    # For numerical stability, subtract max value
    max_score = max(fitness_scores)
    exponentiated_scores = [math.exp(score - max_score) for score in fitness_scores]
    total = sum(exponentiated_scores)

    # Avoid division by zero
    if total == 0:
        return [1.0 / len(fitness_scores)] * len(fitness_scores)

    return [score / total for score in exponentiated_scores]


def select_parent_pairs(
        population: List[Schedule],
        selection_probabilities: List[float],
        number_of_pairs: int
) -> List[Tuple[Schedule, Schedule]]:
    """
    Select parent pairs for crossover using weighted random selection.

    Args:
        population: List of schedules
        selection_probabilities: Probability for each schedule
        number_of_pairs: Number of parent pairs to select

    Returns:
        List of (parent_a, parent_b) tuples
    """
    selected_pairs = []

    for _ in range(number_of_pairs):
        # Select first parent based on fitness
        parent_a = random.choices(population, weights=selection_probabilities, k=1)[0]

        # Select second parent (could be same as first, that's okay)
        parent_b = random.choices(population, weights=selection_probabilities, k=1)[0]

        selected_pairs.append((parent_a, parent_b))

    return selected_pairs


def select_best_schedules(
        population: List[Schedule],
        fitness_scores: List[float],
        number_to_select: int
) -> List[Schedule]:
    """
    Select the best schedules for elitism preservation.

    Args:
        population: List of schedules
        fitness_scores: Fitness score for each schedule
        number_to_select: Number of best schedules to select

    Returns:
        List of the best schedule copies
    """
    # Pair each schedule with its fitness score
    schedule_fitness_pairs = list(zip(population, fitness_scores))

    # Sort by fitness in descending order
    schedule_fitness_pairs.sort(key=lambda pair: pair[1], reverse=True)

    # Select top schedules and return copies
    top_schedules = []
    for schedule, _ in schedule_fitness_pairs[:number_to_select]:
        top_schedules.append(schedule.create_copy())

    return top_schedules