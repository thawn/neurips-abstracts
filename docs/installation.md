# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Install from Source

Clone the repository and install in development mode:

```bash
git clone <repository-url>
cd abstracts
pip install -e .
```

## Dependencies

The package will automatically install the following dependencies:

- **requests**: For API calls to OpenReview
- **chromadb**: For vector embeddings storage
- **pytest**: For running tests
- **pytest-cov**: For test coverage reports
- **pytest-mock**: For test mocking

## Optional Dependencies

For documentation building:

```bash
pip install sphinx sphinx-rtd-theme myst-parser sphinx-autodoc-typehints
```

## Verify Installation

Check that the package is installed correctly:

```bash
neurips-abstracts --help
```

You should see the available commands listed.
