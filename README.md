# Argyle Scanner

## Introduction

This project is designed to automate the process of collecting data from the Upwork portal using web scraping
techniques. The scanner logs into the portal, retrieves valuable information, and returns it as structured data in JSON
format. The project is built with Python, and it emphasizes maintainability, scalability, and resilience to handle
potential errors and unknown situations.

## Features

- Automated data collection using web scraping
- Configurable scanning settings
- Support for multiple data sources
- Integration with Celery for background task processing
- Comprehensive logging and error handling

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd argyle_scanning
    ```

2. Build and start the containers:
    ```sh
    docker-compose up --build
    ```

## Usage

1. Access the API endpoints:
    - `POST /api/scanner/<name>`: Start a scanning task
    - `GET /api/scanner/status/<message_id>`: Check the status of a task

## Extending the Project

### Adding a New Scanner

1. **Create a new scanner creator**:
    - Implement a new creator class in the `app/services/scanners` directory. Ensure it inherits from `ScannerCreator`.

    ```python
    # Example: app/services/scanners/new_scanner_creator.py
    from app.services.scanners.scanner_creator import ScannerCreator

    class NewScannerCreator(ScannerCreator):
        def create_scanner(self):
            # Implement the scanner creation logic
            pass
    ```

2. **Register the new scanner**:
    - Register the new scanner in the `_scanner_selector` dictionary in `tasks.py`:

    ```python
    # Example: tasks.py
    _scanner_selector: Dict[str, ScannerCreator] = {
        "upwork": UpworkCreator(),
        "new_scanner": NewScannerCreator(),  # Add your new scanner here
    }
    ```

3. **Update settings**:
    - Add the necessary settings for the new scanner in the appropriate settings file.
    - Create a JSON file under the `scanner_settings` directory with the settings for the new scanner.

    ```json
      // Example: scanner_settings/new_scanner.json
    {
        "username": "your_username",
        "password": "your_password",
        "other_setting": "value"
    }
    ```

### Environment Variables

- `FLASK_ENV`: The environment in which the Flask application is running (e.g., development, production).
- `FLASK_PORT`: The port on which the Flask application will run.
- `SCANNER_SETTINGS`: The directory containing scanner configuration files.
  ```env
    FLASK_PORT=5002
    FLASK_ENV=development
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    SCANNER_SETTINGS=settings
    ```

