"""
Advanced usage examples for the neurips_abstracts package.
"""

from neurips_abstracts import download_json, DatabaseManager
import logging

# Enable logging to see detailed information
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def example_custom_url():
    """Example: Download from a custom URL."""
    print("\n" + "=" * 60)
    print("Example 1: Download from Custom URL")
    print("=" * 60)

    # Download from any custom URL
    url = "https://neurips.cc/static/virtual/data/neurips-2025-orals-posters.json"

    try:
        data = download_json(url=url, output_path="data/custom_download.json", timeout=60)
        print(f"✓ Downloaded {len(data)} items from custom URL")
    except Exception as e:
        print(f"✗ Download failed: {e}")


def example_batch_processing():
    """Example: Process multiple years of data."""
    print("\n" + "=" * 60)
    print("Example 2: Batch Processing Multiple Years")
    print("=" * 60)

    from neurips_abstracts import download_neurips_data

    years = [2024, 2025]

    with DatabaseManager("multi_year_neurips.db") as db:
        db.create_tables()

        total_papers = 0
        for year in years:
            try:
                print(f"\nProcessing year {year}...")
                data = download_neurips_data(year=year)
                count = db.load_json_data(data)
                total_papers += count
                print(f"✓ Loaded {count} papers from {year}")
            except Exception as e:
                print(f"✗ Failed to process {year}: {e}")

        print(f"\n✓ Total papers loaded: {total_papers}")


def example_advanced_queries():
    """Example: Advanced database queries."""
    print("\n" + "=" * 60)
    print("Example 3: Advanced Database Queries")
    print("=" * 60)

    from neurips_abstracts import download_neurips_data

    # First, ensure we have data
    try:
        data = download_neurips_data(year=2025)
    except:
        print("Using sample data for demonstration")
        data = {
            "papers": [
                {"id": "1", "title": "Deep Learning Paper", "abstract": "About neural networks", "track": "oral"},
                {"id": "2", "title": "Reinforcement Learning", "abstract": "About RL", "track": "poster"},
            ]
        }

    with DatabaseManager("advanced_queries.db") as db:
        db.create_tables()
        db.load_json_data(data)

        # Query 1: Count by track
        print("\n1. Papers by track:")
        results = db.query(
            """
            SELECT track, COUNT(*) as count
            FROM papers
            WHERE track IS NOT NULL AND track != ''
            GROUP BY track
            ORDER BY count DESC
        """
        )
        for row in results:
            print(f"   {row['track']}: {row['count']}")

        # Query 2: Search with complex conditions
        print("\n2. Papers with 'learning' in title or abstract:")
        results = db.query(
            """
            SELECT title, track
            FROM papers
            WHERE (title LIKE '%learning%' OR abstract LIKE '%learning%')
            LIMIT 5
        """
        )
        for i, row in enumerate(results, 1):
            print(f"   {i}. {row['title'][:50]}... ({row['track']})")

        # Query 3: Get recent papers
        print("\n3. Recently added papers:")
        results = db.query(
            """
            SELECT title, created_at
            FROM papers
            ORDER BY created_at DESC
            LIMIT 3
        """
        )
        for row in results:
            print(f"   - {row['title'][:50]}...")


def example_error_handling():
    """Example: Proper error handling."""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling")
    print("=" * 60)

    from neurips_abstracts.downloader import DownloadError
    from neurips_abstracts.database import DatabaseError

    # Handle download errors
    print("\n1. Handling download errors:")
    try:
        data = download_json("https://invalid-url-that-does-not-exist.com/data.json")
    except DownloadError as e:
        print(f"   ✓ Caught DownloadError: {type(e).__name__}")
    except Exception as e:
        print(f"   ✓ Caught exception: {type(e).__name__}")

    # Handle database errors
    print("\n2. Handling database errors:")
    try:
        db = DatabaseManager("test.db")
        # Try to query without connecting
        db.query("SELECT * FROM papers")
    except DatabaseError as e:
        print(f"   ✓ Caught DatabaseError: {type(e).__name__}")


def example_data_export():
    """Example: Export data from database."""
    print("\n" + "=" * 60)
    print("Example 5: Export Data from Database")
    print("=" * 60)

    import json
    from neurips_abstracts import download_neurips_data

    # Create sample database
    try:
        data = download_neurips_data(year=2025)
    except:
        data = {"papers": [{"id": "1", "title": "Sample", "track": "oral"}]}

    with DatabaseManager("export_example.db") as db:
        db.create_tables()
        db.load_json_data(data)

        # Export oral papers to JSON
        print("\nExporting oral papers to JSON...")
        oral_papers = db.search_papers(track="oral", limit=100)

        export_data = [dict(paper) for paper in oral_papers]

        with open("data/oral_papers.json", "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported {len(export_data)} oral papers to data/oral_papers.json")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Advanced Usage Examples")
    print("=" * 60)

    examples = [
        example_custom_url,
        example_batch_processing,
        example_advanced_queries,
        example_error_handling,
        example_data_export,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ Example failed: {e}")

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
