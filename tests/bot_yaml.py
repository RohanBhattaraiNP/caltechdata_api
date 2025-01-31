import subprocess
import time
from unittest.mock import patch
import sys
import os
import json
import requests
from datetime import datetime
import pytest
import importlib.util
import traceback


class CaltechDataTester:
    def __init__(self):
        # Use GitHub Actions environment or create a local test directory
        self.test_dir = os.environ.get(
            "GITHUB_WORKSPACE", os.path.join(os.getcwd(), "caltech_test_data")
        )
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure test directory exists
        os.makedirs(self.test_dir, exist_ok=True)

        # Create test run directory
        self.test_run_dir = os.path.join(self.test_dir, f"test_run_{self.timestamp}")
        os.makedirs(self.test_run_dir, exist_ok=True)

        # Initialize logging
        self.log_file = os.path.join(self.test_run_dir, "test_log.txt")

    def log(self, message):
        """Log message to both console and file"""
        print(message)
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.now()}: {message}\n")

    def create_test_files(self):
        """Create necessary test files"""
        csv_path = os.path.join(self.test_run_dir, "test_data.csv")
        with open(csv_path, "w") as f:
            f.write("date,temperature,humidity\n")
            f.write("2023-01-01,25.5,60\n")
            f.write("2023-01-02,26.0,62\n")
            f.write("2023-01-03,24.8,65\n")

        self.log(f"Created test CSV file: {csv_path}")
        return csv_path

    def import_cli_module(self):
        """Dynamically import cli module from the correct path"""
        cli_path = os.path.join(
            os.environ.get("GITHUB_WORKSPACE", os.getcwd()), "caltechdata_api", "cli.py"
        )
        spec = importlib.util.spec_from_file_location("cli", cli_path)
        cli_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli_module)
        return cli_module

    def generate_test_responses(self):
        """Generate test responses for CLI prompts"""
        return {
            "Do you want to create or edit a CaltechDATA record? (create/edit): ": "create",
            "Would you like to load metadata from an existing file or enter new details? (existing/new): ": "new",
            "Enter the dataset title: ": f"Test Dataset {self.timestamp}",
            "Provide a brief description of the dataset: ": "Automated test dataset with sample climate data.",
            "Select the license by entering its corresponding number: ": "1",
            "Please enter your ORCID ID (e.g., 0000-0002-1825-0097): ": os.environ.get(
                "TEST_ORCID", "0000-0002-1825-0097"
            ),
            "How many funding sources would you like to add? ": "1",
            "Please enter the funding award number: ": "NSF-1234567",
            "What is the title of the funding award? ": "Automated Testing Grant",
            "Provide the ROR ID of the funding organization (https://ror.org): ": "021nxhr62",
            "Would you like to upload files, provide a link, or skip? (upload/link/skip): ": "upload",
            "Enter the filename to upload (or type 'done' to finish): ": "test_data.csv",
            "Do you want to add more files? (yes/no): ": "no",
            "Are you ready to submit this dataset to CaltechDATA? (yes/no): ": "yes",
        }

    def run_test_submission(self):
        """Run the complete test submission process"""
        try:
            self.log("Starting test submission process...")

            # Create test files
            test_csv = self.create_test_files()

            # Dynamically import cli module
            cli_module = self.import_cli_module()

            # Generate responses
            responses = self.generate_test_responses()

            # Setup output capture
            class OutputCapture:
                def __init__(self):
                    self.output = []

                def write(self, text):
                    self.output.append(text)
                    sys.__stdout__.write(text)

                def flush(self):
                    pass

                def get_output(self):
                    return "".join(self.output)

            output_capture = OutputCapture()
            sys.stdout = output_capture

            # Mock input and run CLI
            def mock_input(prompt):
                self.log(f"Prompt: {prompt}")
                if prompt in responses:
                    response = responses[prompt]
                    self.log(f"Response: {response}")
                    return response
                return ""

            with patch("builtins.input", side_effect=mock_input):
                # Use -test flag to use test mode
                sys.argv = [sys.argv[0], "-test"]
                cli_module.main()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Ensure the script exits after submission
            self.log("\n🎉 Test submission completed successfully!")
            sys.exit(0)

        except Exception as e:
            self.log(f"Error in test submission: {e}")
            traceback.print_exc()
            sys.exit(1)
        finally:
            # Cleanup
            if "test_csv" in locals() and os.path.exists(test_csv):
                os.remove(test_csv)
            self.log("Test files cleaned up")


def main():
    tester = CaltechDataTester()
    tester.run_test_submission()


if __name__ == "__main__":
    main()
