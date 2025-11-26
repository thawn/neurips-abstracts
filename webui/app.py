"""
Flask web application for NeurIPS Abstracts.

Provides a web interface for searching papers, chatting with RAG,
and exploring the NeurIPS abstracts database.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from neurips_abstracts.database import DatabaseManager
from neurips_abstracts.embeddings import EmbeddingsManager
from neurips_abstracts.rag import RAGChat
from neurips_abstracts.config import get_config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config = get_config()

# Initialize components (lazy loading)
db = None
embeddings_manager = None
rag_chat = None


def get_database():
    """
    Get or create database connection.

    Returns
    -------
    DatabaseManager
        Database instance
    """
    global db
    if db is None:
        db_path = config.paper_db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"Database not found: {db_path}. " "Please run 'neurips-abstracts download' first."
            )
        db = DatabaseManager(db_path)
    return db


def get_embeddings_manager():
    """
    Get or create embeddings manager.

    Returns
    -------
    EmbeddingsManager
        Embeddings manager instance
    """
    global embeddings_manager
    if embeddings_manager is None:
        embeddings_manager = EmbeddingsManager(
            db_path=config.paper_db_path,
            embedding_db_path=config.embedding_db_path,
            collection_name=config.collection_name,
        )
    return embeddings_manager


def get_rag_chat():
    """
    Get or create RAG chat instance.

    Returns
    -------
    RAGChat
        RAG chat instance
    """
    global rag_chat
    if rag_chat is None:
        em = get_embeddings_manager()
        rag_chat = RAGChat(
            embeddings_manager=em,
            lm_studio_url=config.llm_backend_url,
            model=config.chat_model,
        )
    return rag_chat


@app.route("/")
def index():
    """
    Render the main page.

    Returns
    -------
    str
        Rendered HTML template
    """
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    """
    Get database statistics.

    Returns
    -------
    dict
        Statistics including paper count, year range, etc.
    """
    try:
        database = get_database()
        total_papers = database.get_paper_count()

        # Get year statistics
        papers = database.query("SELECT year FROM papers WHERE year IS NOT NULL")
        years = [p["year"] for p in papers]
        year_counts = {}
        for year in years:
            year_counts[year] = year_counts.get(year, 0) + 1

        return jsonify(
            {
                "total_papers": total_papers,
                "years": sorted(set(years)) if years else [],
                "year_counts": year_counts,
                "min_year": min(years) if years else None,
                "max_year": max(years) if years else None,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/search", methods=["POST"])
def search():
    """
    Search for papers.

    Expected JSON body:
    - query: str - Search query
    - use_embeddings: bool - Use semantic search
    - limit: int - Maximum results (default: 10)

    Returns
    -------
    dict
        Search results with papers
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        use_embeddings = data.get("use_embeddings", False)
        limit = data.get("limit", 10)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        if use_embeddings:
            # Semantic search using embeddings
            em = get_embeddings_manager()
            results = em.search(query, n_results=limit)
            papers = results
        else:
            # Keyword search in database
            database = get_database()
            papers = database.search_papers(keyword=query, limit=limit)

            # Convert to list of dicts for JSON serialization
            papers = [dict(p) for p in papers]

        return jsonify({"papers": papers, "count": len(papers), "query": query, "use_embeddings": use_embeddings})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/paper/<int:paper_id>")
def get_paper(paper_id):
    """
    Get a specific paper by ID.

    Parameters
    ----------
    paper_id : int
        Paper ID

    Returns
    -------
    dict
        Paper details including authors
    """
    try:
        database = get_database()
        papers = database.query("SELECT * FROM papers WHERE id = ?", (paper_id,))

        if not papers:
            return jsonify({"error": "Paper not found"}), 404

        paper = dict(papers[0])

        # Get authors
        authors = database.get_paper_authors(paper_id)
        paper["authors"] = [a["name"] for a in authors]

        return jsonify(paper)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Chat with RAG system.

    Expected JSON body:
    - message: str - User message
    - n_papers: int (optional) - Number of papers for context
    - reset: bool (optional) - Reset conversation

    Returns
    -------
    dict
        Chat response with papers used
    """
    try:
        data = request.get_json()
        message = data.get("message", "")
        n_papers = data.get("n_papers", config.max_context_papers)
        reset = data.get("reset", False)

        if not message:
            return jsonify({"error": "Message is required"}), 400

        rag = get_rag_chat()

        if reset:
            rag.reset_conversation()

        # Get response
        response = rag.query(message, n_results=n_papers)

        # Get the papers that were used (from last search)
        # This is a simplified version - you might want to enhance RAGChat
        # to return the papers it used

        return jsonify(
            {
                "response": response,
                "message": message,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/reset", methods=["POST"])
def reset_chat():
    """
    Reset the chat conversation.

    Returns
    -------
    dict
        Success message
    """
    try:
        rag = get_rag_chat()
        rag.reset_conversation()
        return jsonify({"success": True, "message": "Conversation reset"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/years")
def get_years():
    """
    Get available years in the database.

    Returns
    -------
    dict
        List of available years
    """
    try:
        database = get_database()
        papers = database.query("SELECT DISTINCT year FROM papers WHERE year IS NOT NULL ORDER BY year")
        years = [p["year"] for p in papers]
        return jsonify({"years": years})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NeurIPS Abstracts Web Interface")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    print(f"Starting NeurIPS Abstracts Web Interface...")
    print(f"Database: {config.paper_db_path}")
    print(f"Embeddings: {config.embedding_db_path}")
    print(f"Server: http://{args.host}:{args.port}")

    app.run(host=args.host, port=args.port, debug=args.debug)
