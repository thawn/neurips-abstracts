# Changelog Entry 108: Optional Dependencies Fix

**Date**: December 21, 2025  
**Type**: Bug Fix  
**Scope**: Package Dependencies, CLI

## Summary

Fixed critical issue where the CLI tool required Flask and other web dependencies to be installed, even when only using non-web commands. Implemented lazy imports for the web UI module and moved BeautifulSoup4 to core dependencies.

## Problem

The package had a dependency structure issue:

1. **Web UI eager imports**: `web_ui/__init__.py` imported Flask at module level, causing import errors for users who didn't install web dependencies
2. **ML4PS plugin imports**: The ML4PS plugin imported BeautifulSoup4 at the top level, affecting all users
3. **CLI unusable without web dependencies**: Users couldn't use basic commands like `download`, `search`, or `chat` without installing Flask

This violated the principle that optional dependencies should be truly optional.

## Solution

### 1. Lazy Loading for Web UI

Modified `src/neurips_abstracts/web_ui/__init__.py` to use Python's `__getattr__` mechanism for lazy imports:

```python
def __getattr__(name):
    """
    Lazy-load web UI components to avoid importing Flask unless needed.
    
    This allows the CLI and other parts of the package to work without
    the web dependencies installed.
    """
    if name in __all__:
        from .app import app, run_server
        if name == "app":
            return app
        elif name == "run_server":
            return run_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

**Benefits**:
- Flask is only imported when actually accessing `web_ui.app` or `web_ui.run_server`
- Other parts of the package can import without triggering Flask import
- Error messages are clear when Flask is missing

### 2. BeautifulSoup4 as Core Dependency

Moved `beautifulsoup4>=4.12.0` from optional `[web]` dependencies to core dependencies in `pyproject.toml`:

```toml
dependencies = [
    "requests>=2.31.0",
    "chromadb>=0.4.0",
    "pydantic>=2.0.0",
    "beautifulsoup4>=4.12.0",  # Added
]
```

**Rationale**:
- The ML4PS plugin needs BeautifulSoup4 for web scraping
- BeautifulSoup4 is lightweight (~200KB) and has minimal dependencies
- Making it a core dependency simplifies the plugin system
- Users can use ML4PS plugin without installing `[web]` extras

### 3. Maintained Web UI Error Handling

The `web-ui` command already had proper error handling in `cli.py`:

```python
try:
    from neurips_abstracts.web_ui import run_server
except ImportError:
    print("\n❌ Web UI dependencies not installed!", file=sys.stderr)
    print("\nThe web UI requires Flask. Install it with:", file=sys.stderr)
    print("  pip install neurips-abstracts[web]", file=sys.stderr)
    return 1
```

This now works correctly with lazy imports.

## Testing

Created comprehensive test suite in fresh virtual environment:

```bash
# Create test environment
python -m venv temp_venv
source temp_venv/bin/activate
pip install -e .

# Test results:
✓ Package imports successfully
✓ CLI module imports successfully  
✓ Can list plugins (2 plugins available)
✓ DatabaseManager imports successfully
✓ EmbeddingsManager imports successfully
✓ RAGChat imports successfully
✓ web_ui package can be imported
✓ Flask import properly deferred
```

### CLI Commands Work Without Flask

```bash
$ neurips-abstracts --help
# ✓ Shows help text

$ neurips-abstracts download --help
# ✓ Shows download command help

$ neurips-abstracts web-ui
# ❌ Web UI dependencies not installed!
# The web UI requires Flask. Install it with:
#   pip install neurips-abstracts[web]
```

### ML4PS Plugin Works

```python
from neurips_abstracts.plugins import ML4PSDownloaderPlugin
plugin = ML4PSDownloaderPlugin()
# ✓ Works without Flask
# ✓ Can instantiate and use the plugin
```

## Impact

### Users Affected
- **New users**: Can now install and use basic CLI without web dependencies
- **Existing users**: No breaking changes, all functionality preserved
- **ML4PS users**: Plugin now works in base installation

### Files Modified
1. `src/neurips_abstracts/web_ui/__init__.py` - Lazy import implementation
2. `pyproject.toml` - Moved BeautifulSoup4 to core dependencies

### Dependency Structure

**Before**:
```
neurips-abstracts
├── requests (core)
├── chromadb (core)
└── pydantic (core)

[web] (optional)
├── flask
├── flask-cors
└── beautifulsoup4
```

**After**:
```
neurips-abstracts
├── requests (core)
├── chromadb (core)
├── pydantic (core)
└── beautifulsoup4 (core)  ← Moved

[web] (optional)
├── flask
└── flask-cors
```

## Breaking Changes

None. All existing functionality is preserved.

## Documentation Updates

No documentation changes needed - the package already documents optional dependencies correctly.

## Related Issues

- Fixes the CLI being unusable without Flask
- Enables ML4PS plugin in base installation
- Improves package modularity

## Technical Details

### Lazy Import Mechanism

Python's `__getattr__` at module level (PEP 562) allows deferring imports until attribute access:

1. Module is imported normally
2. If attribute doesn't exist, `__getattr__` is called
3. We perform the actual import inside `__getattr__`
4. Return the requested attribute or raise AttributeError

This is a standard pattern for optional dependencies in modern Python packages.

### Why Not Make BeautifulSoup4 Optional?

Considered options:
1. **Make ML4PS plugin optional** - Too complex, breaks plugin discovery
2. **Lazy import in ML4PS** - Added complexity, error handling issues
3. **Make BS4 core dependency** - Simple, lightweight, enables plugins ✓

BeautifulSoup4 is only ~200KB with one small dependency (soupsieve), making it reasonable as a core dependency for web scraping functionality.

## Verification

```bash
# Clean environment test
python -m venv clean_test
source clean_test/bin/activate
pip install -e .

# All core commands work
neurips-abstracts download --list-plugins  # ✓
neurips-abstracts --help                   # ✓

# Web UI shows clear error
neurips-abstracts web-ui                   # ✓ Clear error message

# Install web extras
pip install -e ".[web]"
neurips-abstracts web-ui                   # ✓ Now works
```

## Future Considerations

1. **Other scrapers**: If we add more scraping plugins, BS4 as core dependency makes sense
2. **Alternative parsers**: Could support lxml as alternative parser (also core)
3. **Plugin system**: This pattern can be extended to other optional features

## Conclusion

The package now properly separates core functionality from optional web UI dependencies. Users can:

- ✓ Use CLI commands without Flask
- ✓ Use ML4PS plugin without Flask  
- ✓ Install web dependencies when needed
- ✓ Get clear error messages when dependencies are missing

The fix is minimal, non-breaking, and follows Python best practices for optional dependencies.
