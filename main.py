import discord
import json

from discord.ext import commands

from config.settings import DISCORD_TOKEN

bot = commands.Bot(command_prefix=">")


async def create_account(*, user):
    """
    Open an account for a user
    Save account details in json file
    """
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {"wallet": 0, "bank": 0}
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


def has_account(user):
    with open("mainbank.json", "r") as f:
        users = json.load(f)

        if str(user.id) in users:
            return True
        else:
            return False


@bot.event
async def on_ready():
    print("Ready")


@bot.command()
async def balance(ctx):
    """
    Check balance for a certain user
    """
    if has_account(user=ctx.author):
        with open("mainbank.json", "r") as f:
            users = json.load(f)
            await ctx.send(f'Your balance is {users[str(ctx.author.id)]["wallet"]}')
    else:
        await ctx.send("You do not have a balance")


@bot.command()
async def register(ctx):
    if not has_account(ctx.author):
        await create_account(user=ctx.author)
    else:
        await ctx.send("You are already registered")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
