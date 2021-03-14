from enum import auto

from app.enums.auto_name import AutoName


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
