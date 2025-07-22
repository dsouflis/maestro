# Contributing to Maestro

Thank you for considering contributing to Maestro! We welcome contributions from the community.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/azure-maestro.git
   cd azure-maestro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   pip install -e .[dev]
   ```

## Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Run these tools before submitting:
```bash
black .
flake8 .
mypy .
```

## Testing

Run tests with:
```bash
pytest
pytest --cov  # With coverage
```

## Project Structure

- `types.py` - Pydantic models and type definitions
- `azure_cli.py` - Azure CLI integration functions
- `state_management.py` - Local state operations
- `commands/` - Command implementations organized by theme:
  - `initialization.py` - Setup/teardown commands
  - `synchronization.py` - Sync operations
  - `scaling.py` - Scaling operations
  - `configuration.py` - Configuration management
  - `deployment.py` - Deployment operations
- `main.py` - CLI entry point and argument parsing

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass and code is properly formatted
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Reporting Issues

Please use GitHub Issues to report bugs or request features. Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, Azure CLI version)

## Musical Terminology

When adding new commands, consider using Italian musical terms that relate to the functionality. The existing naming convention helps make the tool memorable and intuitive.