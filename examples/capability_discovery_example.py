import sys
import os
import importlib
import pkgutil
import json # Import json for pretty printing schemas
import inspect

# Add current project root to sys.path if not already there, for local testing and examples
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import necessary components from the UHP SDK
import uhp # Import uhp at the top level
from uhp.capabilities import discover_capabilities
from uhp.capabilities.decorators import uhp_capability
from uhp.capabilities.registry import capability_registry, process_and_register_capabilities_from_module
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Define a simple Pydantic model for a capability input
class SearchQuery(BaseModel):
    keyword: str = Field(..., description="The keyword to search for.")
    max_results: Optional[int] = Field(10, description="Maximum number of results to return.")

# Define a simple Pydantic model for a capability output
class SearchResult(BaseModel):
    results: List[str] = Field(..., description="List of search results.")
    total_found: int = Field(..., description="Total number of items found.")

# --- Define some example capabilities using the decorator ---

@uhp_capability
def search_documents(query: SearchQuery) -> SearchResult:
    """
    Searches for documents matching a given query.
    """
    print(f"Executing search_documents for keyword: {query.keyword}, max_results: {query.max_results}")
    # In a real scenario, this would interact with a document store
    found_docs = [f"Doc_{i}" for i in range(query.max_results or 10) if query.keyword in f"Doc_{i}"]
    return SearchResult(results=found_docs, total_found=len(found_docs))

@uhp_capability
def get_system_health() -> Dict[str, Any]:
    """
    Retrieves the current health status of the system.
    """
    print("Executing get_system_health...")
    return {"status": "healthy", "uptime_days": 120}

@uhp_capability
class UserProfileFetcher:
    """
    A class-based capability to fetch user profiles.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id

    def execute(self) -> Dict[str, Any]:
        """
        Fetches the profile for the initialized user_id.
        """
        print(f"Executing UserProfileFetcher for user_id: {self.user_id}")
        return {"id": self.user_id, "name": f"User {self.user_id}", "email": f"user{self.user_id}@example.com"}

# --- Main execution block to demonstrate discovery ---
if __name__ == "__main__":
    print("--- Demonstrating UHP Capability Discovery ---")

    # Ensure the registry is clear for this example run
    capability_registry._registry.clear()

    # Get a reference to this module itself
    current_module = sys.modules[__name__]
    
    # Process and register capabilities defined within this example script
    process_and_register_capabilities_from_module(current_module)

    capabilities = discover_capabilities()

    if capabilities:
        print(f"\nDiscovered {len(capabilities)} capabilities:")
        for cap in capabilities:
            print(f"\n--- Capability: {cap.id} ---")
            print(f"  Description: {cap.description}")
            print(f"  Input Schema: {json.dumps(cap.input_schema, indent=2)}") # Use json.dumps
            print(f"  Output Schema: {json.dumps(cap.output_schema, indent=2)}") # Use json.dumps
            if cap.examples:
                print(f"  Examples: {cap.examples}")
            else:
                print("  Examples: None provided.")
    else:
        print("\nNo UHP capabilities discovered.")

    # Example of using a discovered capability (conceptually)
    print("\n--- Demonstrating conceptual usage of a discovered capability ---")
    search_cap_found = next((cap for cap in capabilities if cap.id == "search_documents"), None)
    if search_cap_found:
        print(f"Found search_documents capability. Input schema: {json.dumps(search_cap_found.input_schema, indent=2)}") # Use json.dumps
        # In a real agent, it would use this schema to construct a valid input
        # and then dynamically call the underlying function/class.
        # For this example, we just show constructing input based on the schema.
        try:
            sample_input = SearchQuery(keyword="UHP", max_results=5)
            print(f"Sample input for search_documents: {sample_input.model_dump_json(indent=2)}")
            # Conceptual call: result = search_cap_found.execute(sample_input)
            # Actual execution requires reflection and is beyond this example's scope.
            print("Conceptual execution of search_documents with sample input would occur here.")
        except Exception as e:
            print(f"Error creating sample input: {e}")
    else:
        print("search_documents capability not found.")