# Simplifi Agent API Integration Guide

This guide details how to integrate the frontend with the Simplifi Agent backend services. The backend exposes two primary endpoints using **FastAPI**: one for streaming chat interactions and another for finalizing job creation.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication & Context
All endpoints require specific headers to identify the user session and the target VMS program.

| Header       | Type   | Description                                           |
| :---         | :---   | :---                                                  |
| `token`      | String | The **Bearer Token** (JWT) for the VMS API.           |
| `programId`  | String | The UUID of the Program context (e.g., `388d5...`).   |

---

## 1. Chat Endpoint
**POSt** `/chat`

Handles the natural language interaction with the Agent. This endpoint uses **Server-Sent Events (SSE)** to stream the response, providing real-time feedback (status updates) and the final result.

### Request Headers
- `Content-Type`: `application/json`
- `token`: `<BEARER_TOKEN>`
- `programId`: `<PROGRAM_ID>`

### Request Body
```json
{
  "message": "I want to create a Java Developer job",
  "userId": "user-session-123"
}
```

### Response Format (Streaming)
The response is a stream of text chunks. You must read the stream to process multiple events. Events are separated by `\n\n`.

**Event Types:**
1.  **Status Update** (`status: ...`): Indicates what the agent is currently doing (tool usage).
2.  **Result** (`result: ...`): The final text response from the AI.
3.  **Error** (`error: ...`): If something goes wrong during execution.

**Example Stream Output:**
```
status: Finding Job Managers...

status: Memorizing fields...

result: I have found a Java Developer template. What are the bill rates?
```

### Frontend Implementation Example (JavaScript)
```javascript
async function sendMessage(text) {
    const response = await fetch('http://13.60.157.40:8000/api/v1/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'token': config.token,
            'programId': config.programId
        },
        body: JSON.stringify({
            message: text,
            userId: config.userId
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
            if (line.startsWith('status:')) {
                showLoading(line.substring(7)); // e.g. "Finding Job Managers..."
            } else if (line.startsWith('result:')) {
                showResponse(line.substring(7)); // The actual AI reply
            }
        }
    }
}
```

---

## 2. Job Creation Endpoint
**POST** `/jobs/create`

Finalizes the job creation process. This endpoint should be called **only** after the Agent has collected all necessary information and the user clicks the "Create Vacancy Now" button.

### Request Headers
- `Content-Type`: `application/json`
- `token`: `<BEARER_TOKEN>`
- `programId`: `<PROGRAM_ID>`

### Request Body
```json
{
  "userId": "user-session-123"
}
```
*Note: The backend retrieves the actual job details (Draft) from its internal memory using the `userId`.*

### Response (Success 200 OK)
```json
{
  "message": "Job created successfully",
  "vms_response": {
      "job_id": "job-1001",
      "status": "created",
      ...
  }
}
```

### Response (Error)
-   **404 Not Found**: If no job draft exists for the user (session expired or flow not completed).
-   **400 Bad Request**: If `userId` is missing.
-   **500 Internal Server Error**: If the VMS API call fails.

### Frontend Implementation Example
```javascript
async function createJob() {
    const response = await fetch('http://13.60.157.40:8000/api/v1/jobs/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'token': config.token,
            'programId': config.programId
        },
        body: JSON.stringify({
            userId: config.userId
        })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Job Created! ID: " + data.vms_response.id);
    } else {
        alert("Error: " + data.detail);
    }
}
```

## Special UI Triggers
The `/chat` endpoint may return a special hidden JSON block in the `result` stream to trigger UI actions.

**Trigger:** `show_completion_buttons`
When the agent finishes collecting data, it appends:
```json
{
  "ui_action": "show_completion_buttons",
  "draft_data": {
      "job_title": "Java Dev",
      "start_date": "2024-01-01",
      ...
  }
}
```
**Frontend Action:**
Parse this JSON and display the "Create Vacancy Now" button card instead of raw text.
