# Server Setup

## Requirements

- Python 3.11

## Installation

1. Set up a virtual environment (recommended):

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:

   ```bash
   pip install -r ../requirements.txt
   ```

3. Configure environment variables:
   Make sure your `.env` file is properly set up in the server directory.

## MacOS SSL Certificate Configuration

If you're using MacOS, you may encounter SSL certificate issues when working with YouTube and other external APIs. The codebase includes utilities to handle this:

1. You can run the certificate installation script:

   ```bash
   python api/utils/install_certifi.py
   ```

2. Alternatively, the code automatically handles certificate issues for YouTube downloads by creating an unverified SSL context.

## Running the Server

```bash
python manage.py runserver
```
