# Product Guidelines: UHP Python SDK

## Documentation and Messaging Tone
The external documentation, API references, and all messaging related to the UHP Python SDK should adopt a **Formal, Technical, and Agent-Centric** tone. This approach is crucial to align with the SDK's core design philosophy and target audience.

- **Formal and Technical:** Emphasize precision, accuracy, and adherence to protocol specifications. Avoid colloquialisms or overly casual language. The language should be unambiguous and reflect the strict, predictable nature of the SDK.
- **Agent-Centric and Explicit:** Prioritize machine readability and explicit instructions. Documentation should be structured to facilitate consumption by AI agents, developers building agents, and automated tools. This means clear API contracts, detailed explanations of state transitions, error handling, and privacy enforcement mechanisms. Every piece of information should aim to be as explicit as possible, leaving no room for misinterpretation by automated systems or human developers.
- **Clear and Concise (Supporting Role):** While formal and agent-centric, clarity and conciseness should support the primary tone. Information should be presented efficiently, allowing for quick retrieval of essential details without unnecessary verbosity, as long as it doesn't compromise explicitness.

## Design Principles for SDK Usage
- **Predictability:** Users (especially agents) should be able to predict the behavior of the SDK under various inputs and states.
- **Explicitness:** All SDK functionalities, constraints, and contractual obligations (e.g., privacy rules) must be explicitly stated and enforced.
- **Machine Reasoning:** The SDK's design and documentation should support automated reasoning and analysis, enabling agents to understand and correctly interact with the protocol.

## Privacy and Compliance Communication
- All communication related to privacy, consent, and data handling must be exceptionally clear, precise, and compliant with relevant regulations, reflecting the "privacy-native constraints" of the UHP. The SDK's documentation should clearly articulate how it enforces privacy rules and validates consent states.
