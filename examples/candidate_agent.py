import sys
import os
from datetime import datetime

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uhp.actions.apply import ApplyForJob
# from uhp.actions.withdraw import WithdrawApplication # Not yet implemented
from uhp.enums.application_state import ApplicationState
from uhp.models.application import Application
from uhp.models.job import Job

def demonstrate_candidate_agent():
    print("--- Candidate Agent Demonstration ---")

    # Scenario 1: Apply for a Job
    job = Job(title="Software Engineer", description="Develop awesome software.", is_remote=True)
    candidate_id = "candidate123"

    print("\n")
    print(f"Candidate '{candidate_id}' applying for job '{job.title}' (ID: {job.title})...")
    apply_action = ApplyForJob(job_id=job.title, candidate_id=candidate_id)
    new_application = apply_action.execute()

    print(f"Application created: ID={new_application.application_id}, Status={new_application.status}")
    assert new_application.status == ApplicationState.SUBMITTED

    # Scenario 2: Withdraw Application (Placeholder, as WithdrawApplication is not yet implemented)
    print("\n")
    print("--- Demonstrating Withdraw Application (Placeholder) ---")
    print("WithdrawApplication action would be demonstrated here once implemented.")
    # withdraw_action = WithdrawApplication(application_id=new_application.application_id, candidate_id=candidate_id)
    # updated_application = withdraw_action.execute()
    # assert updated_application.status == ApplicationState.WITHDRAWN
    print("Placeholder for WithdrawApplication complete.")

if __name__ == "__main__":
    demonstrate_candidate_agent()
