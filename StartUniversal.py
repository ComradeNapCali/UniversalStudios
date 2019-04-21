from src import UpdateChangelogGetter, UpdateGithubGetter
import discord
import asyncio

CHANNEL = 569390684440625172
client = discord.Client()
changelog_bot = UpdateChangelogGetter.UpdateChangelogGetter()
commit_bot = UpdateGithubGetter.UpdateGithubGetter()

def get_token():
    with open("DISCORD_TOKEN.txt", 'r') as opened_token:
        readable_token = opened_token.readlines()[0]
        return readable_token

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
        await asyncio.sleep(10)

client.run(get_token())