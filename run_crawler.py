from repo_crawler_5000 import GitHubCrawler

if __name__ == "__main__":
    # Create an instance of GitHubCrawler
    crawler = GitHubCrawler(db_path='db.sqlite')

    try:
        # Get and save the top 100 repositories (or any number you want)
        repositories = crawler.get_top_repositories(count=1)  # Fetch 1 page (approximately 100 repositories)
        crawler.save_repositories(repositories)

        print(f"Successfully processed {len(repositories)} repositories")
    finally:
        # Make sure to close the connection
        crawler.close()