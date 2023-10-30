#email
import subprocess

# Run 'terraform output' and capture the output
try:
    output = subprocess.check_output('terraform output', shell=True, stderr=subprocess.STDOUT, text=True)
except subprocess.CalledProcessError as e:
    print("Error running 'terraform output':", e)
    exit(1)

# Split the output into lines and parse the values
output_lines = output.strip().split('\n')
ec2_instance_id = None
ec2_instance_public_ip = None

for line in output_lines:
    key, value = line.split(' = ')
    if key == "ec2_instance_id":
        ec2_instance_id = value
    elif key == "ec2_instance_public_ip":
        ec2_instance_public_ip = value

# Print the values
print("EC2 Instance ID:", ec2_instance_id)
print("EC2 Instance Public IP:", ec2_instance_public_ip)
