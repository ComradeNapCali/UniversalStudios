from bs4 import BeautifulSoup
import requests
import asyncio

class UpdateChangelogGetter:
    def __init__(self):
        self.TOONIVERSAL_URL = "https://tooniversal.com"
        self.TOONIVERSAL_UPDATE_URL = self.TOONIVERSAL_URL + "/releases"
        self.known_updates = []

    def generate_update_announcement(self, version, release_time, url):
        return "@everyone A new update changelog has just been posted for {} on {}!\nChangelog: {}".format(version, release_time, url)

    def get_updates(self):
        update_list = []
        update_site = requests.get(self.TOONIVERSAL_UPDATE_URL).content
        update_site_contents = BeautifulSoup(update_site, features="html.parser")
        updates = update_site_contents.find_all("a", "post-title-label")
        if not self.known_updates:
            firstTime = True
        else:
            firstTime = False
        for update in updates:
            update_title = update.text
            update_link = update.get('href')
            update_title_list = update_title.split("[")
            update_version = update_title_list[-1][:-1]
            update_release = update_title_list[0][:-1]
            if not (update_version in self.known_updates):
                print("Update {} detected!".format(update_version))
                update_announcement = self.generate_update_announcement(update_version, update_release, self.TOONIVERSAL_URL + update_link)
                if not firstTime:
                    update_list.append(update_announcement)
                self.known_updates.append(update_version)
        return update_list
        
if __name__ == "__main__":
    update_bot = UpdateChangelogGetter()
    update_bot.get_updates()
