"""
Data models for representing schedules and assignments.
"""
from copy import deepcopy
from dataclasses import dataclass
import pandas as pd
from gen.constants import ACTIVITY_DEFINITIONS


@dataclass
class ActivityAssignment:
    """
    Represents the assignment for a single activity.
    Contains room, time slot, and facilitator.
    """
    room: str = None
    time: str = None
    facilitator: str = None

    def to_dict(self):
        """Convert to dictionary format for serialization."""
        return {
            "room": self.room,
            "time": self.time,
            "facilitator": self.facilitator
        }

    def copy(self):
        """Create a deep copy of this assignment."""
        return ActivityAssignment(self.room, self.time, self.facilitator)


class Schedule:
    """
    Represents a complete schedule for all SLA activities.
    Each schedule contains assignments for all 11 activities.
    """

    def __init__(self, assignments_dict=None):
        """
        Initialize a new schedule.

        Args:
            assignments_dict: Optional dictionary of {activity_name: ActivityAssignment}
                            If None, creates empty assignments for all activities.
        """
        self._fitness_score = None  # Cache for fitness calculation
        self._violation_summary = None  # Cache for violation counts

        if assignments_dict is None:
            # Create empty assignments for all activities
            self._assignments = {
                activity_name: ActivityAssignment()
                for activity_name in ACTIVITY_DEFINITIONS.keys()
            }
        else:
            self._assignments = assignments_dict

    @property
    def assignments(self):
        """Get the assignments dictionary."""
        return self._assignments

    @property
    def fitness(self):
        """Get the cached fitness score."""
        return self._fitness_score

    @fitness.setter
    def fitness(self, value):
        """Set the fitness score."""
        self._fitness_score = value

    @property
    def violations(self):
        """Get the cached violation summary."""
        return self._violation_summary

    @violations.setter
    def violations(self, value):
        """Set the violation summary."""
        self._violation_summary = value

    def create_copy(self):
        """
        Create a deep copy of this schedule.

        Returns:
            A new Schedule object with copied assignments.
        """
        copied_assignments = {
            activity_name: assignment.copy()
            for activity_name, assignment in self._assignments.items()
        }
        new_schedule = Schedule(copied_assignments)
        new_schedule._fitness_score = self._fitness_score
        return new_schedule

    def to_dataframe(self):
        """
        Convert schedule to pandas DataFrame for display and export.

        Returns:
            DataFrame with columns: Activity, Room, Time, Facilitator
        """
        schedule_records = []

        for activity_name, assignment in self._assignments.items():
            schedule_records.append({
                "Activity": activity_name,
                "Room": assignment.room,
                "Time": assignment.time,
                "Facilitator": assignment.facilitator,
            })

        return pd.DataFrame(schedule_records)

    def save_to_csv(self, filepath):
        """
        Save schedule to a CSV file.

        Args:
            filepath: Path where CSV file will be saved.
        """
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)

    def __str__(self):
        """String representation of schedule for debugging."""
        lines = ["COMPLETE SCHEDULE:"]
        lines.append("-" * 80)

        for activity_name, assignment in self._assignments.items():
            lines.append(
                f"{activity_name:8s} | "
                f"Room: {assignment.room or 'None':<12s} | "
                f"Time: {assignment.time or 'None':<6s} | "
                f"Facilitator: {assignment.facilitator or 'None':<10s}"
            )

        if self._fitness_score is not None:
            lines.append("-" * 80)
            lines.append(f"Fitness Score: {self._fitness_score:.2f}")

        return "\n".join(lines)