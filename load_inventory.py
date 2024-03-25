#! /usr/bin/env python3
# Completed by: Al Farhana Siddique
# Submission Date: March 24, 2024

import ansible_runner  # Import the ansible_runner module to interact with Ansible directly from Python
import re  # Import the re module for regex operations

# List the inventory details from the specified file, capturing the response and any error
inventory_details, inventory_error = ansible_runner.interface.get_inventory(
    action='list',
    inventories=['./hosts.yml'],  # Specify the inventory file
    response_format='json',  # Request the response in JSON format for easy parsing
    quiet=True  # Reduce verbosity
)

# Execute the Ansible playbook to find IP addresses, capturing the response, any error, and the exit code
playbook_response, playbook_error, exit_code = ansible_runner.interface.run_command(
    "ansible-playbook", [
        "-i", "./hosts.yml",  # Specify the inventory file
        "--private-key", "./secrets/id_rsa",  # Path to the private key for SSH authentication
        "./find_ip_playbook.yml"  # Playbook to execute
    ],
    quiet=True  # Reduce verbosity
)

# Check if the playbook execution was unsuccessful
if exit_code != 0:
    print("Error running the playbook")
    print(playbook_error)
    exit(1)  # Exit the script indicating an error

# Define a regular expression pattern to match IP addresses
ip_regex_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
# Find all matches of the IP address pattern in the playbook response
ip_addresses = re.findall(ip_regex_pattern, playbook_response)

# Initialize a counter for iterating through IP addresses
counter = 0
# Iterate over each host defined in the inventory details
for host in inventory_details["_meta"]["hostvars"]:
    # Output the host details including IP address and group membership
    print(f"Host: {host}")
    print(f"IP: {ip_addresses[counter]}")  # Use the counter to index the correct IP address
    # Determine the group of the host dynamically
    group = 'loadbalancer' if host == 'localhost' else 'app_group'
    print(f"Group: {group}")
    print()  # Print a newline for better readability
    counter += 1  # Increment the counter to move to the next IP address

# Finally, perform a connectivity test (ping) on all hosts including localhost
ansible_runner.interface.run_command(
    "ansible", [
        "-i", "./hosts.yml",  # Specify the inventory file
        "--private-key", "./secrets/id_rsa",  # Path to the private key
        "all:localhost",  # Target all hosts including localhost
        "-m", "ping"  # Use the ping module to test connectivity
    ]
)
