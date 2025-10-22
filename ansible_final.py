import subprocess
import shutil

def run_show_command():
    print("---!!! กำลังรันโค้ด ANSBILE FINAL เวอร์ชันใหม่ !!!---")
    """
    Executes an Ansible playbook with a robust method to find the executable
    and provide detailed error feedback.
    """
    playbook_path = 'interface_playbook.yaml'
    
    # Step 1: Find the full path to the 'ansible-playbook' executable.
    # This avoids PATH issues when running from a script.
    ansible_executable = shutil.which('ansible-playbook')
    
    if not ansible_executable:
        error_msg = "Error: 'ansible-playbook' command not found in system PATH."
        print(error_msg)
        return error_msg

    command_args = [ansible_executable, playbook_path]
    
    try:
        # Step 2: Run the command with improved error checking.
        # 'check=True' will raise an exception if the command fails (returns non-zero).
        process = subprocess.run(
            command_args, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=90  # A generous timeout
        )
        
        # Step 3: Use a reliable check for success from Ansible's output.
        if 'failed=0' in process.stdout:
            print("Ansible playbook executed successfully.")
            return 'ok'
        else:
            error_msg = f"Ansible ran but reported an issue. Full output:\n{process.stdout}"
            print(error_msg)
            return error_msg
            
    except subprocess.CalledProcessError as e:
        # This is key: If the command fails, we now print the detailed error.
        error_output = (f"FATAL: Ansible command failed with return code {e.returncode}.\n"
                        f"--- STDOUT ---\n{e.stdout}\n"
                        f"--- STDERR (Errors are often here) ---\n{e.stderr}")
        print(error_output)
        return 'Error: Ansible execution failed. Check terminal for detailed logs.'
        
    except Exception as e:
        # Catch any other unexpected Python errors.
        print(f"An unexpected Python error occurred: {e}")
        return f"An unexpected Python error occurred: {e}"