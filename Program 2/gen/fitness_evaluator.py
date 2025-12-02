"""
Fitness function implementation for SLA scheduling.
Implements all rules from Appendix A of the assignment.
"""
from typing import Dict, List, Tuple
from gen.constants import (
    ACTIVITY_DEFINITIONS,
    ROOMS_WITH_CAPACITIES,
    ALL_TIME_SLOTS,
    SLA101_SECTIONS,
    SLA191_SECTIONS,
    CROSS_SECTION_PAIRS
)


class FitnessCalculator:
    """
    Calculates fitness scores and constraint violations for schedules.
    Implements all rules from Appendix A.
    """

    def __init__(self):
        # Cache for performance optimization
        self._fitness_cache = {}

        # Time slot indices for calculating hour differences
        self._time_slot_indices = {
            time_slot: index for index, time_slot in enumerate(ALL_TIME_SLOTS)
        }

    def _calculate_hour_difference(self, time_slot_1: str, time_slot_2: str) -> int:
        """
        Calculate the number of hours between two time slots.

        Args:
            time_slot_1: First time slot (e.g., "10 AM")
            time_slot_2: Second time slot

        Returns:
            Absolute hour difference (0 for same slot, 1 for consecutive, etc.)
        """
        idx1 = self._time_slot_indices.get(time_slot_1)
        idx2 = self._time_slot_indices.get(time_slot_2)

        if idx1 is None or idx2 is None:
            return 0

        return abs(idx1 - idx2)

    def _is_room_in_beach_or_roman(self, room_name: str) -> bool:
        """
        Check if a room is in the Beach or Roman building.

        Args:
            room_name: Name of the room

        Returns:
            True if room is in Beach or Roman building, False otherwise
        """
        if not room_name:
            return False

        return room_name.startswith("Beach") or room_name.startswith("Roman")

    def _evaluate_room_size(self, activity_name: str, room_name: str) -> float:
        """
        Calculate fitness contribution based on room size vs expected enrollment.

        Returns:
            Fitness score for room size (-0.5 to +0.3)
        """
        if not room_name or activity_name not in ACTIVITY_DEFINITIONS:
            return 0.0

        expected = ACTIVITY_DEFINITIONS[activity_name]["expected_enrollment"]
        capacity = ROOMS_WITH_CAPACITIES.get(room_name, 0)

        # Room too small
        if capacity < expected:
            return -0.5

        # Calculate room utilization ratio
        utilization_ratio = capacity / expected

        if utilization_ratio > 3.0:
            return -0.4  # Way too big
        elif utilization_ratio > 1.5:
            return -0.2  # Too big
        else:
            return 0.3  # Good fit

    def _evaluate_facilitator_preference(self, activity_name: str, facilitator: str) -> float:
        """
        Calculate fitness based on facilitator preference level.

        Returns:
            Fitness score for facilitator (0.5, 0.2, or -0.1)
        """
        if not facilitator or activity_name not in ACTIVITY_DEFINITIONS:
            return 0.0

        activity_info = ACTIVITY_DEFINITIONS[activity_name]

        if facilitator in activity_info["preferred_facilitators"]:
            return 0.5
        elif facilitator in activity_info["acceptable_facilitators"]:
            return 0.2
        else:
            return -0.1

    def _evaluate_section_spacing(self, section_1: str, section_2: str, schedule) -> float:
        """
        Evaluate spacing rules for two sections of the same course.

        Returns:
            +0.5 if >4 hours apart, -0.5 if same time, 0 otherwise
        """
        assign_1 = schedule.assignments[section_1]
        assign_2 = schedule.assignments[section_2]

        if not assign_1.time or not assign_2.time:
            return 0.0

        if assign_1.time == assign_2.time:
            return -0.5  # Same time penalty

        hour_diff = self._calculate_hour_difference(assign_1.time, assign_2.time)

        if hour_diff > 4:
            return 0.5  # Good spacing bonus

        return 0.0

    def _evaluate_cross_section_interaction(self, section_101: str, section_191: str, schedule) -> float:
        """
        Evaluate interaction rules between SLA101 and SLA191 sections.

        Returns:
            Fitness score for this specific pair
        """
        assign_101 = schedule.assignments[section_101]
        assign_191 = schedule.assignments[section_191]

        if not assign_101.time or not assign_191.time:
            return 0.0

        # Same time slot penalty
        if assign_101.time == assign_191.time:
            return -0.25

        hour_diff = self._calculate_hour_difference(assign_101.time, assign_191.time)

        # Consecutive time slots
        if hour_diff == 1:
            score = 0.5  # Consecutive bonus

            # Check building mismatch penalty
            room_101_is_special = self._is_room_in_beach_or_roman(assign_101.room)
            room_191_is_special = self._is_room_in_beach_or_roman(assign_191.room)

            if room_101_is_special != room_191_is_special:  # XOR: one special, one not
                score -= 0.4  # Building mismatch penalty

            return score

        # One hour gap
        if hour_diff == 2:
            return 0.25

        return 0.0

    def calculate_schedule_fitness(self, schedule) -> float:
        """
        Calculate total fitness score for a complete schedule.

        Args:
            schedule: Schedule object to evaluate

        Returns:
            Total fitness score (sum of all activity scores + special rules)
        """
        # Generate cache key from assignments
        cache_key = hash(str([(a.room, a.time, a.facilitator)
                              for a in schedule.assignments.values()]))

        # Return cached result if available
        if cache_key in self._fitness_cache:
            schedule.fitness = self._fitness_cache[cache_key]
            return schedule.fitness

        total_score = 0.0

        # Data structures for conflict detection
        room_time_usage = {}
        facilitator_time_usage = {}
        facilitator_total_load = {}

        # ====================================================================
        # FIRST PASS: Collect usage data and calculate basic scores
        # ====================================================================
        for activity_name, assignment in schedule.assignments.items():
            # Track room-time usage for conflict detection
            if assignment.room and assignment.time:
                room_time_key = (assignment.room, assignment.time)
                room_time_usage[room_time_key] = room_time_usage.get(room_time_key, 0) + 1

            # Track facilitator-time usage
            if assignment.facilitator and assignment.time:
                facilitator_time_key = (assignment.facilitator, assignment.time)
                facilitator_time_usage[facilitator_time_key] = (
                        facilitator_time_usage.get(facilitator_time_key, 0) + 1
                )

            # Track total facilitator load
            if assignment.facilitator:
                facilitator_total_load[assignment.facilitator] = (
                        facilitator_total_load.get(assignment.facilitator, 0) + 1
                )

        # ====================================================================
        # SECOND PASS: Calculate scores for each activity
        # ====================================================================
        for activity_name, assignment in schedule.assignments.items():
            activity_score = 0.0

            # 1. Room size score
            activity_score += self._evaluate_room_size(activity_name, assignment.room)

            # 2. Facilitator preference score
            activity_score += self._evaluate_facilitator_preference(activity_name, assignment.facilitator)

            # 3. Room-time conflict penalty
            if assignment.room and assignment.time:
                room_time_key = (assignment.room, assignment.time)
                if room_time_usage.get(room_time_key, 0) > 1:
                    activity_score -= 0.5

            # 4. Facilitator same-time score
            if assignment.facilitator and assignment.time:
                facilitator_time_key = (assignment.facilitator, assignment.time)
                concurrent_count = facilitator_time_usage.get(facilitator_time_key, 0)

                if concurrent_count == 1:
                    activity_score += 0.2  # Sole facilitator bonus
                elif concurrent_count > 1:
                    activity_score -= 0.2  # Conflict penalty

            # 5. Facilitator total load penalties
            if assignment.facilitator:
                total_load = facilitator_total_load.get(assignment.facilitator, 0)

                if total_load > 4:
                    activity_score -= 0.5  # Overload penalty
                elif total_load < 3:
                    # Special rule for Dr. Tyler
                    if assignment.facilitator == "Tyler":
                        if total_load >= 2:  # Tyler penalty only if 2 or more but less than 3
                            activity_score -= 0.4
                    else:
                        activity_score -= 0.4  # Underload penalty

            total_score += activity_score

        # ====================================================================
        # THIRD PASS: Apply special section rules
        # ====================================================================
        # SLA101 sections spacing
        total_score += self._evaluate_section_spacing(SLA101_SECTIONS[0], SLA101_SECTIONS[1], schedule)

        # SLA191 sections spacing
        total_score += self._evaluate_section_spacing(SLA191_SECTIONS[0], SLA191_SECTIONS[1], schedule)

        # Cross-section interactions
        for section_101, section_191 in CROSS_SECTION_PAIRS:
            total_score += self._evaluate_cross_section_interaction(section_101, section_191, schedule)

        # Cache and return result
        self._fitness_cache[cache_key] = total_score
        schedule.fitness = total_score

        return total_score

    def calculate_constraint_violations(self, schedule) -> Dict:
        """
        Count all constraint violations in a schedule.

        Args:
            schedule: Schedule object to analyze

        Returns:
            Dictionary with counts for each violation type
        """
        violation_counts = {
            "room_conflicts": 0,
            "room_too_small": 0,
            "room_too_big_15": 0,  # >1.5x capacity
            "room_too_big_30": 0,  # >3x capacity
            "facilitator_overload": 0,
            "facilitator_underload": 0,
            "facilitator_same_time_conflict": 0,
            "sla101_same_time": 0,
            "sla191_same_time": 0,
            "sla101_191_same_time": 0,
            "sla101_191_building_mismatch": 0,
            "sla101_191_one_hour_gap": 0,
            "sla101_191_consecutive_pair": 0,
        }

        # Data collection for conflict analysis
        room_time_counts = {}
        facilitator_time_counts = {}
        facilitator_total_counts = {}

        # ====================================================================
        # FIRST PASS: Collect data and check individual violations
        # ====================================================================
        for activity_name, assignment in schedule.assignments.items():
            # Room-time conflicts
            if assignment.room and assignment.time:
                key = (assignment.room, assignment.time)
                room_time_counts[key] = room_time_counts.get(key, 0) + 1

            # Facilitator-time conflicts
            if assignment.facilitator and assignment.time:
                key = (assignment.facilitator, assignment.time)
                facilitator_time_counts[key] = facilitator_time_counts.get(key, 0) + 1

            # Facilitator total load
            if assignment.facilitator:
                facilitator_total_counts[assignment.facilitator] = (
                        facilitator_total_counts.get(assignment.facilitator, 0) + 1
                )

            # Room size violations
            if activity_name in ACTIVITY_DEFINITIONS and assignment.room:
                expected = ACTIVITY_DEFINITIONS[activity_name]["expected_enrollment"]
                capacity = ROOMS_WITH_CAPACITIES.get(assignment.room, 0)

                if capacity < expected:
                    violation_counts["room_too_small"] += 1
                elif capacity > 0 and expected > 0:
                    ratio = capacity / expected
                    if ratio > 3.0:
                        violation_counts["room_too_big_30"] += 1
                    elif ratio > 1.5:
                        violation_counts["room_too_big_15"] += 1

        # ====================================================================
        # SECOND PASS: Count conflicts from collected data
        # ====================================================================
        # Room-time conflicts
        for count in room_time_counts.values():
            if count > 1:
                violation_counts["room_conflicts"] += count - 1

        # Facilitator total load violations
        for facilitator, total in facilitator_total_counts.items():
            if total > 4:
                violation_counts["facilitator_overload"] += 1
            elif total < 3:
                if facilitator == "Tyler":
                    if total >= 2:
                        violation_counts["facilitator_underload"] += 1
                else:
                    violation_counts["facilitator_underload"] += 1

        # Facilitator same-time conflicts
        for count in facilitator_time_counts.values():
            if count > 1:
                violation_counts["facilitator_same_time_conflict"] += count - 1

        # ====================================================================
        # THIRD PASS: Special section violations
        # ====================================================================
        # SLA101 sections same time
        assign_101a = schedule.assignments[SLA101_SECTIONS[0]]
        assign_101b = schedule.assignments[SLA101_SECTIONS[1]]
        if assign_101a.time and assign_101b.time and assign_101a.time == assign_101b.time:
            violation_counts["sla101_same_time"] += 1

        # SLA191 sections same time
        assign_191a = schedule.assignments[SLA191_SECTIONS[0]]
        assign_191b = schedule.assignments[SLA191_SECTIONS[1]]
        if assign_191a.time and assign_191b.time and assign_191a.time == assign_191b.time:
            violation_counts["sla191_same_time"] += 1

        # Cross-section analysis
        for section_101, section_191 in CROSS_SECTION_PAIRS:
            assign_101 = schedule.assignments[section_101]
            assign_191 = schedule.assignments[section_191]

            if not assign_101.time or not assign_191.time:
                continue

            # Same time slot
            if assign_101.time == assign_191.time:
                violation_counts["sla101_191_same_time"] += 1
                continue

            hour_diff = self._calculate_hour_difference(assign_101.time, assign_191.time)

            # Consecutive slots
            if hour_diff == 1:
                violation_counts["sla101_191_consecutive_pair"] += 1

                # Check building mismatch
                if assign_101.room and assign_191.room:
                    room_101_special = self._is_room_in_beach_or_roman(assign_101.room)
                    room_191_special = self._is_room_in_beach_or_roman(assign_191.room)
                    if room_101_special != room_191_special:
                        violation_counts["sla101_191_building_mismatch"] += 1

            # One hour gap
            elif hour_diff == 2:
                violation_counts["sla101_191_one_hour_gap"] += 1

        # Store violations in schedule
        schedule.violations = violation_counts

        return violation_counts


# Global instance for convenience
fitness_calculator = FitnessCalculator()


