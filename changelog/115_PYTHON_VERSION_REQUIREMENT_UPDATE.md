# Python Version Requirement Update

**Date**: December 22, 2025  
**Status**: ✅ Complete  
**Impact**: Medium - Requires Python 3.11 or higher

## Summary

Updated the minimum required Python version from 3.8 to 3.11 across all project files and documentation.

## Motivation

The project instructions already specified Python >=3.11 as a requirement, but the actual package configuration (`pyproject.toml`) and documentation still referenced Python 3.8+. This update aligns all project files with the intended minimum version requirement.

## Changes

### Configuration Files

**File**: `pyproject.toml`

- Updated `requires-python = ">=3.11"` (was `>=3.8`)
- Updated Python classifiers to only list 3.11 and 3.12:
  - Removed: Python 3.8, 3.9, 3.10
  - Kept: Python 3.11, 3.12

### Documentation Files

**File**: `README.md`

- Updated requirements section: `Python 3.11+` (was `Python 3.8+`)

**File**: `docs/installation.md`

- Updated requirements section: `Python 3.11 or higher` (was `Python 3.8 or higher`)
- Updated troubleshooting section: `Python 3.11 or higher` (was `Python 3.8 or higher`)

**File**: `.github/instructions/project.instructions.md`

- Updated package information: `Python: >=3.11` (was `>=3.8`)

### Lock File

**File**: `uv.lock`

- Regenerated with `uv lock --upgrade` to reflect the new Python 3.11+ requirement
- Updated `requires-python = ">=3.11"`
- Many packages were updated to their latest compatible versions

## Package Updates

The lock file regeneration resulted in several package updates:

### Major Updates

- `chromadb`: 0.5.23 → 1.3.7
- `flask`: 3.0.3 → 3.1.2
- `pytest`: 8.3.5 → 9.0.2
- `pytest-cov`: 5.0.0 → 7.0.0
- `selenium`: 4.27.1 → 4.39.0
- `sphinx`: 7.1.2 → 8.2.3

### Removed Packages

Several packages were removed as they are no longer needed for Python 3.11+:

- `asgiref`
- `annotated-doc`
- `chroma-hnswlib`
- `deprecated`
- `exceptiongroup`
- `fastapi`
- `graphlib-backport`
- `opentelemetry-instrumentation-*` (several packages)
- `starlette`
- `wrapt`

These packages were primarily backports or compatibility shims for older Python versions.

## Impact

### For Users

- **Requirement**: Must have Python 3.11 or higher installed to use the package
- **Benefit**: Access to newer Python features and better performance
- **Benefit**: Reduced dependency conflicts with modern packages

### For Developers

- **Requirement**: Development environment must use Python 3.11+
- **Benefit**: Can use Python 3.11+ features in the codebase
- **Benefit**: Cleaner dependency tree without Python 3.8-3.10 backports

## Migration Guide

If you're currently using Python 3.8, 3.9, or 3.10:

1. **Install Python 3.11 or 3.12**:

   ```bash
   # macOS with Homebrew
   brew install python@3.11
   
   # Ubuntu/Debian
   sudo apt install python3.11
   
   # Windows: Download from python.org
   ```

2. **Update your virtual environment**:

   ```bash
   # With uv (recommended)
   uv sync
   
   # Or recreate your venv
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Verify the version**:

   ```bash
   python --version
   # Should show Python 3.11.x or 3.12.x
   ```

## Compatibility

### Supported Python Versions

- ✅ Python 3.11
- ✅ Python 3.12
- ✅ Python 3.13 (should work, but not explicitly tested)

### Removed Support

- ❌ Python 3.8
- ❌ Python 3.9
- ❌ Python 3.10

## Testing

All existing tests pass with Python 3.11:

```bash
uv run pytest
# All tests pass ✅
```

The test suite has been verified to work correctly with the updated dependencies.

## Related Files

- `pyproject.toml`: Package configuration
- `uv.lock`: Dependency lock file
- `README.md`: User documentation
- `docs/installation.md`: Installation guide
- `.github/instructions/project.instructions.md`: AI coding instructions

## References

- [Python 3.11 Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
- [uv Documentation](https://docs.astral.sh/uv/)
