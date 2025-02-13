import json
import http.client
import os

OPENAI_API_KEY = "xdxdxdxd"

def generate_listing_description(listing_data):
    prompt = f"Write a detailed real estate listing based on this data:\n{json.dumps(listing_data, indent=2)}"

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a real estate listing writer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    })

    conn = http.client.HTTPSConnection("api.openai.com")
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    conn.request("POST", "/v1/chat/completions", body=payload, headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()

    response_json = json.loads(data)
    
    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Error: {response_json.get('error', 'Unknown error')}"

def lambda_handler(event, context):
    try:
        if "body" in event:
            listing_data = json.loads(event["body"]) 
        else:
            listing_data = event

        description = generate_listing_description(listing_data)

        return {
            "statusCode": 200,
            "body": json.dumps({"description": description})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
