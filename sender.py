import os
import subprocess

VM_NAME = "REMnux"
FILE_TO_ANALYZE = "C:\\Downloads\\TLauncher-Installer-1.5.2.exe"
VM_PATH = "D:\\ISOfiles\\remnux-v7-focal-virtualbox.ova"

# Start the Virtual Machine
def start_vm():
    subprocess.run(["VBoxManage", "startvm", VM_NAME, "--type", "headless"])

# Transfer file to the Virtual Machine using shared folder or guest control
def copy_file_to_vm():
    subprocess.run(["VBoxManage", "guestcontrol", VM_NAME, "copyto",
                    FILE_TO_ANALYZE, VM_PATH,
                    "--username", "vm_username", "--password", "vm_password"])

# Execute the file inside the VM
def execute_file_in_vm():
    subprocess.run(["VBoxManage", "guestcontrol", VM_NAME, "run",
                    "--exe", VM_PATH,
                    "--username", "vm_username", "--password", "vm_password"])

# Restore VM to clean snapshot after analysis
def revert_vm_snapshot():
    subprocess.run(["VBoxManage", "snapshot", VM_NAME, "restore", "Snapshot_Name"])

if __name__ == "__main__":
    start_vm()
    # copy_file_to_vm()
    # execute_file_in_vm()
    # Add your logic here to analyze the file, wait for some time, etc.
    #revert_vm_snapshot()
