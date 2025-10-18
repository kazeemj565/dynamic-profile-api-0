# Dynamic Profile API (Python / Django)

Small REST API that returns profile info + a dynamic cat fact from https://catfact.ninja/fact.

## Endpoint
GET `/me` -> returns JSON:
```json
{
  "status": "success",
  "user": { "email": "...", "name": "...", "stack": "..." },
  "timestamp": "2025-10-17T12:34:56.789Z",
  "fact": "Cats sleep for 70% of their lives."
}
