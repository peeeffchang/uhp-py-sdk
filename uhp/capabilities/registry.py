from uhp.models.capability import Capability
from typing import Dict, List, Optional
from types import ModuleType
from uhp.capabilities.scanner import scan_for_capabilities

class _CapabilityRegistry: # Renamed to an internal class
    """
    An internal registry for discovering and managing UHP capabilities.
    """
    _registry: Dict[str, Capability] = {}

    def __init__(self):
        # Clear registry for fresh start in testing/re-initialization.
        # This is primarily for test isolation; in production, it's usually initialized once.
        self._registry = {} 

    def register(self, capability: Capability):
        """
        Registers a capability.
        """
        if capability.id in self._registry:
            # Optionally raise an error or log a warning if a capability is registered twice
            # For now, let's allow re-registration to simplify, but in a robust system, this needs thought.
            pass 
        self._registry[capability.id] = capability

    def get(self, capability_id: str) -> Optional[Capability]:
        """
        Retrieves a capability by its ID.
        """
        return self._registry.get(capability_id)

    def describe_all(self) -> List[Capability]:
        """
        Returns a list of all registered capabilities.
        """
        return list(self._registry.values())

# Create a module-level instance of the registry to ensure it's a singleton (or at least, its state is shared)
capability_registry = _CapabilityRegistry()

def process_and_register_capabilities_from_module(module: ModuleType):
    """
    Scans a module for capabilities, converts them to `Capability` models,
    and registers them in the global `capability_registry`.
    """
    discovered_capabilities = scan_for_capabilities(module)
    for cap_model in discovered_capabilities:
        capability_registry.register(cap_model)

