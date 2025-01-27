import os
from botocore.exceptions import PartialCredentialsError, NoCredentialsError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import boto3

def lambda_handler(event, context):


    try:

        s3_client = boto3.client('s3', region_name=os.environ.get("AWS_REGION"))
        ses_client = boto3.client('ses', region_name=os.environ.get("AWS_REGION"))

        s3_bucket_name = 'challenge-storage-devcommunitymaua'
        file_key = 'kick buttowski.png'

        file_response = s3_client.get_object(Bucket=s3_bucket_name, Key=file_key)
        file_content = file_response['Body'].read()

        sender_email = 'contato@devmaua.com'
        recipient_email = 'mcapaldo.devmaua@gmail.com'
        subject = "Desafio Hardcore"
        body_text = "Deasfio Leo e Gustavo"

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email

        message.attach(MIMEText(body_text, 'plain'))

        mime_base = MIMEBase('image', 'png')
        mime_base.set_payload(file_content)
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="{file_key}"')
        message.attach(mime_base)

        response = ses_client.send_raw_email(
            Source=sender_email,
            Destinations=[recipient_email, 'lseixas.iorio@gmail.com'],
            RawMessage={'Data': message.as_string()}
        )

        return {
            "statusCode": 200,
            "body": "Email sent successfully"
        }

    except NoCredentialsError:
        print("AWS credentials not found.")
        return {
            "statusCode": 500,
            "body": "Failed to process files or send email"
        }
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
        return {
            "statusCode": 500,
            "body": "Failed to process files or send email"
        }
    except Exception as e:
        print("Error sending email:", str(e))
        return {
            "statusCode": 500,
            "body": "Failed to process files or send email"
        }
