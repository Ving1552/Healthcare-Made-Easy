import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Email configuration
    sender_email = "recefakecbp@gmail.com"  # Replace with your Gmail address
    sender_password = ' 12'   # Replace with your Gmail password
    recipient_email = "recefakecbp@gmail.com"
    subject = "Symptoms Check"

    # List of data for the email body
    data_list = ["Symptom 1: ...", "Symptom 2: ...", "Symptom 3: ..."]

    # Compose the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add body text
    body = "\n".join(data_list)
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Enable TLS
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

if __name__ == "__main__":
    send_email()
