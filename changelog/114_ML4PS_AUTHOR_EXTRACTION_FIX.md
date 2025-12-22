# ML4PS Author Extraction Fix

**Date**: December 22, 2025  
**Status**: ✅ Fixed  
**Impact**: High - All ML4PS papers now have complete author information

## Problem

The ML4PS downloader plugin was only populating author data for the first 15 papers out of 266 total papers. The remaining 251 papers had empty author fields in the database.

### Root Cause

The HTML structure on the ML4PS workshop website changed between papers:

- **First 15 papers**: Used `<br>Authors</br>` format (authors inside the br tag)
- **Remaining papers**: Used `<br/>Authors` format (self-closing br tag with authors as siblings)

The author extraction code only handled the first case, where authors were contained within the `<br>` tag's contents. It didn't handle the case where authors appeared as sibling elements after a self-closing `<br/>` tag.

## Solution

Updated the `_extract_paper_info_from_row` method in `ml4ps_downloader.py` to handle both HTML formats:

1. **Case 1**: Authors inside `<br>` tag (original logic)
   - Check `br_tag.string` and `br_tag.contents`

2. **Case 2**: Authors after self-closing `<br/>` tag (new logic)
   - Iterate through `br_tag.next_siblings` to collect text content
   - Skip link elements and other tags
   - Combine text fragments into the authors string

### Code Changes

**File**: `src/neurips_abstracts/plugins/ml4ps_downloader.py`

```python
# Extract authors - handle both <br>...</br> and <br/> formats
authors = ""
br_tag = content.find("br")
if br_tag:
    # Case 1: Authors inside <br> tag (old format: <br>Authors</br>)
    if br_tag.string:
        authors = br_tag.string
    elif br_tag.contents:
        authors_parts = []
        for item in br_tag.contents:
            if isinstance(item, str):
                authors_parts.append(item.strip())
            else:
                authors_parts.append(item.get_text(strip=True))
        authors = " ".join(authors_parts)
    
    # Case 2: Authors after self-closing <br/> tag (new format)
    if not authors.strip():
        # Get all siblings after the br tag
        authors_parts = []
        for sibling in br_tag.next_siblings:
            if isinstance(sibling, str):
                text = sibling.strip()
                if text:
                    authors_parts.append(text)
            elif sibling.name not in ['a', 'br']:  # Skip links and nested br tags
                text = sibling.get_text(strip=True)
                if text:
                    authors_parts.append(text)
        if authors_parts:
            authors = " ".join(authors_parts)
```

## Results

After applying the fix and re-downloading the data:

### Before

- Total papers: 266
- Papers with authors: 15 (5.6%)
- Papers without authors: 251 (94.4%)
- Author relationships: ~60

### After

- Total papers: 266
- Papers with authors: 266 (100%) ✅
- Papers without authors: 0 (0%)
- Author relationships: 1,177

## Verification

Tested on previously broken papers:

**Paper 28** (SeasonCast: A Masked Latent Diffusion Model):

- Authors: Tung Nguyen, Tuan Pham, Corinna Cortes, Rao Kotamarthi, Ian Foster, Sandeep Madireddy, Aditya Grover

**Paper 32** (Radio Astronomy in the Era of Vision-Language Models):

- Authors: Mariia Drozdova, Erica Lastufka, Vitaliy Kinakh, Taras Holotyak, Daniel Schaerer, Slava Voloshynovskiy

## Impact

- ✅ All 266 ML4PS workshop papers now have complete author information
- ✅ Author search and filtering now works for all papers
- ✅ Web UI displays authors correctly for all papers
- ✅ Database integrity maintained with proper foreign key relationships

## Migration

Users with existing ML4PS databases should re-download the data:

```bash
# Clear old data and re-download
uv run neurips-abstracts download --plugin ml4ps --year 2025 --output data/neurips_2025.db --force
```

Or manually delete ML4PS papers and re-import:

```python
import sqlite3

conn = sqlite3.connect('data/neurips_2025.db')
cursor = conn.cursor()

# Delete old ML4PS data
cursor.execute('DELETE FROM paper_authors WHERE paper_id IN (SELECT id FROM papers WHERE conference LIKE "%ML4PS%")')
cursor.execute('DELETE FROM papers WHERE conference LIKE "%ML4PS%"')

conn.commit()
conn.close()
```

Then re-download using the CLI command above.

## Testing

The fix was tested by:

1. Scraping sample papers from the live website
2. Verifying author extraction for both HTML formats
3. Re-downloading all 266 papers
4. Validating database integrity
5. Checking author names match the website

All tests passed successfully.

## Related Files

- `src/neurips_abstracts/plugins/ml4ps_downloader.py`: Author extraction logic
- `src/neurips_abstracts/database.py`: Author storage and relationships
- `data/neurips_2025.db`: Updated database with complete author data

## Notes

This fix demonstrates the importance of robust HTML parsing that handles multiple formats. The ML4PS workshop website appears to have inconsistent HTML formatting across papers, likely due to manual editing or different generation methods.

The fix is backward compatible and will continue to work if the website format changes back to the original style.
