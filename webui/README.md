# NeurIPS Abstracts Web Interface

A modern, clean web interface for exploring NeurIPS conference papers with AI-powered search and chat capabilities.

## Features

### 🔍 **Paper Search**
- **Keyword Search**: Traditional text-based search through paper titles and abstracts
- **Semantic Search**: AI-powered semantic similarity search using embeddings
- **Filters**: Filter by year, limit results
- **Rich Results**: View paper details, authors, abstracts, and PDFs

### 💬 **AI Chat Assistant**
- **RAG-Powered**: Chat with an AI assistant that has access to NeurIPS papers
- **Context-Aware**: Uses relevant papers to answer your questions
- **Conversation History**: Maintains context across multiple questions
- **Adjustable Context**: Control how many papers are used for responses

### 📊 **Statistics**
- View total paper count
- See available year ranges
- Track database contents

## Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-CORS**: Cross-origin resource sharing support
- **neurips-abstracts**: Core package for data access

### Frontend
- **Tailwind CSS**: Modern utility-first CSS framework
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No heavy frameworks, fast and responsive

## Installation

### Prerequisites

1. Install the neurips-abstracts package:
```bash
cd ..
pip install -e ".[dev]"
```

2. Install web dependencies:
```bash
pip install flask flask-cors
```

3. Ensure you have:
   - Downloaded papers: `neurips-abstracts download --year 2025 --db-path neurips_2025.db`
   - Created embeddings: `neurips-abstracts create-embeddings --db-path neurips_2025.db`
   - LM Studio running (for AI chat): http://localhost:1234

### Configuration

Create a `.env` file in the project root (if not already present):

```bash
# LLM Backend
LLM_BACKEND_URL=http://localhost:1234
CHAT_MODEL=gemma-3-4b-it-qat
EMBEDDING_MODEL=text-embedding-qwen3-embedding-4b

# Database Paths
PAPER_DB_PATH=neurips_2025.db
EMBEDDING_DB_PATH=chroma_db

# Optional Settings
COLLECTION_NAME=neurips_papers
MAX_CONTEXT_PAPERS=5
CHAT_TEMPERATURE=0.7
CHAT_MAX_TOKENS=1000
```

## Running the Web Interface

### Development Mode

```bash
cd web
python app.py
```

The server will start at http://127.0.0.1:5000

### Production Mode

```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Command-Line Options

```bash
python app.py --host 0.0.0.0 --port 8080 --debug
```

Options:
- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to bind to (default: 5000)
- `--debug`: Enable debug mode (auto-reload, detailed errors)

## Usage

### Search Papers

1. Navigate to the **Search Papers** tab
2. Enter your search query (e.g., "transformer architecture")
3. Choose search type:
   - Uncheck "Semantic Search" for keyword matching
   - Check "Semantic Search" for AI-powered similarity
4. Optionally filter by year
5. Click **Search**
6. Click on any paper card to view full details

### AI Chat

1. Navigate to the **AI Chat** tab
2. Type your question (e.g., "What are the main themes in attention mechanisms?")
3. Adjust "Papers in context" if needed (3-10 papers)
4. Press Enter or click the send button
5. View AI-generated response with relevant paper context
6. Continue the conversation or click **Reset** to start over

## API Endpoints

The web interface provides a REST API:

### GET `/api/stats`
Get database statistics

**Response:**
```json
{
  "total_papers": 1234,
  "years": [2023, 2024, 2025],
  "year_counts": {"2023": 500, "2024": 400, "2025": 334},
  "min_year": 2023,
  "max_year": 2025
}
```

### POST `/api/search`
Search for papers

**Request:**
```json
{
  "query": "transformer",
  "use_embeddings": true,
  "year": 2025,
  "limit": 10
}
```

**Response:**
```json
{
  "papers": [...],
  "count": 10,
  "query": "transformer",
  "use_embeddings": true
}
```

### GET `/api/paper/<id>`
Get paper details

**Response:**
```json
{
  "id": 123,
  "title": "Paper Title",
  "abstract": "Abstract text...",
  "year": 2025,
  "authors": ["Author 1", "Author 2"],
  "pdf_url": "https://..."
}
```

### POST `/api/chat`
Chat with RAG assistant

**Request:**
```json
{
  "message": "What is a transformer?",
  "n_papers": 5,
  "reset": false
}
```

**Response:**
```json
{
  "response": "A transformer is...",
  "message": "What is a transformer?"
}
```

### POST `/api/chat/reset`
Reset chat conversation

**Response:**
```json
{
  "success": true,
  "message": "Conversation reset"
}
```

### GET `/api/years`
Get available years

**Response:**
```json
{
  "years": [2023, 2024, 2025]
}
```

## Project Structure

```
web/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── app.js         # Frontend JavaScript
│   └── style.css      # Custom CSS
└── README.md          # This file
```

## Customization

### Styling

Edit `static/style.css` to customize styles. The interface uses Tailwind CSS, so you can also add Tailwind utility classes directly in the HTML.

### Layout

Edit `templates/index.html` to modify the page structure.

### Functionality

Edit `static/app.js` to add new features or modify existing ones.

### API

Edit `app.py` to add new endpoints or modify existing ones.

## Troubleshooting

### Web server won't start

**Problem**: `Address already in use`
**Solution**: Another process is using port 5000. Either stop it or use a different port:
```bash
python app.py --port 8080
```

### No papers found

**Problem**: Database is empty or doesn't exist
**Solution**: Download papers first:
```bash
neurips-abstracts download --year 2025 --db-path neurips_2025.db
```

### Semantic search not working

**Problem**: Embeddings not created
**Solution**: Create embeddings:
```bash
neurips-abstracts create-embeddings --db-path neurips_2025.db
```

### AI chat not working

**Problem**: LM Studio not running or model not loaded
**Solution**: 
1. Start LM Studio
2. Load the chat model configured in `.env`
3. Verify it's running at http://localhost:1234

### CORS errors

**Problem**: Frontend can't connect to backend
**Solution**: Flask-CORS is installed and enabled. Check browser console for specific errors.

## Performance

### Tips for Better Performance

1. **Use semantic search wisely**: It's more accurate but slower than keyword search
2. **Limit results**: Request only the number of results you need
3. **Index your database**: Ensure SQLite indexes are created (automatic)
4. **Cache embeddings**: Embeddings are cached automatically in ChromaDB

### Scaling

For production deployment:

1. **Use gunicorn**: Better performance than Flask development server
2. **Add reverse proxy**: Use nginx for static files and load balancing
3. **Database optimization**: Consider connection pooling for high traffic
4. **Caching**: Add Redis for response caching
5. **CDN**: Serve static files from CDN

## Security

### Production Deployment

1. **Disable debug mode**: Never run with `--debug` in production
2. **Use HTTPS**: Always use SSL/TLS certificates
3. **Authentication**: Add user authentication if needed
4. **Rate limiting**: Implement rate limiting to prevent abuse
5. **Input validation**: All inputs are validated server-side
6. **CORS**: Configure CORS appropriately for your domain

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Contributing

To contribute to the web interface:

1. Follow the coding style in existing files
2. Test thoroughly in multiple browsers
3. Ensure mobile responsiveness
4. Update this README if adding features

## License

Same as the parent neurips-abstracts package (MIT).

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main package documentation
3. Check console for error messages
