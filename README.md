# UHP Python SDK

The UHP Python SDK (`uhp-py-sdk`) aims to provide a thin, correct, agent-friendly Python SDK that implements the Universal Hiring Protocol (UHP). This SDK focuses on encapsulating protocol semantics, validating state transitions, and enforcing privacy rules, specifically avoiding product logic, UI assumptions, or platform coupling.

## Features

This SDK provides a robust and compliant interface for the Universal Hiring Protocol, including:

*   **Pydantic v2 Models:** For all canonical protocol objects, ensuring data validation and integrity.
*   **Protocol State Machines:** Explicit logic to manage and validate state transitions within the UHP (e.g., Application and Consent state machines).
*   **Privacy Enforcement Module:** Functions to filter visible fields based on consent and visibility levels, and to assert purpose binding.
*   **Intent-Based Actions:** A structured approach for AI agents to perform actions like applying for jobs.
*   **Capability Discovery:** Mechanisms for agents to introspect and understand the supported capabilities of the SDK.
*   **Structured Error Handling:** Machine-readable error messages for graceful recovery by agents, with custom exception classes.
*   **Practical Example Implementations:** Demonstrations of how to use the SDK for various scenarios, including a candidate agent, an employer agent reviewing anonymized profiles, and a privacy violation scenario.

## Installation

To install the UHP Python SDK and its dependencies, first ensure you have Python (3.x recommended) and `pip` installed. Then, navigate to the project root directory and run:

```bash
pip install -r requirements.txt
```

## Usage

The SDK is designed to be integrated into AI agents and Python applications. You can explore the `examples/` directory for practical demonstrations:

*   `examples/candidate_agent.py`: Demonstrates how a candidate agent can apply for a job.
*   `examples/employer_agent.py`: Shows how an employer agent can review anonymized candidate profiles while respecting privacy rules.
*   `examples/privacy_violation.py`: Illustrates how the SDK prevents privacy violations through its enforcement mechanisms.

To run an example, navigate to the project root and execute it with Python:

```bash
python examples/candidate_agent.py
```

## Testing

The project uses `pytest` for unit and integration testing. To run all tests, ensure you have installed the development dependencies (as per the Installation section) and then execute:

```bash
pytest tests/uhp/
```

## Contributing

Contributions are welcome! Please follow the project's established conventions and the workflow outlined in `workflow.md`.

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.
