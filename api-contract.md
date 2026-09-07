# KiranaBot API Contract

Base path:

```text
/api/v1
```

## 1. General Conventions

Protected endpoints require:

```http
Authorization: Bearer <JWT>
```

The authenticated user identity is derived from the token. Protected requests should not accept `user_id` from the client.

Standard error format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

Common status codes: `200`, `201`, `202`, `400`, `401`, `403`, `404`, `409`, `413`, `415`, `422`, `500`, `503`.

---

## 2. User / Auth APIs

### POST `/api/v1/user/signup`

Request:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

Success: `201 Created`

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-09-05T12:00:00Z"
}
```

Errors: `400 INVALID_REQUEST`, `409 USER_ALREADY_EXISTS`, `422 VALIDATION_ERROR`, `500 INTERNAL_ERROR`.

### POST `/api/v1/user/signin`

Request:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

Success: `200 OK`

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Errors: `400 INVALID_REQUEST`, `401 INVALID_CREDENTIALS`, `422 VALIDATION_ERROR`, `500 INTERNAL_ERROR`.

### POST `/api/v1/user/logout`

Authentication required.

Success: `200 OK`

```json
{
  "message": "Logged out successfully"
}
```

Errors: `401 UNAUTHORIZED`, `500 INTERNAL_ERROR`.

### GET `/api/v1/user/`

Returns the current authenticated user.

Success: `200 OK`

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-09-05T12:00:00Z",
  "updated_at": "2026-09-05T12:00:00Z"
}
```

Errors: `401 UNAUTHORIZED`, `404 USER_NOT_FOUND`, `500 INTERNAL_ERROR`.

---

## 3. Invoice APIs

### POST `/api/v1/invoices`

Uploads an invoice and starts asynchronous processing.

Authentication required.

Request type:

```http
Content-Type: multipart/form-data
```

Form field:

```text
file=<invoice file>
```

Server flow:

1. Authenticate user.
2. Run preflight checks.
3. Validate file size/type.
4. Calculate file hash.
5. Check duplicate.
6. Create Invoice.
7. Create Job.
8. Commit transaction.
9. Enqueue background processing.
10. Return without waiting for OCR/validation.

Success: `202 Accepted`

```json
{
  "id": "invoice-uuid",
  "filename": "invoice.pdf",
  "status": "Queued",
  "job_id": "job-uuid",
  "created_at": "2026-09-05T12:00:00Z"
}
```

Errors: `401 UNAUTHORIZED`, `409 DUPLICATE_INVOICE`, `413 FILE_TOO_LARGE`, `415 UNSUPPORTED_MEDIA_TYPE`, `422 VALIDATION_ERROR`, `500 INTERNAL_ERROR`, `503 QUEUE_UNAVAILABLE`.

### GET `/api/v1/invoices`

Returns invoices owned by the authenticated user.

Success: `200 OK`

```json
{
  "items": [
    {
      "id": "invoice-uuid",
      "filename": "invoice.pdf",
      "status": "Completed",
      "created_at": "2026-09-05T12:00:00Z"
    }
  ]
}
```

Future query parameters may include `page`, `page_size`, `status`, and `sort`.

### GET `/api/v1/invoices/{invoice_id}`

Returns one invoice owned by the authenticated user.

Authorization rule:

```text
invoice.user_id == authenticated_user.id
```

Success: `200 OK`

```json
{
  "id": "invoice-uuid",
  "filename": "invoice.pdf",
  "status": "Completed",
  "invoice_file_link": "file-location",
  "ocr_result": {},
  "validation_results": {},
  "job": {
    "job_id": "job-uuid",
    "status": "Completed",
    "retry_count": 0,
    "error_message": null,
    "started_at": "2026-09-05T12:01:00Z",
    "completed_at": "2026-09-05T12:02:00Z"
  },
  "created_at": "2026-09-05T12:00:00Z",
  "updated_at": "2026-09-05T12:02:00Z"
}
```

Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 INVOICE_NOT_FOUND`, `422 INVALID_INVOICE_ID`, `500 INTERNAL_ERROR`.

---

## 4. Job APIs

### GET `/api/v1/jobs`

Returns jobs visible to the authenticated user.

Optional filters:

```text
?invoice_id=<uuid>
?worker_id=<worker-id>
?status=<status>
```

Success: `200 OK`

```json
{
  "items": [
    {
      "job_id": "job-uuid",
      "invoice_id": "invoice-uuid",
      "status": "Processing",
      "retry_count": 0,
      "worker_id": "worker-1",
      "error_message": null,
      "started_at": "2026-09-05T12:01:00Z",
      "completed_at": null,
      "created_at": "2026-09-05T12:00:00Z",
      "updated_at": "2026-09-05T12:01:00Z"
    }
  ]
}
```

Errors: `401 UNAUTHORIZED`, `422 INVALID_FILTER`, `500 INTERNAL_ERROR`.

### GET `/api/v1/jobs/{job_id}`

Returns one job.

Success: `200 OK`

Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 JOB_NOT_FOUND`, `422 INVALID_JOB_ID`, `500 INTERNAL_ERROR`.

---

## 5. Conversation APIs

