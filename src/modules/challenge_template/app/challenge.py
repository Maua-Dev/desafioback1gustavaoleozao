import os

from botocore.exceptions import PartialCredentialsError, NoCredentialsError

import boto3

def lambda_handler(event, context):


    try:

        s3_client = boto3.client('s3', region_name=os.environ.get("AWS_REGION"))
        ses_client = boto3.client('ses', region_name=os.environ.get("AWS_REGION"))

        s3_bucket_name = 'challenge-storage-devcommunitymaua'

        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)

        latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
        latest_file_key = latest_file['Key']

        file_response = s3_client.get_object(Bucket=s3_bucket_name, Key=latest_file_key)
        file_content = file_response['Body'].read().decode('utf-8')

        ses_client.send_email(
            Source='lseixas.iorio@gmail.com',
            Destination={
                'ToAddresses': ['lseixas.iorio@gmail.com'],
            },
            Message={
                'Subject': {
                    'Data': "subject",
                },
                'Body': {
                    'Text': {
                        'Data': f"Content of the latest file ({latest_file_key}):\n\n{file_content}",
                    },
                },
            }
        )

        return {
            "statusCode": 200,
            "body": f"Email sent successfully with content of file: {latest_file_key}"
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

