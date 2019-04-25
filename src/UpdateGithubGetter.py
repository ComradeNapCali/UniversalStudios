import requests
import json

class UpdateGithubGetter:
    def __init__(self):
        self.REPO_NAME = "TCOperations/releases"
        self.REPO_URL = "https://github.com/{}"
        self.API_URL = "https://api.github.com/repos/{}/events"
        self.known_commits = []

    def generate_commit_announcement(self, url, head):
        return "@everyone A new commit was just pushed to the release repo!\nCommit: {}\nSHA: {}".format(url, head)

    def get_commit_url(self, head):
        return "{}/commit/{}".format(self.REPO_URL.format(self.REPO_NAME), head)

    def get_commits(self):
        commit_list = []
        api_site = requests.get(self.API_URL.format(self.REPO_NAME)).json()
        if not self.known_commits:
            firstTime = True
        for commits in api_site:
            commit_id = commits["id"]
            if not (commit_id in self.known_commits):
                print("Commit {} detected!".format(commit_id))
                self.known_commits.append(commit_id)
                commit_head = commits["payload"]["head"]
                commit_url = self.get_commit_url(commit_head)
                commit_announcement = self.generate_commit_announcement(commit_url, commit_head)
                if not firstTime:
                    commit_list.append(commit_announcement)
        return commit_list

if __name__ == "__main__":
    update_bot = UpdateGithubGetter()
    print(update_bot.get_commits())