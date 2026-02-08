# Product Definition: UHP Python SDK

## Initial Concept
The UHP Python SDK (`uhp-py-sdk`) aims to provide a thin, correct, agent-friendly Python SDK that implements the Universal Hiring Protocol (UHP). This SDK focuses on encapsulating protocol semantics, validating state transitions, and enforcing privacy rules, specifically avoiding product logic, UI assumptions, or platform coupling.

## Target Users
The primary target users for the UHP Python SDK are:
- **AI Agents:** This includes chatbots, autonomous agents, and planners that need to interact with the Universal Hiring Protocol programmatically. The SDK is designed with an "agent-first usage" philosophy, prioritizing predictability and machine reasoning.
- **Developers:** Python developers who need to integrate UHP functionalities into their applications, acting as a robust and compliant interface for the protocol.

## Core Goals and Vision
The vision for the UHP Python SDK is to be the definitive, minimalistic, and highly compliant interface for the Universal Hiring Protocol in Python. Its core goals include:
- **Protocol Fidelity:** Strictly adhere to the UHP specification, ensuring correct implementation of protocol semantics.
- **Agent Empowerment:** Provide a predictable and explicit API that empowers AI agents to interact with the protocol reliably.
- **Privacy by Design:** Embed strong privacy enforcement mechanisms, validating consent states and visibility levels to prevent data misuse.
- **Stateless Operation:** Maintain a stateless design by default, enabling flexible integration into various architectural patterns.
- **Models-First Approach:** Leverage Pydantic v2 for canonical, immutable data models that are central to the SDK's operation and ensure data integrity.

## Key Features
- **Pydantic v2 Models:** For all canonical protocol objects, ensuring data validation and integrity.
- **Protocol State Machines:** Explicit logic to manage and validate state transitions within the UHP.
- **Privacy Enforcement Module:** Functions to filter visible fields based on consent and purpose binding.
- **Intent-Based Actions:** A structured approach for agents to perform actions like applying for jobs, withdrawing applications, and managing consent.
- **Capability Discovery:** Mechanisms for agents to introspect and understand the supported capabilities of the SDK.
- **Structured Error Handling:** Machine-readable error messages for graceful recovery by agents.
