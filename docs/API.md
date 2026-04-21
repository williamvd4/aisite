# API Documentation

This project currently exposes server-rendered Django views rather than a formal REST API.

## AJAX endpoints

### `POST /chat/`
- Purpose: submit chat payloads for lesson generation/review workflow.
- Content type: JSON.
- Auth: session-based authenticated user.

### `POST /review-lesson/`
- Purpose: submit lesson text for AI review.
- Content type: JSON.
- Auth: session-based authenticated user.

## Notes
- Request/response contracts are currently defined in the Django view logic and frontend JavaScript interactions.
- If third-party API consumers are required, add Django REST Framework and OpenAPI schema generation in a future version.
