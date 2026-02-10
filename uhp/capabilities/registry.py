from uhp.models.capability import CapabilityDescriptor
from typing import Dict, List, Optional

class CapabilityRegistry:
    """
    A registry for discovering and managing UHP capabilities.
    """
    _registry: Dict[str, CapabilityDescriptor] = {}

    def __init__(self):
        # Clear registry for fresh start in testing/re-initialization
        self._registry = {}

    def register(self, descriptor: CapabilityDescriptor):
        """
        Registers a capability descriptor.
        """
        self._registry[descriptor.capability_id] = descriptor

    def get(self, capability_id: str) -> Optional[CapabilityDescriptor]:
        """
        Retrieves a capability descriptor by its ID.
        """
        return self._registry.get(capability_id)

    def describe_all(self) -> List[CapabilityDescriptor]:
        """
        Returns a list of all registered capability descriptors.
        """
        return list(self._registry.values())
