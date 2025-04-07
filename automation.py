import os
import subprocess
import schedule
import time
from datetime import datetime

def get_day_of_week():
    # Get the current day of the week (e.g., 'Monday', 'Tuesday', etc.)
    day_of_week = datetime.now().strftime('%A')
    return day_of_week

def git_push():
    repo_path = '/Users/johannesejrskildrejsenhus/Documents/GitHub/automation'  
    day_of_week = get_day_of_week()
    
    # Commit message
    commit_message = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nDay of the Week: {day_of_week}"
    
    try:
        os.chdir(repo_path)
        
        # Append the day of the week to the file
        with open("trending_searches.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {day_of_week}\n")
        
        # Check if there are changes before committing
        status = subprocess.run(["git", "diff", "--exit-code"], capture_output=True)
        if status.returncode == 0:
            print("No changes detected. Skipping commit.")
            return  # No changes, skip commit
        
        # Commit and push the changes
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Successfully pushed to repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

# Schedule the job to run every day at night (e.g., 23:59)
#schedule.every().day.at("23:59").do(git_push)

schedule.every().minute.at(":00").do(git_push)

print("Auto Git Push script running...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking again
