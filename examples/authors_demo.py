"""
Example script demonstrating authors table functionality.

This script shows how to:
1. Load NeurIPS data with author information
2. Query authors by name and institution
3. Find all papers by a specific author
4. Find all authors for a specific paper
"""

from neurips_abstracts import DatabaseManager


def main():
    # Sample NeurIPS data with authors
    sample_data = [
        {
            "id": 123456,
            "uid": "abc123",
            "name": "Deep Learning with Neural Networks",
            "abstract": "This paper explores deep neural networks for various applications.",
            "authors": [
                {
                    "id": 457880,
                    "fullname": "Miaomiao Huang",
                    "url": "http://neurips.cc/api/miniconf/users/457880?format=json",
                    "institution": "Northeastern University",
                },
                {
                    "id": 457881,
                    "fullname": "John Smith",
                    "url": "http://neurips.cc/api/miniconf/users/457881?format=json",
                    "institution": "MIT",
                },
            ],
            "keywords": "deep learning, neural networks",
            "topic": "General Machine Learning",
            "decision": "Accept (poster)",
            "session": "Poster Session A",
            "eventtype": "Poster",
            "event_type": "poster_template",
            "room_name": "Hall A",
            "virtualsite_url": "https://neurips.cc/virtual/2025/poster/123456",
            "url": "https://openreview.net/forum?id=abc123",
            "sourceid": 123456,
            "sourceurl": "https://openreview.net/forum?id=abc123",
            "starttime": "2025-12-10T10:00:00",
            "endtime": "2025-12-10T12:00:00",
            "starttime2": None,
            "endtime2": None,
            "diversity_event": False,
            "paper_url": "https://openreview.net/forum?id=abc123",
            "paper_pdf_url": "https://openreview.net/pdf?id=abc123",
            "children_url": None,
            "children": [],
            "children_ids": [],
            "parent1": None,
            "parent2": None,
            "parent2_id": None,
            "eventmedia": None,
            "show_in_schedule_overview": True,
            "visible": True,
            "poster_position": "A-1",
            "schedule_html": "<p>Poster Session A</p>",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "related_events": [],
            "related_events_ids": [],
        },
        {
            "id": 123457,
            "uid": "def456",
            "name": "Advances in Computer Vision",
            "abstract": "This paper discusses state-of-the-art computer vision techniques.",
            "authors": [
                {
                    "id": 457881,
                    "fullname": "John Smith",
                    "url": "http://neurips.cc/api/miniconf/users/457881?format=json",
                    "institution": "MIT",
                },
                {
                    "id": 457882,
                    "fullname": "Jane Doe",
                    "url": "http://neurips.cc/api/miniconf/users/457882?format=json",
                    "institution": "Stanford University",
                },
            ],
            "keywords": "computer vision, image processing",
            "topic": "Computer Vision",
            "decision": "Accept (oral)",
            "session": "Oral Session B",
            "eventtype": "Oral",
            "event_type": "oral_template",
            "room_name": "Hall B",
            "virtualsite_url": "https://neurips.cc/virtual/2025/oral/123457",
            "url": "https://openreview.net/forum?id=def456",
            "sourceid": 123457,
            "sourceurl": "https://openreview.net/forum?id=def456",
            "starttime": "2025-12-10T14:00:00",
            "endtime": "2025-12-10T15:00:00",
            "starttime2": None,
            "endtime2": None,
            "diversity_event": False,
            "paper_url": "https://openreview.net/forum?id=def456",
            "paper_pdf_url": "https://openreview.net/pdf?id=def456",
            "children_url": None,
            "children": [],
            "children_ids": [],
            "parent1": None,
            "parent2": None,
            "parent2_id": None,
            "eventmedia": None,
            "show_in_schedule_overview": True,
            "visible": True,
            "poster_position": None,
            "schedule_html": "<p>Oral Session B</p>",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "related_events": [],
            "related_events_ids": [],
        },
    ]

    # Create database and load data
    with DatabaseManager("examples/authors_demo.db") as db:
        print("Creating database tables...")
        db.create_tables()

        print("Loading sample data...")
        count = db.load_json_data(sample_data)
        print(f"Loaded {count} papers\n")

        # Get statistics
        paper_count = db.get_paper_count()
        author_count = db.get_author_count()
        print(f"Total papers: {paper_count}")
        print(f"Total unique authors: {author_count}\n")

        # Search authors by name
        print("=" * 70)
        print("SEARCHING AUTHORS BY NAME")
        print("=" * 70)
        authors = db.search_authors(name="Smith")
        print(f"\nAuthors matching 'Smith': {len(authors)}")
        for author in authors:
            print(f"  - {author['fullname']} ({author['institution']})")

        # Search authors by institution
        print("\n" + "=" * 70)
        print("SEARCHING AUTHORS BY INSTITUTION")
        print("=" * 70)
        authors = db.search_authors(institution="University")
        print(f"\nAuthors from institutions containing 'University': {len(authors)}")
        for author in authors:
            print(f"  - {author['fullname']} ({author['institution']})")

        # Get all papers by a specific author
        print("\n" + "=" * 70)
        print("PAPERS BY SPECIFIC AUTHOR")
        print("=" * 70)
        author_id = 457881  # John Smith
        papers = db.get_author_papers(author_id)
        print(f"\nPapers by John Smith (ID: {author_id}): {len(papers)}")
        for paper in papers:
            print(f"  - {paper['name']}")
            print(f"    Decision: {paper['decision']}")
            print(f"    Event Type: {paper['eventtype']}")

        # Get all authors for a specific paper
        print("\n" + "=" * 70)
        print("AUTHORS FOR SPECIFIC PAPER")
        print("=" * 70)
        paper_id = 123456
        authors = db.get_paper_authors(paper_id)
        print(f"\nAuthors for paper ID {paper_id} (in order):")
        for author in authors:
            print(f"  {author['author_order']}. {author['fullname']}")
            print(f"     Institution: {author['institution']}")
            print(f"     URL: {author['url']}")

        # Search papers and get their authors
        print("\n" + "=" * 70)
        print("PAPERS WITH AUTHORS")
        print("=" * 70)
        papers = db.search_papers(keyword="learning")
        print(f"\nPapers containing 'learning': {len(papers)}")
        for paper in papers:
            print(f"\n  {paper['name']}")
            print(f"  Decision: {paper['decision']}")

            # Get authors for this paper
            authors = db.get_paper_authors(paper["id"])
            author_names = [a["fullname"] for a in authors]
            print(f"  Authors: {', '.join(author_names)}")

        print("\n" + "=" * 70)
        print("DONE!")
        print("=" * 70)
        print(f"\nDatabase saved to: examples/authors_demo.db")


if __name__ == "__main__":
    main()
