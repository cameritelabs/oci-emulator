from enum import Enum, auto


class LifecycleState(Enum):
    MOVING = auto()
    PROVISIONING = auto()
    RUNNING = auto()
    STARTING = auto()
    STOPPING = auto()
    STOPPED = auto()
    CREATING_IMAGE = auto()
    TERMINATING = auto()
    TERMINATED = auto()
