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

for line in output_lines:
    key, value = line.split(' = ')
    if key == "ec2_instance_id":
        ec2_instance_id = value
    elif key == "ec2_instance_public_ip":
        ec2_instance_public_ip = value

# Email configuration
sender_email = "your_email@gmail.com"
subject = "EC2 Instance Information"
body = f"""
Hi,

The EC2 instance information is as follows:

EC2 Instance ID: {ec2_instance_id}
EC2 Instance Public IP: {ec2_instance_public_ip}

Attached to this email is a file.

Best Regards,
Your Name
"""

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Gmail SMTP port

# Your email credentials
username = "your_email@gmail.com"
password = "your_password"

# Recipient email address
recipient_email = "recipient@example.com"

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Attachment configuration
attachment_path = "path_to_your_attachment.pdf"
attachment_filename = "attachment.pdf"
with open(attachment_path, "rb") as attachment:
    pdf_part = MIMEApplication(attachment.read(), _subtype="pdf")
    pdf_part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
    message.attach(pdf_part)

# Connect to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Enable TLS encryption

try:
    server.login(username, password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print("An error occurred:", str(e))
finally:
    server.quit()
