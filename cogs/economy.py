import discord
import random
from discord.ext import commands
from database import db  # Ensure database.py exists in your root folder

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your global balance or someone else's."""
        member = member or ctx.author # If no one is mentioned, check own balance
        user_data = db.get_user(member.id)
        
        wallet, bank = user_data[1], user_data[2]
        
        embed = discord.Embed(
            title=f"💰 {member.display_name}'s Global Balance", 
            color=discord.Color.green()
        )
        embed.add_field(name="Wallet", value=f"`${wallet:,}`", inline=True)
        embed.add_field(name="Bank", value=f"`${bank:,}`", inline=True)
        embed.set_footer(text="ServerWideCurrencyBot Template")
        await ctx.send(embed=embed)

    @commands.command(name="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        """Beg for some spare change. 30s cooldown."""
        amount = random.randint(10, 100) # Adds variety for the template
        db.update_wallet(ctx.author.id, amount)
        await ctx.send(f"🪙 A kind stranger gave you **${amount}**!")

    # This handles the "You are on cooldown" message
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Slow down! Try again in **{error.retry_after:.1f}s**.")

async def setup(bot):
    await bot.add_cog(Economy(bot))