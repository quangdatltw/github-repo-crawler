import requests
import sqlite3
from bs4 import BeautifulSoup

class GitHubCrawler:

    def __init__(self, db_path='db.sqlite'):
        self.github_star_url = "https://gitstar-ranking.com/repositories?page="
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        print(f"Connected to database: {db_path}")

    def create_tables(self):
        cursor = self.conn.cursor()

        # Drop existing tables if they exist
        cursor.execute('DROP TABLE IF EXISTS commits;')
        cursor.execute('DROP TABLE IF EXISTS releases;')
        cursor.execute('DROP TABLE IF EXISTS repositories;')

        # Create `repositories` table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                name TEXT NOT NULL
            );
        ''')

        # Create `releases` table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS releases (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                repoID INTEGER NOT NULL,
                FOREIGN KEY (repoID) REFERENCES repositories (id)
            );
        ''')

        # Create `commits` table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commits (
                hash TEXT NOT NULL,
                message TEXT NOT NULL,
                releaseID INTEGER NOT NULL,
                FOREIGN KEY (releaseID) REFERENCES releases (id)
            );
        ''')

        self.conn.commit()
        print("Tables have been recreated - all previous data has been deleted")

    def get_top_repositories(self, count):
        repositories = []

        for page in range(1, count + 1):
            url = f"{self.github_star_url}{page}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find all repository items in the list
                repo_items = soup.select('.list-group-item.paginated_item')

                for item in repo_items:
                    repo_href = item.get('href', '')
                    if repo_href.startswith('/'):
                        repo_href = repo_href[1:]

                    if '/' in repo_href:
                        user, name = repo_href.split('/', 1)

                        repositories.append({
                            "user": user,
                            "name": name,
                        })
                        print(user, name)

            else:
                print(f"Error when fetched from {url}: {response.status_code}")
                break

        print(f"Fetched {len(repositories)} repositories from {self.github_star_url} to {self.db_path}")
        return repositories

    def save_repositories(self, repositories):
        if not repositories:
            return []

        cursor = self.conn.cursor()
        saved_repos = []

        for repo in repositories:
            cursor.execute('''
                INSERT INTO repositories (user, name)
                VALUES (?, ?)
            ''', (
                repo["user"],
                repo["name"]
            ))

            # Get ID of the repository just added
            repo_id = cursor.lastrowid

            # Save repository info and ID for later use
            saved_repos.append({
                "id": repo_id,
                "user": repo["user"],
                "name": repo["name"],
            })

        self.conn.commit()
        print(f"Saved {len(repositories)} repositories to database")
        return saved_repos

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")