import subprocess

STUDENT_ID = "66070216"

def showrun():
    command = ['ansible-playbook', '-i', 'hosts', '-e', f'student_id={STUDENT_ID}', 'playbook.yaml']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if 'failed=0' in result.stdout:
            print("Ansible playbook ran successfully.")
            return "ok"
        else:
            print("Ansible playbook failed.")
            print(result.stderr)
            return "Error: Ansible"
            
    except subprocess.CalledProcessError as e:
        print("Error running ansible-playbook command.")
        print(e.stderr)
        return "Error: Ansible"