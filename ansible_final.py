import subprocess

STUDENT_ID = "66070216"


def showrun():
    playbook_file = 'showrun_playbook.yaml'
    command = ['ansible-playbook', '-e', f'student_id={STUDENT_ID}', playbook_file]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, stdin=subprocess.PIPE)
        output = result.stdout
        
        if 'failed=0' in output and 'unreachable=0' in output:
            print("Ansible playbook ran successfully.")
            return 'ok'
        else:
            print(f"Ansible playbook failed. Error: {result.stderr}")
            return 'Error: Ansible'
            
    except subprocess.CalledProcessError as e:
        print(f"Error executing ansible-playbook. Stderr: {e.stderr}")
        return 'Error: Ansible'