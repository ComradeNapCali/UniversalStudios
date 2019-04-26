from src import UpdateChangelogGetter, UpdateGithubGetter
import discord
import os
import asyncio

CHANNEL = 569398270552702990
client = discord.Client()
changelog_bot = UpdateChangelogGetter.UpdateChangelogGetter()
commit_bot = UpdateGithubGetter.UpdateGithubGetter()

def get_token():
    try:
        with open("DISCORD_TOKEN.txt", 'r') as opened_token:
            readable_token = opened_token.readlines()[0]
            return readable_token
    except:
        return os.getenv('DISCORD_TOKEN')

async def changelog_update_talk():
    update_channel = client.get_channel(CHANNEL)
    changelog_updates = changelog_bot.get_updates()
    if changelog_updates:
        for update in changelog_updates:
            await update_channel.send(update)

async def github_update_talk():
    update_channel = client.get_channel(CHANNEL)
    github_commits = commit_bot.get_commits()
    if github_commits:
        for commit in github_commits:
            await update_channel.send(commit)

@client.event
async def on_ready():
    print('We have logged in as {0.user}! Now logging updates...'.format(client))
    while True:
        await changelog_update_talk()
        await github_update_talk()
        await asyncio.sleep(120) # Because of GitHub's rate limiting, we have to do this here.

client.run(get_token())
