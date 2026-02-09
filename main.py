import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

VERSION = "1.1.0" # 1 (Initial Release) . 1 (Banking/Robbing Update) . 0 (No patches yet)

# Load environment variables (the .env file)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Required for reading commands

class CurrencyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # This automatically loads every .py file in the /cogs folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: {filename}')

    @bot.event
    async def on_ready():
        print(f'--- GlobEx Global Economy ---')
        print(f'Logged in as {bot.user.name}')
        print(f'Version: {VERSION}')
        print(f'-----------------------------')

bot = CurrencyBot()

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())