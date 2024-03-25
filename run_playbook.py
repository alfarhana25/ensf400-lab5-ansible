# File Name: run_playbook.py
# Assignment: 2
# Completed by: Al Farhana Siddique
# Submission Date: March 24, 2024
import ansible_runner  # Import the ansible_runner module to run Ansible playbooks
import urllib.request  # Import urllib.request for making HTTP requests

# Open and read the SSH private key for authentication
with open("./secrets/id_rsa", "r") as file:
    ssh_key_contents = file.read()

# Execute an Ansible playbook, specifying the necessary parameters
playbook_execution_result = ansible_runner.run(
    private_data_dir=".",  # Directory where Ansible Runner will look for files
    playbook='./hello.yml',  # The playbook file to execute
    inventory='./hosts.yml',  # The inventory file to use
    ssh_key=ssh_key_contents  # SSH private key for authentication
)

# Loop to make multiple HTTP requests
for _ in range(6):  # Use underscore as variable name for unused loop counter
    # Perform an HTTP GET request to the specified URL
    http_response = urllib.request.urlopen("http://0.0.0.0")
    # Decode the response content to a string using UTF-8 encoding
    response_message = http_response.read().decode("utf-8")
    # Print the decoded response content
    print(response_message)