### POST `/api/v1/conversations`

Creates a conversation for the authenticated user.

Success: `201 Created`

```json
{
  "id": "conversation-uuid",
  "created_at": "2026-09-05T12:00:00Z",
  "updated_at": "2026-09-05T12:00:00Z"
}
```

### GET `/api/v1/conversations`

Returns conversations belonging to the authenticated user.

Success: `200 OK`

```json
{
  "items": [
    {
      "id": "conversation-uuid",
      "created_at": "2026-09-05T12:00:00Z",
      "updated_at": "2026-09-05T12:00:00Z"
    }
  ]
}
```

---

## 6. Message APIs

### POST `/api/v1/conversations/{conversation_id}/messages`

Creates a message in an owned conversation.

Request:

```json
{
  "role": "user",
  "content": "Why did this invoice fail validation?"
}
```

Success: `201 Created`

```json
{
  "id": "message-uuid",
  "conversation_id": "conversation-uuid",
  "role": "user",
  "content": "Why did this invoice fail validation?",
  "created_at": "2026-09-05T12:05:00Z"
}
```

Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 CONVERSATION_NOT_FOUND`, `422 VALIDATION_ERROR`, `500 INTERNAL_ERROR`.

### GET `/api/v1/conversations/{conversation_id}/messages`

Returns messages from an owned conversation.

Success: `200 OK`

---

## 7. RAG API

### POST `/api/v1/rag/query`

Sends a grounded query to the RAG system.

Request:

```json
{
  "conversation_id": "conversation-uuid",
  "invoice_id": "invoice-uuid",
  "query": "Why was this invoice marked invalid?"
}
```

Processing:

1. Verify conversation ownership.
2. Verify invoice ownership.
3. Load invoice/OCR/validation context.
4. Retrieve relevant knowledge.
5. Apply metadata/temporal filtering.
6. Rerank evidence.
7. Generate a grounded answer.
8. Validate LLM output.
9. Return answer, citations, and evidence.
10. Store messages where appropriate.

Success: `200 OK`

```json
{
  "status": "success",
  "answer": "The invoice failed because ...",
  "citations": [
    {
      "source_id": "source-1",
      "reference": "..."
    }
  ],
  "evidence": [
    {
      "text": "...",
      "source_id": "source-1"
    }
  ]
}
```

Insufficient evidence may still return `200 OK`:

```json
{
  "status": "insufficient_evidence",
  "answer": null,
  "citations": [],
  "evidence": []
}
```

Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 INVOICE_NOT_FOUND`, `404 CONVERSATION_NOT_FOUND`, `422 VALIDATION_ERROR`, `500 INTERNAL_ERROR`, `503 RETRIEVAL_UNAVAILABLE`.

The RAG system should not answer from unsupported model knowledge when retrieval fails.

---

## 8. OCR and Validation Errors

Do not expose separate public endpoints such as:

```text
/api/v1/invoice/ocr_error
/api/v1/invoice/validation_error
```

Represent these through invoice/job state instead.

Example:

```json
{
  "status": "OCR_FAILED",
  "error": {
    "code": "OCR_ERROR",
    "message": "OCR processing failed"
  }
}
```

or:

```json
{
  "status": "VALIDATION_FAILED",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invoice validation failed"
  }
}
```

Clients obtain these states through:

```text
GET /api/v1/invoices/{invoice_id}
GET /api/v1/jobs/{job_id}
```

---

## 9. Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/user/signup` | Sign up |
| POST | `/api/v1/user/signin` | Sign in |
| POST | `/api/v1/user/logout` | Log out |
| GET | `/api/v1/user/` | Current user |
| POST | `/api/v1/invoices` | Upload invoice |
| GET | `/api/v1/invoices` | List invoices |
| GET | `/api/v1/invoices/{invoice_id}` | Get invoice |
| GET | `/api/v1/jobs` | List/filter jobs |
| GET | `/api/v1/jobs/{job_id}` | Get job |
| POST | `/api/v1/conversations` | Create conversation |
| GET | `/api/v1/conversations` | List conversations |
| POST | `/api/v1/conversations/{conversation_id}/messages` | Create message |
| GET | `/api/v1/conversations/{conversation_id}/messages` | List messages |
| POST | `/api/v1/rag/query` | Ask grounded RAG question |

---

## 10. Planned Pydantic Schemas

```text
schemas/
├── user.py
├── invoice.py
├── job.py
├── conversation.py
├── message.py
├── rag.py
└── error.py
```

Database ORM models should not be returned directly from routes.

---

## 11. Architecture

```text
Client
  ↓
FastAPI Router / Controller
  ↓
Authentication / Authorization
  ↓
Pydantic Validation
  ↓
Service Layer
  ↓
Repository Layer
  ↓
PostgreSQL
```

Invoice upload flow:

```text
Client
  ↓
POST /api/v1/invoices
  ↓
Auth
  ↓
Preflight checks
  ↓
Duplicate check
  ↓
Invoice + Job transaction
  ↓
Queue
  ↓
202 Accepted

Background Worker
  ↓
OCR
  ↓
Validation
  ↓
Persist results
  ↓
Completed / Failed
```
