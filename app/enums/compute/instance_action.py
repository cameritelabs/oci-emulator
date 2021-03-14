from enum import Enum
from typing import Optional

from app.enums.compute.lifecycle_state import LifecycleState


class InstanceAction(Enum):
    START = [LifecycleState.STARTING, LifecycleState.RUNNING]
    STOP = [LifecycleState.STOPPED]
    RESET = [LifecycleState.STOPPED, LifecycleState.STARTING, LifecycleState.RUNNING]
    SOFTSTOP = [LifecycleState.STOPPING, LifecycleState.STOPPED]
    SOFTRESET = [
        LifecycleState.STOPPING,
        LifecycleState.STOPPED,
        LifecycleState.STARTING,
        LifecycleState.RUNNING,
    ]
    SENDDIAGNOSTICINTERRUPT = []

    def parse_str_to_enum(value: str) -> Optional["InstanceAction"]:
        value = value.upper()

        if value in list(InstanceAction.__members__.keys()):
            return InstanceAction[value]

        return None
