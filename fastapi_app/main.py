from fastapi import FastAPI, Request
import boto3
import os

app = FastAPI()

@app.post("/receive")
async def receive_message(request: Request):
    body = await request.json()
    connection_id = body.get("connectionId")
    message = body.get("message")

    if not connection_id or not message:
        return {"status": "Missing connectionId or message"}

    # Send message back to client via API Gateway Management API
    domain_name = os.environ.get("APIGW_DOMAIN")
    stage = os.environ.get("APIGW_STAGE")
    endpoint_url = f"https://{domain_name}/{stage}"

    apigw_client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

    try:
        apigw_client.post_to_connection(
            Data=f"Echo: {message}".encode("utf-8"),
            ConnectionId=connection_id
        )
    except Exception as e:
        return {"status": f"Failed to send message: {str(e)}"}

    return {"status": "Message sent"}