# Technology Stack: UHP Python SDK

## Core Technologies

- **Programming Language:** Python
  - **Rationale:** The project is explicitly defined as a Python SDK (`uhp-py-sdk`), and the `DESIGN.md` outlines Python-specific constructs and libraries.

- **Data Modeling Framework:** Pydantic v2
  - **Rationale:** The `DESIGN.md` explicitly mandates the use of "Pydantic v2" for canonical protocol objects, emphasizing features like immutability by default, validation of required fields, and rejection of unknown fields (strict mode). This is central to the SDK's "models-first" approach for defining UHP data structures.

## Other Considerations (Inferred from Design)

- **Protocol Specification:** Universal Hiring Protocol (UHP) v0.1-ESSENTIAL
  - **Rationale:** The entire SDK is built to implement and interact with this specific protocol version.

- **Architectural Style:** Library/SDK with a focus on clear separation of concerns (models, enums, actions, state machines, privacy, transport adapters).
  - **Rationale:** The `DESIGN.md` details a modular structure intended for an SDK, emphasizing statelessness by default and agent-first usage without embedding product logic or UI assumptions.

- **Testing Framework:** (Implicit)
  - **Rationale:** While not explicitly named, the `DESIGN.md` outlines a `tests/` directory with `test_state_machine.py`, `test_privacy.py`, and `test_actions.py`, indicating a standard Python testing framework (likely `pytest`) will be used.

- **Package Management:** (Implicit)
  - **Rationale:** The `DESIGN.md` proposes a `pyproject.toml` file, which is common for modern Python projects using tools like Poetry or Flit for dependency management and packaging.
