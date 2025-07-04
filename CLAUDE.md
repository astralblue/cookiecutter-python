# Claude Session Memory

This file serves as session memory for Claude Code interactions on this cookiecutter-python template project.

## Project Overview

This is a modern Python cookiecutter template that supports:
- **PEP 420 namespace packages** (e.g., `k3l.fcgraph.tools`)
- **Dynamic Python version detection** from endoflife.date API
- **Flit-based packaging** with automatic module configuration
- **Modern development tooling** (Black, isort, pytest, Sphinx)

## Development History

### Session 2025-06-21: Major Feature Development

#### 🎯 **Main Accomplishment: PEP 420 Namespace Package Support**

**Problem**: User wanted to create packages like `k3l.fcgraph.tools` where `k3l` and `k3l.fcgraph` are PEP 420 namespace packages (no `__init__.py`) but `k3l.fcgraph.tools` is a regular package (with `__init__.py`).

**Solution Implemented**:
1. **Updated `cookiecutter.json`** - reordered to ask for `package_name` first, derive `distribution_name`
2. **Enhanced `hooks/post_gen_project.py`** with three new functions:
   - `setup_namespace_packages()` - restructures cookiecutter's flat directory to proper nested structure
   - `update_flit_module_config()` - adds `[tool.flit.module]` section when package name differs from expected
   - Enhanced `fetch_supported_python_versions()` - fixed EOL date parsing

**Key Insight**: Cookiecutter creates directories with dots as literal names (`k3l.fcgraph.tools/`), so post-hook moves files to proper structure (`k3l/fcgraph/tools/`).

#### 🐛 **Bug Fix: Python Version API Parsing**

**Problem**: `fetch_supported_python_versions()` returned empty list because EOL field is date string, not boolean.

**Solution**: Enhanced function to:
- Parse EOL dates in YYYY-MM-DD format
- Handle mixed field types (false/null, true, date strings)
- Add 30-day expiration warnings for versions approaching EOL
- Improved error handling for unparseable dates

#### 🧪 **Testing & Validation**

**Namespace Package Test**:
```bash
cookiecutter . --no-input package_name="k3l.fcgraph.tools" project_name="K3L FCGraph Tools"
```
- ✅ Builds correctly with `flit build`
- ✅ Installs and imports: `import k3l.fcgraph.tools`
- ✅ Proper PEP 420 structure (no `__init__.py` in namespace dirs)
- ✅ Automatic `[tool.flit.module]` configuration

**Simple Package Test**:
```bash
cookiecutter . --no-input package_name="simple_pkg" project_name="Simple Package"
```
- ✅ Builds correctly with traditional structure
- ✅ No unnecessary `[tool.flit.module]` section

#### 📚 **Documentation**

**GitHub Workflow Established**:
- Issue #1: feat: add a project README.md
- PR #2: Comprehensive README with all features documented
- ✅ Merged successfully

**README.md Features**:
- Complete feature overview
- Template variables reference table
- Python version range syntax explanation
- Namespace package examples with directory structures
- Development setup instructions

## Current Project State

### 📁 **File Structure**
```
cookiecutter-python/
├── README.md                    # Comprehensive project documentation
├── cookiecutter.json           # Template variables (package_name first)
├── hooks/
│   └── post_gen_project.py     # Enhanced with namespace package support
└── {{cookiecutter.distribution_name}}/
    ├── README.md
    ├── pyproject.toml           # Flit-based with dynamic metadata
    └── {{cookiecutter.package_name}}/
        └── __init__.py
```

### 🔧 **Key Functions in post_gen_project.py**

1. **`setup_namespace_packages()`**
   - Detects multi-level package names
   - Moves cookiecutter-generated files to proper nested structure
   - Ensures PEP 420 compliance (no `__init__.py` in namespace dirs)

2. **`update_flit_module_config()`**
   - Compares package_name vs expected module name
   - Adds `[tool.flit.module]` section when needed
   - Handles both namespace and simple packages

