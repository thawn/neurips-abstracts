# Example usage of the neurips_abstracts package

from neurips_abstracts import download_neurips_data, DatabaseManager


def main():
    """
    Example demonstrating the complete workflow.

    This example:
    1. Downloads NeurIPS 2025 conference data
    2. Creates a SQLite database
    3. Loads the data into the database
    4. Performs various queries
    """
    print("=" * 60)
    print("NeurIPS Abstracts Package - Example Usage")
    print("=" * 60)

    # Step 1: Download data
    print("\n1. Downloading NeurIPS 2025 data...")
    try:
        data = download_neurips_data(year=2025, output_path="data/neurips_2025.json")
        print(f"✓ Downloaded data successfully")
    except Exception as e:
        print(f"✗ Failed to download: {e}")
        return

    # Step 2: Create database and load data
    print("\n2. Loading data into SQLite database...")
    db_path = "neurips.db"

    try:
        with DatabaseManager(db_path) as db:
            # Create tables
            db.create_tables()
            print("✓ Database tables created")

            # Load data
            count = db.load_json_data(data)
            print(f"✓ Loaded {count} papers into database")

            # Get statistics
            total_papers = db.get_paper_count()
            print(f"✓ Total papers in database: {total_papers}")

            # Step 3: Query examples
            print("\n3. Running example queries...")

            # Query by track
            print("\n   a) Papers by track:")
            for track in ["oral", "poster"]:
                papers = db.search_papers(track=track)
                print(f"      - {track.capitalize()}: {len(papers)} papers")

            # Search by keyword
            print("\n   b) Searching for 'learning' keyword:")
            papers = db.search_papers(keyword="learning", limit=5)
            print(f"      Found {len(papers)} papers:")
            for i, paper in enumerate(papers, 1):
                print(f"      {i}. {paper['title'][:60]}...")

            # Custom query
            print("\n   c) Custom SQL query - Papers by track:")
            results = db.query(
                """
                SELECT track, COUNT(*) as count 
                FROM papers 
                GROUP BY track
            """
            )
            for row in results:
                print(f"      - {row['track'] or 'Unknown'}: {row['count']} papers")

    except Exception as e:
        print(f"✗ Database operation failed: {e}")
        return

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print(f"Database saved to: {db_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
