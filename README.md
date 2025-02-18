# Loss Run Report Processing System

## Overview
This project is a Django-based application designed to process loss run reports from PDF files. It extracts relevant data, validates it, and stores it in a database. The system also uses Celery for background task processing and integrates with the OpenAI API for claim summarization and sentiment analysis.

## Features
- **PDF Data Extraction**: Extracts data from loss run reports in PDF format.
- **Data Validation**: Validates extracted data using Django REST framework serializers.
- **Background Processing**: Uses Celery for asynchronous task processing.
- **OpenAI Integration**: Utilizes OpenAI's GPT models for claim summarization and sentiment analysis.
- **Multi-tenancy**: Support for multiple tenants, allowing businesses to manage their own wallets and customers.
- **Shared Database & Shared Tables**: All tenants share the same tables, simplifying database management.
- **Tenant-Aware Queries**: Middleware dynamically identifies the tenant and filters queries by tenant_id to ensure data isolation.
- **Single Database, Single Schema**: No need for separate schemas for each tenant.
- **Scalability**: This architecture scales well for tenants that don't require significant isolation.
- **Simplified Migrations**: Apply migrations once, and they will be applied to all tenants sharing the same tables.

## Technical Details

### Stack
- **Backend**: Django, Django REST framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis as the broker
- **Machine Learning**: OpenAI API for NLP tasks
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: Nginx

### Directory Structure
```
loss_run_project/
│
├── loss_run/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── utils.py
│   ├── views.py
│   └── handlers
│
├── claim_flow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── requirements.txt
└── README.md
```

## Quickstart

### Prerequisites
- Docker
- Docker Compose
- Python 3.10
- pip

### Installation

#### Clone the Repository:
```sh
git clone https://github.com/akanuragkumar/ClaimFlowAI.git
cd ClaimFlowAI
```

#### Install Dependencies:
```sh
pip install -r requirements.txt
```

#### Build and Run Containers:
```sh
docker-compose up --build
```

#### Access the Application:
Open your browser and navigate to `http://localhost`.

#### Stop the Containers:
```sh
docker-compose down
```

## Environment Variables
Ensure you have the following environment variables set:
- `DJANGO_SETTINGS_MODULE`: Path to your Django settings module.
- `DATABASE_URL`: URL for your PostgreSQL database.
- `REDIS_URL`: URL for your Redis instance.
- `OPENAI_API_KEY`: Your OpenAI API key.

## Database Migrations
Run the following command to apply database migrations:
```sh
docker-compose run web python manage.py migrate
```

## Implementation Details

### Data Extraction
The `utils.py` module contains functions to extract data from PDF files using `pdfplumber` and regular expressions.

### Data Validation
The `serializers.py` module contains serializers to validate the extracted data before saving it to the database.

### Background Tasks
The `tasks.py` module contains Celery tasks for data enrichment, sentiment analysis, and report generation.

