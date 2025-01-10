# Hunter.io Python SDK

A clean, type-safe Python SDK for the Hunter.io API with built-in storage capabilities.

## Features

- 🔍 Email verification using Hunter.io API
- 🌐 Domain search functionality
- 💾 Thread-safe in-memory storage
- ✨ Clean, modular architecture
- 📝 Comprehensive type hints and documentation
- 🔒 Error handling with custom exceptions
- 🧪 Test coverage

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from hunter_sdk import HunterService

# Initialize service
service = HunterService(api_key='your_api_key')

# Verify and store email
result = service.verify_and_store_email('example@domain.com')
print(result)

# Retrieve stored verification
stored = service.get_email_verification('example@domain.com')
print(stored)

# Search domain
domain_results = service.search_domain('example.com')
print(domain_results)
```

## Development

### Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

### Testing

```bash
# Run tests
pytest tests/

# Check types
mypy hunter_sdk/

# Check code style
flake8 hunter_sdk/
```

## Project Structure

```
hunter_sdk/
├── client.py      # HTTP client for Hunter.io API
├── service.py     # Main service layer
├── storage.py     # Storage implementations
└── exceptions.py  # Custom exceptions
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
