"""
Tests for Pydantic validation in database module.
"""

import pytest
from neurips_abstracts.database import DatabaseManager


class TestPydanticValidation:
    """Tests for Pydantic data validation."""

    def test_invalid_paper_id_type(self, connected_db):
        """Test that invalid paper ID type is rejected."""
        data = [
            {
                "id": "not-a-number",  # Invalid: should be integer
                "name": "Test Paper",
                "abstract": "Test abstract",
            }
        ]

        # Should not raise, but should log warning and skip record
        count = connected_db.load_json_data(data)
        assert count == 0  # Record should be skipped due to validation error

    def test_missing_required_fields(self, connected_db):
        """Test that missing required fields are rejected."""
        data = [
            {
                "id": 123456,
                # Missing required 'name' field
                "abstract": "Test abstract",
            }
        ]

        count = connected_db.load_json_data(data)
        assert count == 0  # Record should be skipped due to validation error

    def test_empty_paper_name(self, connected_db):
        """Test that empty paper name is rejected."""
        data = [
            {
                "id": 123456,
                "name": "",  # Invalid: name cannot be empty
                "abstract": "Test abstract",
            }
        ]

        count = connected_db.load_json_data(data)
        assert count == 0  # Record should be skipped due to validation error

    def test_invalid_author_data(self, connected_db):
        """Test that invalid author data is handled gracefully."""
        data = [
            {
                "id": 123456,
                "name": "Valid Paper",
                "abstract": "Test abstract",
                "authors": [
                    {
                        "id": 999999,
                        "fullname": "",  # Invalid: fullname cannot be empty
                        "url": "http://test.com",
                    }
                ],
            }
        ]

        # Paper should be inserted but invalid author should be skipped
        count = connected_db.load_json_data(data)
        assert count == 1  # Paper inserted despite invalid author

        # Check that no authors were inserted
        authors = connected_db.get_paper_authors(123456)
        assert len(authors) == 0

    def test_valid_data_passes_validation(self, connected_db):
        """Test that valid data passes validation."""
        data = [
            {
                "id": 123456,
                "name": "Valid Paper Title",
                "abstract": "This is a valid abstract",
                "authors": [
                    {
                        "id": 999999,
                        "fullname": "John Doe",
                        "url": "http://test.com",
                        "institution": "Test University",
                    }
                ],
                "topic": "Machine Learning",
                "keywords": ["deep learning", "neural networks"],
                "decision": "Accept (poster)",
                "session": "Test Session",
                "eventtype": "Poster",
                "event_type": "poster_template",
                "diversity_event": False,  # Can be boolean
            }
        ]

        count = connected_db.load_json_data(data)
        assert count == 1

        # Verify data was inserted correctly
        papers = connected_db.search_papers(keyword="Valid")
        assert len(papers) == 1
        assert papers[0]["name"] == "Valid Paper Title"

        # Verify author was inserted
        authors = connected_db.get_paper_authors(123456)
        assert len(authors) == 1
        assert authors[0]["fullname"] == "John Doe"

    def test_extra_fields_allowed(self, connected_db):
        """Test that extra fields not in model are allowed."""
        data = [
            {
                "id": 123456,
                "name": "Paper with Extra Fields",
                "abstract": "Test abstract",
                "extra_field_1": "This field is not in the model",
                "extra_field_2": 12345,
                "nested_extra": {"key": "value"},
            }
        ]

        # Should succeed because extra fields are allowed
        count = connected_db.load_json_data(data)
        assert count == 1

    def test_type_coercion(self, connected_db):
        """Test that Pydantic coerces compatible types."""
        data = [
            {
                "id": "123456",  # String that can be converted to int
                "name": "Test Paper",
                "abstract": "Test abstract",
                "sourceid": "789",  # String that can be converted to int
            }
        ]

        count = connected_db.load_json_data(data)
        assert count == 1

        papers = connected_db.search_papers(keyword="Test")
        assert papers[0]["id"] == 123456  # Should be integer
