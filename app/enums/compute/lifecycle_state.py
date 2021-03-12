from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class LifecycleState(AutoName):
    MOVING = auto()
    PROVISIONING = auto()
    RUNNING = auto()
    STARTING = auto()
    STOPPING = auto()
    STOPPED = auto()
    CREATING_IMAGE = auto()
    TERMINATING = auto()
    TERMINATED = auto()
