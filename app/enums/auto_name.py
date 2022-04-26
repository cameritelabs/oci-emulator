from enum import Enum


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
