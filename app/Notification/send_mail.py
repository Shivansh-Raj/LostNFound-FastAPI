import aiosmtplib
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 465  
SENDER_EMAIL = "abcraj12356@gmail.com"  
SENDER_PASSWORD = "dxudxmcclszkufre"  

async def send_email(subject: str, body: str, recipient_email: str):
    try:
        validate_email(recipient_email)
        message = MIMEText(body, "plain")
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject

        async with aiosmtplib.SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=True) as server:
            # await server.starttls()
            await server.login(SENDER_EMAIL, SENDER_PASSWORD)
            await server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())

            print(f"Email sent to {recipient_email}")
    
    except EmailNotValidError as e:
        print(f"Invalid email address: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")
