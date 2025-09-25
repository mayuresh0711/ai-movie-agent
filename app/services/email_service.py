import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

# Configure Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_email(to_email: str, subject: str, body: str):
    if not SENDER_EMAIL or not BREVO_API_KEY:
        return {"error": "Sender email or Brevo API key not configured."}

    sender = sib_api_v3_sdk.SendSmtpEmailSender(email=SENDER_EMAIL, name="AI Movie Recommender")
    to = [sib_api_v3_sdk.SendSmtpEmailTo(email=to_email)]
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        text_content=body
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Brevo API Response: {api_response}")
        return {"message": "Email sent successfully via Brevo!"}
    except ApiException as e:
        print(f"Failed to send email via Brevo: {e}")
        return {"error": f"Failed to send email via Brevo: {e}"}