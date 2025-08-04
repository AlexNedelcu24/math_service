# 🧮 MathService API

**MathService** is an asynchronous API built with FastAPI for executing mathematical computations like **factorials**, **Fibonacci numbers**, and **exponentiation**. Jobs are processed asynchronously using a background worker and stored in a SQLite database.

---

## 🚀 Features

- 📥 Submit mathematical jobs (`fib`, `fact`, `pow`) via HTTP POST
- 📤 Retrieve results based on operation + input
- 🧵 Background worker queue powered by `asyncio`
- ✅ Token-based security (via Bearer token)
- 🐳 Full Docker support (`Dockerfile` + `docker-compose`)
- 📄 SQLite database integration via `databases` and SQLAlchemy Core
- 📂 Persistent logging to `logs.txt`
- 📊 Prometheus metrics exposed at `/metrics`
- 🧪 Unit tests included

---

## 🗂️ Project Structure

```
├── app/
│   ├── controllers/       # API routes (FastAPI)
│   ├── database/          # DB engine and table definition
│   ├── entities/          # Computation entity model
│   ├── repositories/      # DB access layer
│   ├── schemas/           # Pydantic models for request/response
│   ├── services/          # Business logic (MathService)
│   ├── utils/             # Token auth, logging utils
│   └── workers/           # Asynchronous task worker
│
├── config/                # App settings
├── docker/                # Dockerfile & docker-compose config
├── tests/                 # Unit tests for business logic
│
├── main.py                # Application entrypoint
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└──  logs.txt               # Runtime logs (job results/errors)
```




---

## 📦 Endpoints Overview

| Method | Endpoint             | Description                             |
|--------|----------------------|-----------------------------------------|
| POST   | `/api/compute`       | Submit a Fibonacci or Factorial job     |
| POST   | `/api/compute/pow`   | Submit a power (exponentiation) job     |
| GET    | `/api/results/{op}/{input}` | Fetch the result of a computation |

🛡️ All endpoints require:
```http
Authorization: Bearer token123
```

---

### 📤 POST `/api/compute`

Used for submitting a **Fibonacci** or **Factorial** job.

**Request body:**
```json
{
  "operation": "fib",   // or "fact"
  "value": 10
}
```

**Example values:**
- `"operation": "fib"` → Fibonacci of 10
- `"operation": "fact"` → Factorial of 10

---

### 📤 POST `/api/compute/pow`

Used for submitting an **exponentiation** job.

**Request body:**
```json
{
  "base": 2,
  "exponent": 5
}
```

This computes `2^5 = 32`.

---

### 📥 GET `/api/results/{operation}/{input_value}`

Used to fetch the result of a previously submitted job.  
- `operation` can be `"fib"`, `"fact"`, or `"pow"`
- `input_value` must match the input format used earlier:
  - `"10"` for fib/fact
  - `"2^5"` for pow

**Example:**
```
GET /api/results/fib/10
GET /api/results/pow/2^5
```
```http
Authorization: Bearer token123
```

---

