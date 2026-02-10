import pytest
import subprocess
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_candidate_agent_example_runs_and_completes():
    example_path = os.path.join('examples', 'candidate_agent.py')
    # Assert that the script runs without errors and produces expected output
    try:
        result = subprocess.run(
            [sys.executable, example_path],
            check=True,
            capture_output=True,
            text=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Run from project root
        )
        # Check if expected output is present
        assert "--- Candidate Agent Demonstration ---" in result.stdout
        assert "Candidate 'candidate123' applying for job 'Software Engineer'" in result.stdout
        assert "Application created" in result.stdout
        assert "--- Demonstrating Withdraw Application (Placeholder) ---" in result.stdout
        assert "Placeholder for WithdrawApplication complete." in result.stdout
        print(result.stdout) # Print output for debugging if needed
    except subprocess.CalledProcessError as e:
        print(f"Example script failed with exit code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        pytest.fail(f"Candidate Agent Example script failed: {e.stderr}")
    except FileNotFoundError:
        pytest.fail(f"Candidate Agent Example script not found at {example_path}")

def test_employer_agent_example_runs_and_completes():
    example_path = os.path.join('examples', 'employer_agent.py')
    # Assert that the script runs without errors and produces expected output
    try:
        result = subprocess.run(
            [sys.executable, example_path],
            check=True,
            capture_output=True,
            text=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Run from project root
        )
        # Check if expected output is present
        assert "--- Employer Agent Demonstration ---" in result.stdout
        assert "Original Candidate Profile:" in result.stdout
        assert "Anonymized Profile for Employer Review" in result.stdout
        assert "Public Profile (PUBLIC visibility)" in result.stdout
        print(result.stdout) # Print output for debugging if needed
    except subprocess.CalledProcessError as e:
        print(f"Example script failed with exit code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        pytest.fail(f"Employer Agent Example script failed: {e.stderr}")
    except FileNotFoundError:
        pytest.fail(f"Employer Agent Example script not found at {example_path}")


def test_privacy_violation_example_runs_and_completes():
    example_path = os.path.join('examples', 'privacy_violation.py')
    # Assert that the script runs without errors and produces expected output
    try:
        result = subprocess.run(
            [sys.executable, example_path],
            check=True,
            capture_output=True,
            text=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Run from project root
        )
        # Check if expected output is present
        assert "--- Privacy Violation Demonstration ---" in result.stdout
        assert "Successfully prevented direct access to sensitive fields like email (anonymized)." in result.stdout
        assert "Privacy Violation Caught:" in result.stdout
        assert "Successfully prevented data usage for unapproved purpose." in result.stdout
        print(result.stdout) # Print output for debugging if needed
    except subprocess.CalledProcessError as e:
        print(f"Example script failed with exit code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        pytest.fail(f"Privacy Violation Example script failed: {e.stderr}")
    except FileNotFoundError:
        pytest.fail(f"Privacy Violation Example script not found at {example_path}")