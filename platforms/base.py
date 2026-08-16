from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

@dataclass
class PlatformSpec:
    platform: str
    vcpu: float = 0.5
    ram_mb: int = 256
    disk_gb: int = 1
    tier_name: str = "free"
    region: str = "unknown"
    driver_used: str = "unknown"

class GraphAdapter(ABC):
    name: str
    spec: PlatformSpec

    @abstractmethod
    def connect(self) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def load(self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, float]: ...
    @abstractmethod
    def query(self, workload: str, params: dict[str, Any]) -> Any: ...
    @abstractmethod
    def create_indexes(self) -> None: ...
