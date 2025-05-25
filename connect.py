import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    table.put_item(Item={'connectionId': connection_id})
    return {'statusCode': 200}