# GitHub Repository Crawler

A Python tool that crawls GitHub repositories ranked by stars and stores repository information in a SQLite database.   
Currently only get repotitories name and owner name   
Future: Add more repository details (e.g., commits, releases)
## Features

- Fetches top repositories from [GitStar Ranking](https://gitstar-ranking.com/)
- Stores repository data in SQLite database
- Tracks commits and releases for each repository
- Simple database schema for easy querying

## Installation

```bash
pip install -r requirements.txt
```

## Example usage in run_crawler.py

```python
from repo_crawler_5000 import GitHubCrawler

# Create a crawler instance
crawler = GitHubCrawler(db_path='db.sqlite')

# Get top 5 pages of repositories (500 repo - 100 each page)
repos = crawler.get_top_repositories(5)

# Save repositories to database
saved_repos = crawler.save_repositories(repos)

# Close database connection
crawler.close()
```

## Database Schema

- `repositories`: Stores basic repository information (user, name)
- `releases`: Tracks release information for each repository
- `commits`: Stores commit data associated with releases

## Requirements

- Python 3.6+
- requests
- BeautifulSoup4
- sqlite3

## License

MIT
