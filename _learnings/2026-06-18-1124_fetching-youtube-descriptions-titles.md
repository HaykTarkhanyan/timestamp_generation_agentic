# Fetching YouTube descriptions/titles

`WebFetch` on youtube.com always redirects through `consent.youtube.com` from German IPs (consent flow). The HTML it returns has no actual video data. ALWAYS use yt-dlp's metadata extractor instead:

```python
import yt_dlp
with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
    info = ydl.extract_info(f'https://www.youtube.com/watch?v={vid}', download=False)
    # info['title'], info['description'], info['upload_date'], info['duration'], info['tags']
```

Same for playlists - use `extract_flat=True` to dump video list without downloading each.

Windows console / Git Bash will mangle Armenian/Greek/math glyphs when Python prints to stdout. Two fixes:
- `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` at the top, OR
- Redirect stdout to a file and read it back with `encoding='utf-8'` explicitly.
