---
name: notion-push
description: Push local chapter markdown files to Notion, auto-detecting create vs update per page, tracked via notion-pages.json. Trigger on "push notes to Notion", "sync chapters", "push chapter N". Not for pulling from Notion or deleting pages.
---

# Notion Push

## Overview

Push chapter markdown files from the repo to Notion. Tracks filename → page_id mappings in `notion-pages.json` and automatically creates new pages or updates existing ones.

## When to Use

- User says "push notes to Notion", "sync chapters", "update Notion", "推章節到 Notion"
- User says "push chapter N" (one or more specific chapters)
- After finishing chapter notes and wanting to sync for the study group to read

**Do not use when:** pulling content from Notion to local, deleting Notion pages, or pushing non-chapter files.

## Core Flow

### Step 1: Resolve Target Files

1. If the user specifies chapters (e.g. "push chapter 3"), match `chapter-03-*.md`; collect multiple if specified
2. If no chapter is specified, find all `chapter-*.md` files in the repo root

### Step 2: Load notion-pages.json

1. If `notion-pages.json` does not exist, initialize it with `{"database_id": "", "pages": {}}` and prompt the user to fill in `database_id`
2. Load the `pages` field as a filename → page_id map

### Step 3: Push Each File

For each target file:

1. Extract the page title from the first `# Heading` line in the markdown file
2. Strip the H1 line from the content before pushing (title is set as a page property, not body content)
3. If `pages[filename]` exists:
   - Run `ntn pages update <page_id>` with the stripped content via stdin
   - PATCH `v1/pages/<page_id>` with `{"properties":{"Name":{"title":[{"text":{"content":"<title>"}}]}}}` to update the title
4. If not → run `ntn pages create --parent database:<database_id> --title "<extracted_title>"` with the stripped content via stdin, capture the returned page_id
5. Record the new page_id into `pages[filename]`

### Step 4: Save notion-pages.json

1. Write the updated mapping back to `notion-pages.json`
2. Report a summary: total pushed, created, updated

## Rationalizations to Avoid

| Rationalization | Reality |
|---|---|
| "No notion-pages.json, so skip" | Initialize the file and prompt for database_id — skipping silently breaks new-page creation |
| "database_id is empty, just try update" | Missing database_id causes create to fail; surface the error early |
| "The H1 will be picked up automatically" | Always extract and pass the title explicitly — implicit behavior varies by CLI version |
| "Just push the whole file including H1" | The H1 must be stripped from body content; `ntn pages update` renders it as a duplicate heading inside the page |

## Warning Signs

- No result summary after pushing
- notion-pages.json not written before exiting
- Attempting create with an empty database_id
- New pages created without a visible title in Notion

## Verification

- [ ] Every target file was pushed (update or create returned a page_id)
- [ ] `notion-pages.json` updated with any newly created page mappings
- [ ] Newly created pages have the correct title visible in Notion
- [ ] Summary displayed to the user

## Authentication

`ntn login` / keychain auth may not be configured — don't rely on it. Always use the PAT directly:

```bash
# Preferred: inline the token so the command is self-contained
NOTION_API_TOKEN="$(grep NOTION_API_TOKEN ~/.zshrc | cut -d'"' -f2)" ntn pages update ...

# Or source first, then run
source ~/.zshrc && ntn pages update ...
```

The PAT is stored in `~/.zshrc` as `NOTION_API_TOKEN`. If `ntn doctor` shows workspace warnings, that's fine — the PAT still works for API calls.

## ntn api Syntax (for direct API calls)

```bash
# Correct — path first, then -X and -d
ntn api /v1/comments -X POST -d '{"parent": {...}, "rich_text": [...]}'

# Wrong — method before path causes parse error
ntn api POST /v1/comments ...
```

## Error Handling

- If `NOTION_API_TOKEN` is not set, check `~/.zshrc`; if missing, prompt: `export NOTION_API_TOKEN=secret_...`
- If `ntn pages update` returns 404, the integration doesn't have page access — prompt user to share the page with the integration in Notion
- If `ntn api` returns 403, same issue — page not shared with the integration; PAT-based calls bypass this if the PAT owner has access
- If `database_id` is empty, stop and explain how to find the database_id from a Notion page URL
- If no `# Heading` is found in the file, fall back to the filename (without extension) as the title
