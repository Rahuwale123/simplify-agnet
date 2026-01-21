# Simi AI API Documentation

Base URL: `https://13-60-157-40.nip.io` (Local)

## 1. Chat Endpoint (`/chat`)
Executes the agent logic with the user's message. Returns a streaming response (Server-Sent Events).

**Method:** `POST`
**URL:** `/api/v1/chat`

**Headers:**
- `Content-Type`: `application/json`
- `token`: `<auth_token>`
- `programId`: `<program_id>`

**Request Body:**
```json
{
  "message": "I need to hire a Java Developer",
  "userId": "user-6",
  "sessionId": "session-uuid-123"
}
```

**cURL Command:**
```bash
curl -X POST https://13-60-157-40.nip.io/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "token: YOUR_TOKEN" \
  -H "programId: YOUR_PROGRAM_ID" \
  -d '{
    "message": "I need to hire a Java Developer",
    "userId": "user-6",
    "sessionId": "session-uuid-123"
  }'
```

**Response (Stream):**
```text
status: Thinking...

status: Saving job title...

result: I have saved the job title as Java Developer. What is the start date?
```

---

## 2. Start New Session (`/start-chat`)
Creates a new chat session for a user.

**Method:** `POST`
**URL:** `/api/v1/start-chat`

**Request Body:**
```json
{
  "user_id": "user-6"
}
```

**cURL Command:**
```bash
curl -X POST https://13-60-157-40.nip.io/api/v1/start-chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-6"
  }'
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 3. Get User Sessions (`/sessions/{user_id}`)
Retrieves a list of all active sessions for a user.

**Method:** `GET`
**URL:** `/api/v1/sessions/{user_id}`

**cURL Command:**
```bash
curl -X GET https://13-60-157-40.nip.io/api/v1/sessions/user-6
```

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2023-10-27T10:00:00.000Z",
      "title": "I need to hire a Java Developer"
    },
    {
      "session_id": "another-session-uuid",
      "created_at": "2023-10-26T14:30:00.000Z",
      "title": "Hi, how are you?"
    }
  ]
}
```

---

## 4. Get Session History (`/history/{session_id}`)
Retrieves the full chat history for a session, formatted as User/AI pairs.

**Method:** `GET`
**URL:** `/api/v1/history/{session_id}`

**cURL Command:**
```bash
curl -X GET https://13-60-157-40.nip.io/api/v1/history/session-uuid-123
```

**Response:**
```json
{
  "session_id": "session-uuid-123",
  "messages": [
    {
      "user": "Hi",
      "ai": "Hello! How can I help you today?"
    },
    {
      "user": "I need a developer",
      "ai": "Sure, I can help with that. What is the job title?"
    }
  ]
}
```

---

## 5. Delete Session (`/sessions/{session_id}`)
Deletes a specific session and its history.

**Method:** `DELETE`
**URL:** `/api/v1/sessions/{session_id}`

**cURL Command:**
```bash
curl -X DELETE https://13-60-157-40.nip.io/api/v1/sessions/session-uuid-123
```

**Response:**
```json
{
  "status": "success",
  "message": "Session session-uuid-123 deleted"
}
```

---

## 6. Reset Session (`/reset`)
Clears the current history and draft state for a user (Legacy/Dev endpoint).

**Method:** `POST`
**URL:** `/api/v1/reset`

**Request Body:**
```json
{
  "userId": "user-6"
}
```

**cURL Command:**
```bash
curl -X POST https://13-60-157-40.nip.io/api/v1/reset \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user-6"
  }'
```

**Response:**
```json
{
  "message": "Session reset successfully. Memory and drafts cleared."
}
```