3. **`fetch_supported_python_versions()`**
   - Fetches from endoflife.date API
   - Parses EOL dates correctly
   - Warns about versions expiring within 30 days
   - Handles network failures gracefully

### 🚀 **GitHub Workflow**

**Established Pattern**:
1. User files GitHub issues with requirements
2. Claude reads issue: `gh issue view <number>`
3. Claude creates feature branch and implements
4. Claude creates PR with detailed description
5. User reviews and merges
6. Claude syncs with main branch

**Recent Commits**:
- `3e0d846` - feat: separate author name from GitHub usernames
- `9b37fbb` - docs: add Claude session memory file
- `855f46b` - fix: handle date-based EOL fields in Python version API
- `152824e` - feat: add PEP 420 namespace package support

## Development Notes

### 🔍 **Package Name Mapping Logic**
- `package_name`: `"k3l.fcgraph.tools"` → `distribution_name`: `"k3l-fcgraph-tools"`
- Expected Flit module: `"k3l_fcgraph_tools"` (dashes → underscores)
- Since `"k3l.fcgraph.tools" != "k3l_fcgraph_tools"` → add `[tool.flit.module]`

### 🧪 **Testing Commands Used**
```bash
# Create test packages
cookiecutter . --no-input package_name="..." project_name="..." python_version_range="3.10-3.12"

# Test building
python3.12 -m venv .venv
.venv/bin/pip install flit
.venv/bin/flit build
.venv/bin/pip install dist/*.whl

# Test importing
.venv/bin/python -c "import <package_name>"
```

### 🐍 **Python Version Range Examples**
- `"3.10-3.12"` → specific range
- `"3.10-"` → minimum with internet lookup for max
- `"-3.12"` → internet lookup for min, specific max
- `"-"` → full internet lookup for both min/max

## Next Session Instructions

If resuming work on this project:

1. **Check recent issues**: `gh issue list --state=open`
2. **Review recent commits**: `git log --oneline -10`
3. **Current branch**: Should be on `main` with all features merged
4. **Test the template**: Try both namespace and simple package generation
5. **Key files to understand**:
   - `cookiecutter.json` - template variables
   - `hooks/post_gen_project.py` - main logic
   - `README.md` - user documentation

## Known Working Examples

### Namespace Package
```bash
cookiecutter . --no-input \
  package_name="k3l.fcgraph.tools" \
  project_name="K3L FCGraph Tools" \
  author_name="Test User" \
  author_email="test@example.com" \
  python_version_range="3.10-3.12"
```

### Simple Package  
```bash
cookiecutter . --no-input \
  package_name="simple_pkg" \
  project_name="Simple Package" \
  python_version_range="3.10-3.12"
```

Both generate working, buildable, installable Python packages.

## Session 2025-07-04: GitHub Username Separation

### 🎯 **Enhancement: Separate Author Name from GitHub Usernames**

**Problem**: User wanted to use real name ("Eugene Kim") as `author_name` but this was being used in GitHub URLs, creating invalid links.

**Solution Implemented**:
1. **Added two new variables to `cookiecutter.json`:**
   - `github_user`: GitHub username (asked first)
   - `github_owner`: Repository owner (defaults to `github_user`)

2. **Updated `pyproject.toml`** to use `github_owner` instead of `author_name` in GitHub URLs:
   - Homepage, Repository, and Issues URLs now use `{{cookiecutter.github_owner}}`

**Key Benefits**:
- `author_name`: "Eugene Kim" (display name in package metadata)
- `github_owner`: "astralblue" (used in GitHub URLs)
- Proper separation of concerns between display names and usernames

**Testing Confirmed**:
- Template generates correct GitHub URLs using `github_owner`
- Author metadata uses proper display name
- Both namespace and simple packages work correctly

---
*Last updated: 2025-07-04 by Claude Code*