import boto3
import os
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    api_gateway_management_api = boto3.client('apigatewaymanagementapi',
        endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}")

    try:
        connections = table.scan()['Items']
        for connection in connections:
            connection_id = connection['connectionId']
            try:
                api_gateway_management_api.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps({'message': 'Hello from Lambda'})
                )
            except ClientError as e:
                if e.response['Error']['Code'] == 'GoneException':
                    table.delete_item(Key={'connectionId': connection_id})
    except Exception as e:
        print(f"Error: {e}")

    return {'statusCode': 200}