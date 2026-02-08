# Plan: Implement Core UHP Data Models using Pydantic v2

## Phase 1: Implement Job and CandidateProfile Models

- [ ] Task: Write tests for the `Job` model
    - [ ] Create `tests/uhp/models/test_job.py`
    - [ ] Define tests for `Job` model instantiation (valid/invalid data)
    - [ ] Define tests for `Job` model immutability
    - [ ] Confirm tests fail (Red phase)
- [ ] Task: Implement the `Job` model
    - [ ] Create `uhp/models/job.py`
    - [ ] Define `Job` Pydantic v2 model as per `DESIGN.md`
    - [ ] Implement `model_config` for frozen and extra='forbid'
    - [ ] Add type hints for all fields
    - [ ] Run tests and confirm they pass (Green phase)
- [ ] Task: Write tests for the `CandidateProfile` model
    - [ ] Create `tests/uhp/models/test_candidate.py`
    - [ ] Define tests for `CandidateProfile` model instantiation (valid/invalid data)
    - [ ] Define tests for `CandidateProfile` model immutability
    - [ ] Confirm tests fail (Red phase)
- [ ] Task: Implement the `CandidateProfile` model
    - [ ] Create `uhp/models/candidate.py`
    - [ ] Define `CandidateProfile` Pydantic v2 model (anonymized only) as per `DESIGN.md`
    - [ ] Implement `model_config` for frozen and extra='forbid'
    - [ ] Add type hints for all fields
    - [ ] Run tests and confirm they pass (Green phase)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Implement Job and CandidateProfile Models' (Protocol in workflow.md)

## Phase 2: Implement Application and Consent Models

- [ ] Task: Write tests for the `Application` model
    - [ ] Update `tests/uhp/models/test_application.py` (or create if not exists)
    - [ ] Define tests for `Application` model instantiation (valid/invalid data)
    - [ ] Define tests for `Application` model immutability
    - [ ] Confirm tests fail (Red phase)
- [ ] Task: Implement the `Application` model
    - [ ] Create `uhp/models/application.py`
    - [ ] Define `Application` Pydantic v2 model as per `DESIGN.md`
    - [ ] Implement `model_config` for frozen and extra='forbid'
    - [ ] Add type hints for all fields
    - [ ] Run tests and confirm they pass (Green phase)
- [ ] Task: Write tests for the `Consent` model
    - [ ] Update `tests/uhp/models/test_consent.py` (or create if not exists)
    - [ ] Define tests for `Consent` model instantiation (valid/invalid data)
    - [ ] Define tests for `Consent` model immutability
    - [ ] Confirm tests fail (Red phase)
- [ ] Task: Implement the `Consent` model
    - [ ] Create `uhp/models/consent.py`
    - [ ] Define `Consent` Pydantic v2 model as per `DESIGN.md`
    - [ ] Implement `model_config` for frozen and extra='forbid'
    - [ ] Add type hints for all fields
    - [ ] Run tests and confirm they pass (Green phase)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Implement Application and Consent Models' (Protocol in workflow.md)

## Phase 3: Implement CapabilityDescriptor Model and Package Structure

- [ ] Task: Write tests for the `CapabilityDescriptor` model
    - [ ] Update `tests/uhp/models/test_capability.py` (or create if not exists)
    - [ ] Define tests for `CapabilityDescriptor` model instantiation (valid/invalid data)
    - [ ] Define tests for `CapabilityDescriptor` model immutability
    - [ ] Confirm tests fail (Red phase)
- [ ] Task: Implement the `CapabilityDescriptor` model
    - [ ] Create `uhp/models/capability.py`
    - [ ] Define `CapabilityDescriptor` Pydantic v2 model as per `DESIGN.md`
    - [ ] Implement `model_config` for frozen and extra='forbid'
    - [ ] Add type hints for all fields
    - [ ] Run tests and confirm they pass (Green phase)
- [ ] Task: Finalize `uhp/models/__init__.py`
    - [ ] Create `uhp/models/__init__.py` if it doesn't exist
    - [ ] Ensure all implemented models are importable from `uhp.models`
- [ ] Task: Ensure `uhp/__init__.py` exists
    - [ ] Create `uhp/__init__.py` if it doesn't exist
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Implement CapabilityDescriptor Model and Package Structure' (Protocol in workflow.md)
