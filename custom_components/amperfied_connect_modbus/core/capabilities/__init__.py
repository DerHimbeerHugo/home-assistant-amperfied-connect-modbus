"""Capability modules for the Amperfied Connect Modbus integration."""

from __future__ import annotations

from .base import Capability
from .core import CoreCapability
from .eco_mode import EcoModeCapability
from .phase_switch import PhaseSwitchCapability
from .phase_switch_duration import PhaseSwitchDurationCapability
from .standby import StandbyCapability
from .watchdog import WatchdogCapability

CAPABILITIES: tuple[type[Capability], ...] = (
    CoreCapability,
    StandbyCapability,
    WatchdogCapability,
    PhaseSwitchCapability,
    PhaseSwitchDurationCapability,
    EcoModeCapability,
)

__all__ = [
    "CAPABILITIES",
    "Capability",
    "CoreCapability",
    "EcoModeCapability",
    "PhaseSwitchCapability",
    "PhaseSwitchDurationCapability",
    "StandbyCapability",
    "WatchdogCapability",
]
