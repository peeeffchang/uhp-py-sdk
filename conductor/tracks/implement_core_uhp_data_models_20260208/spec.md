# Specification: Implement Core UHP Data Models using Pydantic v2

## 1. Overview
This specification details the implementation of the core data models for the Universal Hiring Protocol (UHP) Python SDK, leveraging Pydantic v2. The objective is to create robust, validated, and immutable data structures that accurately represent the UHP protocol objects as defined in the `DESIGN.md`.

## 2. Scope
The scope of this track is limited to the implementation of the foundational data models. It does not include:
- Implementation of enums (these are separate).
- Implementation of actions or state machines.
- Any transport layer (HTTP, mock).
- Persistence mechanisms.
- Business logic beyond data validation.

## 3. Core Models to Implement
Based on `DESIGN.md` Section 3.1 (`models/`), the minimal required models are:
- `Job`
- `CandidateProfile` (anonymized only)
- `Application`
- `Consent`
- `CapabilityDescriptor`

## 4. Technical Requirements

### 4.1. Pydantic v2 Usage
- All models MUST inherit from `pydantic.BaseModel`.
- Models MUST be configured to be immutable by default (e.g., using `model_config = {'frozen': True}` or `ConfigDict(frozen=True)`).
- Models MUST validate required fields.
- Models MUST reject unknown fields (strict mode, e.g., `model_config = {'extra': 'forbid'}` or `ConfigDict(extra='forbid')`).
- Type hints MUST be used comprehensively for all fields.

### 4.2. Data Validation
- Ensure that all fields are correctly typed and validated according to the UHP protocol's data requirements.
- Implement any specific custom validators if required by the protocol for complex data types or business rules (e.g., date formats, UUIDs, email addresses).

### 4.3. Modularity and Structure
- Each core model should ideally reside in its own Python file within the `uhp/models/` directory as proposed in `DESIGN.md` (e.g., `job.py`, `candidate.py`).
- An `__init__.py` file in `uhp/models/` should expose these models for easy import.

## 5. Definition of Done
- All five core models (`Job`, `CandidateProfile`, `Application`, `Consent`, `CapabilityDescriptor`) are implemented as Pydantic v2 models.
- Each model adheres to the technical requirements for immutability, validation, and strictness.
- Comprehensive unit tests are in place for each model, covering:
    - Successful instantiation with valid data.
    - Failure on missing required fields.
    - Failure on invalid data types.
    - Failure on unknown fields.
    - Immutability enforcement.
- Models are correctly integrated into the `uhp/models/` package structure.
