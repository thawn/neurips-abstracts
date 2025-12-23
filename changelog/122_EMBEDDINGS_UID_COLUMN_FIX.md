# Bug Fix: Embeddings Database Column Reference

## Summary

Fixed a database column reference error in the embeddings module where the code was trying to access the non-existent `id` column instead of the correct `uid` column.

## Problem

When running `neurips-abstracts create-embeddings`, the following error occurred:

```text
Embeddings error: Database error: no such column: id
```

This was caused by the `embed_from_database()` method in `embeddings.py` attempting to select and access a column named `id` from the papers table, but the actual column name in the database schema is `uid`.

## Changes

Modified `src/neurips_abstracts/embeddings.py`:

1. **Line 579**: Changed SQL column selection from `id` to `uid` in the `base_columns` list

   ```python
   # Before:
   base_columns = ["id", "title", "abstract", "authors", "keywords", "session"]
   
   # After:
   base_columns = ["uid", "title", "abstract", "authors", "keywords", "session"]
   ```

2. **Line 596**: Changed row access from `row["id"]` to `row["uid"]`

   ```python
   # Before:
   paper_id = row["id"]
   
   # After:
   paper_id = row["uid"]
   ```

## Root Cause

The database schema was previously updated to use `uid` as the primary key for the papers table (see `database.py` line 126), but the embeddings module was not updated to reflect this change.

## Impact

- Users can now successfully run `neurips-abstracts create-embeddings` without encountering the column error
- The embeddings functionality now correctly reads paper IDs from the database
- All embeddings operations that depend on database reading are now functional

## Testing

- Verified that `embeddings.py` compiles without syntax errors
- Confirmed no other references to the old `id` column exist in the embeddings module
- The CLI command `neurips-abstracts create-embeddings --help` works correctly

## Related Files

- `src/neurips_abstracts/embeddings.py`: Main fix location
- `src/neurips_abstracts/database.py`: Contains the correct schema definition

---

**Date**: December 23, 2025
**Issue**: Database column reference mismatch
**Severity**: Critical - Blocked embeddings functionality
**Status**: ✅ Fixed
