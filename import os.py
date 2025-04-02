import os
import subprocess
import schedule
import time
from datetime import datetime
import requests

def get_trending_search():
    try:
        response = requests.get("https://trends.google.com/trends/trendingsearches/daily?geo=US")
        if response.status_code == 200:
            return response.text[:100]  # Store only a snippet for now
        else:
            return "No trending search data available"
    except Exception as e:
        return f"Error fetching trends: {e}"

def git_push():
    repo_path = "/path/to/your/repo"  # Change this to your repo path
    trending_search = get_trending_search()
    commit_message = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nTrending: {trending_search}"
    
    try:
        os.chdir(repo_path)
        with open("trending_searches.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {trending_search}\n")
        
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Successfully pushed to repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

# Schedule the job to run every day at night (e.g., 23:59)
schedule.every().day.at("23:59").do(git_push)

print("Auto Git Push script running...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking again