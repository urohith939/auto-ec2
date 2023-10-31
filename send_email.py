#email
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication

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
ssh_key_file_name = None 

for line in output_lines:
    key, value = line.split(' = ')
    if key == "ec2_instance_id":
        ec2_instance_id = value
    elif key == "ec2_instance_public_ip":
        ec2_instance_public_ip = value
    elif key == "ssh_key_file_name":
        ssh_key_file_name = value.strip('"\'')

sender_email = "urohithnarasimha.1si19ec111@gmail.com"
subject = "Instance detail"
body = f"""Hi Team,
Regarding instance detail:
EC2 instance id is {ec2_instance_id}
EC2 public IP is {ec2_instance_public_ip}
Thank you"""
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Gmail SMTP port
username = "urohithnarasimha.1si19ec111@gmail.com"
password = "sahhndrskgzkzbir"

recipient_list = ["urohithnarasimha@gmail.com", "rohithnarasimha2001@gmail.com"]

for receiver_email in recipient_list:
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    # Attach the .pem file from the same directory
    attachment = open(ssh_key_file_name, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{ssh_key_file_name}"')
    message.attach(part)
    
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption
    
    try:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully! to",receiver_email)
    except Exception as e:
        print("An error occurred: ", str(e))
    finally:
        server.quit()
