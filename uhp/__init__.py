from uhp.capabilities.registry import capability_registry, process_and_register_capabilities_from_module
from typing import List, Optional
from uhp.models.capability import Capability
from uhp.capabilities.decorators import uhp_capability
import pkgutil
import importlib
import sys
import os # Import os for os.getcwd() and os.path.abspath
from types import ModuleType # Import ModuleType

# Placeholder for SDK version (can be moved to a separate version.py later)
__version__ = "0.1.0"

# Auto-discovery of capabilities during SDK initialization
# This section will execute when the 'uhp' package is first imported.
def _initialize_capabilities(modules_to_scan: Optional[List[ModuleType]] = None):
    capability_registry._registry.clear()

    if modules_to_scan:
        # Scan explicitly provided modules (useful for testing)
        for module in modules_to_scan:
            try:
                process_and_register_capabilities_from_module(module)
            except Exception as e:
                print(f"Error during explicit capability discovery in module {module.__name__}: {e}", file=sys.stderr)
    else:
        # Default behavior: auto-discover from uhp.capabilities subpackages
        capabilities_package = importlib.import_module("uhp.capabilities")
        if hasattr(capabilities_package, '__path__'):
            for _, name, ispkg in pkgutil.walk_packages(capabilities_package.__path__):
                full_module_name = f"{capabilities_package.__name__}.{name}"
                if not ispkg:
                    try:
                        module = importlib.import_module(full_module_name)
                        process_and_register_capabilities_from_module(module)
                    except Exception as e:
                        print(f"Error during capability discovery in module {full_module_name}: {e}", file=sys.stderr)


# Call initialization on package import (default behavior)
_initialize_capabilities()


def discover_capabilities() -> List[Capability]:
    """
    Returns a list of all discovered and registered UHP capabilities.
    """
    return capability_registry.describe_all()