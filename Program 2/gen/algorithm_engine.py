"""
Main genetic algorithm engine for SLA scheduling.
Coordinates population evolution through generations.
"""
from typing import Dict, List, Any, Tuple
import statistics
from gen.population_manager import create_initial_population
from gen.fitness_evaluator import fitness_calculator
from gen.selection_methods import (
    calculate_softmax_probabilities,
    select_parent_pairs,
    select_best_schedules
)
from gen.genetic_operators import (
    perform_single_point_crossover,
    perform_uniform_crossover,
    apply_mutation
)


class GeneticAlgorithmEngine:
    """
    Main controller for the genetic algorithm optimization.
    """

    def __init__(self):
        self.generation_history = []
        self.total_generations_run = 0
        self.final_mutation_rate = 0.01

    def _evaluate_entire_population(
            self,
            population: List[Any]
    ) -> Tuple[List[float], float, float, float]:
        """
        Calculate fitness for all schedules in population.

        Returns:
            Tuple of (fitness_list, best_score, average_score, worst_score)
        """
        fitness_scores = []

        for schedule in population:
            score = fitness_calculator.calculate_schedule_fitness(schedule)
            fitness_scores.append(score)

        if not fitness_scores:
            return [], 0.0, 0.0, 0.0

        best_fitness = max(fitness_scores)
        average_fitness = statistics.mean(fitness_scores)
        worst_fitness = min(fitness_scores)

        return fitness_scores, best_fitness, average_fitness, worst_fitness

    def run_optimization(
            self,
            population_size: int = 250,
            minimum_generations: int = 100,
            maximum_generations: int = 500,
            initial_mutation_probability: float = 0.01,
            crossover_method: str = "single_point",
            elitism_count: int = 1,
            use_adaptive_mutation: bool = True
    ) -> Dict[str, Any]:
        """
        Execute the complete genetic algorithm optimization.

        Returns:
            Dictionary containing results:
            - best_schedule: Best schedule found
            - history: Generation-by-generation metrics
            - final_mutation_rate: Mutation rate at termination
            - generations_run: Total generations executed
        """
        # ====================================================================
        # INITIALIZATION
        # ====================================================================
        print(f"Initializing genetic algorithm with population size {population_size}...")

        current_population = create_initial_population(population_size=population_size)
        current_mutation_rate = initial_mutation_probability
        self.generation_history = []
        self.total_generations_run = 0

        previous_average_fitness = None

        # ====================================================================
        # MAIN EVOLUTION LOOP
        # ====================================================================
        for generation_number in range(maximum_generations):
            self.total_generations_run = generation_number + 1

            # ----------------------------------------------------------------
            # EVALUATION PHASE
            # ----------------------------------------------------------------
            (current_fitness_scores,
             generation_best_fitness,
             generation_average_fitness,
             generation_worst_fitness) = self._evaluate_entire_population(current_population)

            # Calculate improvement percentage
            if previous_average_fitness is None:
                improvement_percentage = None
            else:
                denominator = (abs(previous_average_fitness)
                               if abs(previous_average_fitness) > 1e-9 else 1e-9)
                improvement_percentage = (
                        (generation_average_fitness - previous_average_fitness)
                        / denominator * 100.0
                )

            previous_average_fitness = generation_average_fitness

            # ----------------------------------------------------------------
            # RECORD GENERATION STATISTICS
            # ----------------------------------------------------------------
            generation_record = {
                "generation": generation_number,
                "best": generation_best_fitness,
                "avg": generation_average_fitness,
                "worst": generation_worst_fitness,
                "improvement": improvement_percentage,
                "mutation_rate": current_mutation_rate,
            }
            self.generation_history.append(generation_record)

            # ----------------------------------------------------------------
            # CHECK TERMINATION CONDITIONS
            # ----------------------------------------------------------------
            should_terminate = (
                    generation_number + 1 >= minimum_generations and
                    improvement_percentage is not None and
                    improvement_percentage < 1.0  # Less than 1% improvement
            )

            if should_terminate:
                print(f"Terminating at generation {generation_number + 1}: "
                      f"Improvement ({improvement_percentage:.2f}%) < 1%")
                break

            # ----------------------------------------------------------------
            # ADAPTIVE MUTATION ADJUSTMENT
            # ----------------------------------------------------------------
            if use_adaptive_mutation and generation_number > 0 and generation_number % 20 == 0:
                if improvement_percentage is not None and improvement_percentage > 0.1:
                    # Halve mutation rate if it's helping
                    current_mutation_rate = current_mutation_rate / 2.0
                    print(f"Generation {generation_number + 1}: "
                          f"Reducing mutation rate to {current_mutation_rate:.4f}")

            # ----------------------------------------------------------------
            # SELECTION PHASE
            # ----------------------------------------------------------------
            selection_probabilities = calculate_softmax_probabilities(current_fitness_scores)
            number_of_parent_pairs = population_size - elitism_count
            parent_combinations = select_parent_pairs(
                current_population, selection_probabilities, number_of_parent_pairs
            )

            # ----------------------------------------------------------------
            # REPRODUCTION PHASE (Crossover + Mutation)
            # ----------------------------------------------------------------
            offspring_schedules = []

            for parent_a, parent_b in parent_combinations:
                # Crossover
                if crossover_method == "uniform":
                    child_schedule = perform_uniform_crossover(parent_a, parent_b)
                else:  # Default to single-point
                    child_schedule = perform_single_point_crossover(parent_a, parent_b)

                # Mutation
                apply_mutation(child_schedule, mutation_probability=current_mutation_rate)

                offspring_schedules.append(child_schedule)

            # ----------------------------------------------------------------
            # ELITISM: Preserve best schedules
            # ----------------------------------------------------------------
            elite_schedules = select_best_schedules(
                current_population, current_fitness_scores, elitism_count
            )

            # ----------------------------------------------------------------
            # CREATE NEXT GENERATION
            # ----------------------------------------------------------------
            next_generation = elite_schedules + offspring_schedules

            # Ensure correct population size
            if len(next_generation) > population_size:
                next_generation = next_generation[:population_size]
            elif len(next_generation) < population_size:
                # Add more offspring if needed
                shortage = population_size - len(next_generation)
                next_generation.extend(offspring_schedules[:shortage])

            # Update population for next generation
            current_population = next_generation

        # ====================================================================
        # FINAL EVALUATION AND RESULT PREPARATION
        # ====================================================================
        print(f"Algorithm completed after {self.total_generations_run} generations")

        # Final population evaluation
        (final_fitness_scores,
         final_best_fitness,
         final_average_fitness,
         final_worst_fitness) = self._evaluate_entire_population(current_population)

        # Find best schedule
        best_schedule_index = max(
            range(len(current_population)),
            key=lambda i: final_fitness_scores[i]
        )
        optimal_schedule = current_population[best_schedule_index]

        # Calculate violations for the best schedule
        fitness_calculator.calculate_constraint_violations(optimal_schedule)

        # Store final mutation rate
        self.final_mutation_rate = current_mutation_rate

        # Prepare results
        results = {
            "best_schedule": optimal_schedule,
            "history": self.generation_history,
            "final_mutation_rate": current_mutation_rate,
            "generations_run": self.total_generations_run,
            "final_fitness_scores": {
                "best": final_best_fitness,
                "average": final_average_fitness,
                "worst": final_worst_fitness,
            }
        }

        return results


# Convenience function
def execute_genetic_algorithm(**kwargs):
    """
    Convenience wrapper for running the genetic algorithm.

    Returns:
        Results dictionary from GeneticAlgorithmEngine.run_optimization()
    """
    engine = GeneticAlgorithmEngine()
    return engine.run_optimization(**kwargs)


