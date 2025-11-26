# Command-Line Interface Reference

Complete reference for all CLI commands.

## Global Options

All commands support these global options:

- `--help`: Show help message and exit
- `--version`: Show version information

## Commands

### download

Download NeurIPS papers from OpenReview API.

**Usage:**

```bash
neurips-abstracts download [OPTIONS]
```

**Options:**

- `--year INTEGER`: Conference year to download (required)
- `--db-path TEXT`: Path to SQLite database file (required)
- `--force`: Force re-download even if papers exist
- `--cache/--no-cache`: Enable/disable caching (default: enabled)

**Examples:**

```bash
# Download 2025 papers
neurips-abstracts download --year 2025 --db-path neurips_2025.db

# Force re-download
neurips-abstracts download --year 2025 --db-path neurips_2025.db --force

# Disable caching
neurips-abstracts download --year 2025 --db-path neurips_2025.db --no-cache
```

### create-embeddings

Create vector embeddings for semantic search.

**Usage:**

```bash
neurips-abstracts create-embeddings [OPTIONS]
```

**Options:**

- `--db-path TEXT`: Path to SQLite database with papers (required)
- `--embedding-db-path TEXT`: Path to ChromaDB database (default: from config)
- `--collection-name TEXT`: Collection name in ChromaDB (default: from config)
- `--model TEXT`: Embedding model to use (default: from config)
- `--force`: Recreate embeddings even if they exist

**Examples:**

```bash
# Create embeddings with defaults
neurips-abstracts create-embeddings --db-path neurips_2025.db

# Use custom paths
neurips-abstracts create-embeddings \
    --db-path neurips_2025.db \
    --embedding-db-path custom_embeddings \
    --collection-name my_papers

# Force recreation
neurips-abstracts create-embeddings --db-path neurips_2025.db --force
```

### search

Search papers by keywords or semantic similarity.

**Usage:**

```bash
neurips-abstracts search QUERY [OPTIONS]
```

**Arguments:**

- `QUERY`: Search query string (required)

**Options:**

- `--db-path TEXT`: Path to SQLite database (required)
- `--limit INTEGER`: Maximum number of results (default: 10)
- `--year INTEGER`: Filter by conference year
- `--use-embeddings`: Use semantic search (requires embeddings)
- `--title-only`: Search only in paper titles
- `--abstract-only`: Search only in abstracts

**Examples:**

```bash
# Basic search
neurips-abstracts search "transformer" --db-path neurips_2025.db

# Limit results
neurips-abstracts search "deep learning" --db-path neurips_2025.db --limit 20

# Filter by year
neurips-abstracts search "neural network" --db-path neurips_2025.db --year 2025

# Semantic search using embeddings
neurips-abstracts search "attention mechanism" --db-path neurips_2025.db --use-embeddings

# Search only titles
neurips-abstracts search "BERT" --db-path neurips_2025.db --title-only
```

### chat

Interactive RAG-powered chat interface.

**Usage:**

```bash
neurips-abstracts chat [OPTIONS]
```

**Options:**

- `--db-path TEXT`: Path to SQLite database (required)
- `--embedding-db-path TEXT`: Path to ChromaDB database (default: from config)
- `--model TEXT`: LLM model to use (default: from config)
- `--temperature FLOAT`: Temperature for responses (default: from config)
- `--max-tokens INTEGER`: Maximum tokens in response (default: from config)
- `--n-papers INTEGER`: Number of papers for context (default: from config)

**Interactive Commands:**

While in the chat session:

- Type your question and press Enter to get a response
- `exit` or `quit`: Exit the chat session
- `reset`: Reset the conversation history
- `export [filename]`: Export conversation to JSON file

**Examples:**

```bash
# Start chat with defaults
neurips-abstracts chat --db-path neurips_2025.db

# Use custom model
neurips-abstracts chat --db-path neurips_2025.db --model llama-3.2-3b-instruct

# Adjust response parameters
neurips-abstracts chat \
    --db-path neurips_2025.db \
    --temperature 0.9 \
    --max-tokens 2000 \
    --n-papers 10
```

### info

Show database information and statistics.

**Usage:**

```bash
neurips-abstracts info [OPTIONS]
```

**Options:**

- `--db-path TEXT`: Path to SQLite database (required)
- `--show-embeddings`: Also show embedding statistics

**Examples:**

```bash
# Basic info
neurips-abstracts info --db-path neurips_2025.db

# Include embedding info
neurips-abstracts info --db-path neurips_2025.db --show-embeddings
```

## Environment Variables

All CLI commands respect configuration from environment variables and `.env` files. See the [Configuration](configuration.md) page for details.

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments or options
