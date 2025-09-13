import boto3
import os
from urllib.parse import unquote_plus
from PIL import Image
import json # We need the json library to open the "envelope"
import uuid

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

DEST_BUCKET = os.environ['DESTINATION_BUCKET']
RESULTS_TABLE = os.environ['RESULTS_TABLE']
table = dynamodb.Table(RESULTS_TABLE)

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)

def handler(event, context):
    # This outer loop is for the SQS message "envelope"
    for sqs_record in event['Records']:
        # The S3 event "letter" is a string in the 'body', so we parse it
        s3_event_body = json.loads(sqs_record['body'])
        
        # Now we can loop through the S3 records just like before
        for s3_record in s3_event_body['Records']:
            bucket_name = s3_record['s3']['bucket']['name']
            key = unquote_plus(s3_record['s3']['object']['key'])
            
            # Recursion-avoidance: skip if the object is already in the destination bucket
            dest_bucket_name = DEST_BUCKET
            if bucket_name == dest_bucket_name:
                # skip processing objects that originate from the destination bucket
                continue

            tmpkey = key.replace('/', '')
            download_path = f'/tmp/{tmpkey}'
            upload_path = f'/tmp/resized-{tmpkey}'
            
            s3_client.download_file(bucket_name, key, download_path)
            
            #call rekognition

            response = rekognition_client.detect_labels(
                Image ={'S3Object':{'Bucket': bucket_name, 'Name': key}},
                MaxLabels=10,
                MinConfidence=90
            )

            labels = [label['Name'] for label in response['Labels']]
            
            #store in DB
            image_id = str(uuid.uuid4())
            table.put_item(
               Item={
                    'ImageId': image_id,
                    'S3Key': key,
                    'Bucket': bucket_name,
                    'Labels': labels
               }
           )

            resize_image(download_path, upload_path)
            
            dest_key = f"thumbnails/{key}"
            
            s3_client.upload_file(upload_path, dest_bucket_name, dest_key)

    return { 'statusCode': 200, 'body': 'Image processed!' }

