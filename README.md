# Cookiecutter Python Template

A modern Python project template with support for PEP 420 namespace packages, dynamic Python version detection, and sensible defaults for contemporary Python development.

## Features

### 🐍 Modern Python Packaging
- **PEP 420 Namespace Packages**: Automatically handles multi-level namespace packages (e.g., `k3l.fcgraph.tools`)
- **Flit-based packaging**: Uses `flit_core` build backend with `pyproject.toml`
- **Dynamic metadata**: Automatically configures Flit module names when needed

### 📦 Intelligent Python Version Management
- **Dynamic version detection**: Fetches current Python support status from [endoflife.date](https://endoflife.date/python)
- **Flexible version ranges**: Support for `3.10-3.12`, `3.10-`, `-3.12`, or single versions
- **EOL warnings**: Alerts when Python versions are approaching end-of-life (within 30 days)
- **Automatic classifiers**: Generates appropriate `Programming Language :: Python :: X.Y` classifiers

### 🛠️ Development Tools
- **Linting & Formatting**: Pre-configured Black and isort with Black profile
- **Testing**: pytest with coverage support
- **Documentation**: Sphinx setup with RTD theme
- **IDE Integration**: JetBrains IDE configuration (`.idea/`)

### 🔧 Project Setup
- **Git initialization**: Creates repository with empty root commit
- **Conventional commits**: Follows semantic commit message format
- **Multi-gitignore**: Combines language-specific and IDE gitignores

## Usage

### Basic Usage

```bash
cookiecutter https://github.com/astralblue/cookiecutter-python
```

### Quick Start with Parameters

```bash
# Simple package
cookiecutter https://github.com/astralblue/cookiecutter-python \
  --no-input \
  package_name="my_package" \
  project_name="My Package" \
  python_version_range="3.10-3.12"

# Namespace package
cookiecutter https://github.com/astralblue/cookiecutter-python \
  --no-input \
  package_name="company.product.module" \
  project_name="Company Product Module" \
  author_name="Your Name" \
  author_email="your.email@example.com"
```

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `project_name` | Human-readable project name | `"My Python Package"` |
| `package_name` | Python import name (supports dots for namespaces) | `"my_package"` or `"company.product.module"` |
| `distribution_name` | PyPI/distribution name (auto-derived) | `"my-package"` or `"company-product-module"` |
| `author_name` | Package author name | `"Your Name"` |
| `author_email` | Author email address | `"your.email@example.com"` |
| `description` | Short package description | `"A short description"` |
| `version` | Initial version | `"0.1.0"` |
| `license` | License type | `"MIT"`, `"BSD-3-Clause"`, `"Apache-2.0"`, `"GPL-3.0"` |
| `python_version_range` | Supported Python versions | `"3.10-3.12"`, `"3.10-"`, `"-"` |

## Python Version Ranges

The template supports flexible Python version specifications:

- **Specific range**: `"3.10-3.12"` → Python 3.10, 3.11, 3.12
- **Minimum only**: `"3.10-"` → Python 3.10 and all newer supported versions
- **Maximum only**: `"-3.12"` → All supported versions up to Python 3.12
- **Single version**: `"3.10"` → Only Python 3.10
- **Auto-detect**: `"-"` → All currently supported Python versions (requires internet)

When using ranges that require internet lookup (`"-"`, `"3.10-"`, `"-3.12"`), the template fetches current Python support status and warns about versions approaching end-of-life.

## Namespace Packages (PEP 420)

The template automatically handles PEP 420 namespace packages:

### Input
```
package_name: "company.product.tools"
```

### Generated Structure
```
company-product-tools/
├── company/
│   └── product/
│       └── tools/
│           └── __init__.py
├── pyproject.toml
└── README.md
```

### Features
- **No `__init__.py`** in namespace directories (`company/`, `company/product/`)
- **Proper `__init__.py`** in the final package (`company/product/tools/`)
- **Automatic Flit configuration** with `[tool.flit.module]` section
- **Correct imports**: `import company.product.tools`

## Development Setup

After generating your project:

```bash
cd your-project-name
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -e .[dev]
```

### Available Commands

```bash
# Formatting
black .
isort .

# Testing
pytest
pytest --cov

# Building
flit build

# Publishing
flit publish
```

## Default Configuration

Consider creating `~/.cookiecutterrc` to set default values:

```yaml
default_context:
    author_name: "Your Name"
    author_email: "your.email@example.com"
```

## Requirements

- Python 3.9+
- Git
- Internet connection (for dynamic Python version detection)

## License

This template is released under the MIT License.