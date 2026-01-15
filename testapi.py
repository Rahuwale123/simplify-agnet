import requests
import json

def test_chat():
    url = "http://13.60.157.40:8000/api/v1/chat"
    
    # You can provide the token here that you want the tool to use
    headers = {
        "token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMTl81cm1HcHNlUHpOemQ3YzlON0tGbHhYUWlCVE0xdlkzUHpIUlBVLUk0In0.eyJleHAiOjE3NjgyNjg5MDEsImlhdCI6MTc2ODIzMjkwMSwianRpIjoiNmFjM2JjMjMtN2U0OS00MmNiLTk3ZTktNThlZGRlODVjNmQ3IiwiaXNzIjoiaHR0cHM6Ly92NC1ub25wcm9kLWF1dGguc2ltcGxpZnlzYW5kYm94Lm5ldC9yZWFsbXMvcWEtaGVhbHRoY2FyZSIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiJlNDc5NWM0Ni1kMDUxLTQxYWItYjNjYS1hNGE0YWUzNDg0ZDAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzaW1wbGlmeS1hdXRoLXNlcnZpY2UiLCJzaWQiOiJhMTJlYmFhMS0wYjMwLTQ3ODUtOTI1NS1kMmUzZDUwN2UwNGQiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFhLWhlYWx0aGNhcmUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbImltcGVyc29uYXRpb24iLCJ2aWV3LXVzZXJzIiwicXVlcnktZ3JvdXBzIiwicXVlcnktdXNlcnMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoic2ltcGxpZnktYXV0aCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInByZWZlcnJlcl91c2VybmFtZSI6ImFkbWluIiwiY2xpZW50X3R5cGUiOiJpbnRlcm5hbCIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwidXNlclR5cGUiOiJzdXBlcl91c2VyIn0.AWTrklFwrN3FvEUlJWxdTbm_xpHwKL5laJndPyZ-TrebR6uoH351IQAx2QJbwGsWqe5IXgFDugiH7zq7fvm6VVmJgNxWEkpvRB7pr_Y7DP_NDMK68UTrUaULYNTSc3fyXZSy0I9GzRbRx0kcJLigscO0sPFIJhguoNWuCrSlswNfZtTFmxCkSfnjaVEhgDi8eTbsTCsmlmHWXJI8etR2GXdaS39tj5ZsdxGovXJPuM1fMbdktTg1i-G__1-0C18rKmfb3NGHGz-0iEnzy51oPWZnk4WpPLSHVyTKJUWmc3h-tGfNjy_hj5WW90Bp57IFzwNqpvu_s3DhG9AqmSsazA",
        "programId": "20da23d5-83cb-4dc1-aa4f-9f79840ad966",
        "Content-Type": "application/json"
    }
    
    data = {
        "message": "Please get the job templates for hierarchy ID 11be6d7f-22ea-4a7b-9409-8f77501138b9",
        "userId": "user-456"
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response Content:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_chat()
