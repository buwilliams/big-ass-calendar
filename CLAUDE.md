# Big Ass Calendar Developer Guide

## Commands
- Setup: `pip install -r requirements.txt`
- Config: `cp config_sample.yaml config.yaml && nano config.yaml`
- Google credentials: `cp google_client_sample.json google_client.json && nano google_client.json`
- Run dev server: `python run.py`
- Run with custom config: `python run.py --config=path/to/config.yaml`
- Run with custom Google client: `python run.py --google-client=path/to/credentials.json`
- Run with both: `python run.py --config=path/to/config.yaml --google-client=path/to/credentials.json`
- Lint Python: `flake8`
- Format Python: `black .`
- Type check: `mypy .`
- Run tests: `pytest`
- Run single test: `pytest tests/path/to/test.py::test_function`

## Code Style Guidelines
- **Python**: Follow PEP 8, use type hints, use f-strings
- **JS**: Use Alpine.js directives, avoid jQuery, use ES6+ features
- **Structure**: Modular design with separate Flask blueprints
- **Imports**: Group standard lib, third-party, then local imports
- **Naming**: snake_case for Python, camelCase for JS
- **Error handling**: Use try/except with specific exceptions
- **Canvas**: Comments for complex drawing operations
- **API**: RESTful endpoints with clear documentation
- **Comments**: Docstrings for functions, inline for complex logic