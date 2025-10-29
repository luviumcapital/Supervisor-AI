# API Documentation

This document describes the integration with external APIs used by the Supervisor AI system.

## Table of Contents

- [Bytez API](#bytez-api)
- [Brevo API](#brevo-api)
- [Skywork.ai API](#skyworkai-api)
- [Dolibarr API](#dolibarr-api)

---

## Bytez API

**Purpose:** File processing and bytecode analysis for invoice extraction

### Authentication

```python
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")
BYTEZ_BASE_URL = os.getenv("BYTEZ_BASE_URL", "https://api.bytez.io")
```

### Endpoints

#### Process Document

```
POST /api/v1/documents/process
```

**Request Body:**
```json
{
  "file": "binary",
  "file_type": "pdf|image",
  "extraction_type": "invoice|receipt"
}
```

**Response:**
```json
{
  "id": "doc_123456",
  "status": "processed",
  "data": {
    "vendor": "Company Name",
    "invoice_number": "INV-2025-001",
    "amount": 1500.00,
    "date": "2025-10-29",
    "items": [...]
  }
}
```

#### Get Document Status

```
GET /api/v1/documents/{document_id}/status
```

### Error Handling

```python
# Fallback to Google Gemini if Bytez fails
try:
    response = bytez_client.process_document(file)
except BytezError:
    response = gemini_client.extract_invoice(file)
```

---

## Brevo API

**Purpose:** Email sending and campaign management for notifications

### Authentication

```python
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
from brevo_python import Configuration, ApiClient, TransactionalEmailsApi

config = Configuration()
config.api_key["api-key"] = BREVO_API_KEY
```

### Endpoints

#### Send Email

```
POST /v3/smtp/email
```

**Request Body:**
```json
{
  "sender": {
    "name": "Luvium AI",
    "email": "noreply@luvium.online"
  },
  "to": [
    {
      "email": "recipient@example.com",
      "name": "Recipient Name"
    }
  ],
  "subject": "Invoice Processed",
  "htmlContent": "<p>Your invoice has been processed successfully.</p>"
}
```

**Response:**
```json
{
  "messageId": "<message_id@smtp.brevo.com>"
}
```

#### Get Campaign Reports

```
GET /v3/smtp/statistics
```

### Implementation

```python
from brevo_python import TransactionalEmailsApi, SendSmtpEmail

api_instance = TransactionalEmailsApi(ApiClient(config))

email = SendSmtpEmail(
    to=[{"email": recipient_email, "name": recipient_name}],
    sender={"name": "Luvium AI", "email": "noreply@luvium.online"},
    subject="Invoice Notification",
    html_content=email_body
)

response = api_instance.send_transactional_email(email)
```

---

## Skywork.ai API

**Purpose:** AI-powered text analysis and language processing for document comprehension

### Authentication

```python
SKYWORK_API_KEY = os.getenv("SKYWORK_API_KEY")
SKYWORK_BASE_URL = os.getenv("SKYWORK_BASE_URL", "https://api.skywork.ai")
```

### Endpoints

#### Text Analysis

```
POST /api/v1/text/analyze
```

**Request Body:**
```json
{
  "text": "Invoice content here...",
  "analysis_type": "entity_extraction|sentiment|summary",
  "language": "en"
}
```

**Response:**
```json
{
  "status": "success",
  "entities": {
    "vendor_name": "Company Inc",
    "invoice_id": "INV-12345",
    "total_amount": 2500.00
  },
  "confidence": 0.95
}
```

#### Document Classification

```
POST /api/v1/documents/classify
```

### Implementation

```python
import requests

def classify_document(text):
    response = requests.post(
        f"{SKYWORK_BASE_URL}/api/v1/documents/classify",
        headers={"Authorization": f"Bearer {SKYWORK_API_KEY}"},
        json={"text": text}
    )
    return response.json()
```

---

## Dolibarr API

**Purpose:** ERP integration for invoice storage, customer management, and financial data synchronization

### Authentication

```python
DOLIBARR_URL = os.getenv("DOLIBARR_URL", "https://dolibarr.luvium.online")
DOLIBARR_API_KEY = os.getenv("DOLIBARR_API_KEY")
DOLIBARR_USER_ID = os.getenv("DOLIBARR_USER_ID")
```

### Endpoints

#### Create Invoice

```
POST /api/index.php/invoices
```

**Request Headers:**
```
Authorization: {DOLIBARR_API_KEY}
Accept: application/json
Content-Type: application/json
```

**Request Body:**
```json
{
  "socid": 1,
  "date": "2025-10-29",
  "date_due": "2025-11-28",
  "type": "0",
  "ref_client": "CLIENT-001",
  "total_net": 1000.00,
  "total_tax": 100.00,
  "total_ttc": 1100.00,
  "lines": [
    {
      "fk_product": 1,
      "qty": 2,
      "price": 500.00,
      "tva_tx": 10.0
    }
  ]
}
```

**Response:**
```json
{
  "id": 123,
  "ref": "INV-2025-001",
  "status": "draft",
  "date": "2025-10-29"
}
```

#### Get Customer

```
GET /api/index.php/thirdparties/{id}
```

#### Update Invoice Status

```
PUT /api/index.php/invoices/{id}
```

### Implementation

```python
import requests

def create_dolibarr_invoice(invoice_data):
    headers = {
        "Authorization": DOLIBARR_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{DOLIBARR_URL}/api/index.php/invoices",
        headers=headers,
        json=invoice_data
    )
    
    return response.json()
```

---

## Environment Configuration

### Required Environment Variables

```bash
# Bytez API
BYTEZ_API_KEY=your_bytez_api_key
BYTEZ_BASE_URL=https://api.bytez.io

# Brevo API
BREVO_API_KEY=your_brevo_api_key

# Skywork.ai API
SKYWORK_API_KEY=your_skywork_api_key
SKYWORK_BASE_URL=https://api.skywork.ai

# Dolibarr API
DOLIBARR_URL=https://dolibarr.luvium.online
DOLIBARR_API_KEY=your_dolibarr_api_key
DOLIBARR_USER_ID=your_user_id
```

### Sample .env File

See `.env.example` for a complete template.

---

## Error Handling Strategy

### Fallback Mechanisms

1. **Bytez Failure** → Fallback to Google Gemini
2. **Brevo Failure** → Log and queue for retry
3. **Skywork Failure** → Use local NLP fallback
4. **Dolibarr Failure** → Store locally and retry

### Retry Logic

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10),
       stop=stop_after_attempt(3))
async def call_external_api(endpoint, data):
    # API call with automatic retry on failure
    pass
```

---

## Rate Limiting

- **Bytez:** 1000 requests/hour
- **Brevo:** 10,000 requests/day
- **Skywork.ai:** 500 requests/hour
- **Dolibarr:** 300 requests/hour

---

## Testing

### Unit Tests for API Integration

```bash
pytest tests/test_api_integration.py -v
```

### API Mock Server

```bash
python -m mockserver --port 8888
```

---

## References

- [Bytez Documentation](https://docs.bytez.io)
- [Brevo API Reference](https://developers.brevo.com)
- [Skywork.ai API Guide](https://docs.skywork.ai)
- [Dolibarr API Documentation](https://wiki.dolibarr.org/index.php/API)

---

## Support

For issues with API integrations, please contact:
- **Technical Support:** tech@luvium.online
- **Integration Team:** integration@luvium.online
