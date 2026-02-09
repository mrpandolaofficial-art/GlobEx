import discord
import random
from discord.ext import commands
from database import db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your global balance or someone else's."""
        member = member or ctx.author
        user_data = db.get_user(member.id)
        wallet, bank = user_data[1], user_data[2]
        
        embed = discord.Embed(title=f"💰 {member.display_name}'s Balance", color=discord.Color.green())
        embed.add_field(name="Wallet", value=f"`${wallet:,}`", inline=True)
        embed.add_field(name="Bank", value=f"`${bank:,}`", inline=True)
        embed.set_footer(text="GlobEx — Global Economy")
        await ctx.send(embed=embed)

    @commands.command(name="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        amount = random.randint(10, 100)
        db.update_wallet(ctx.author.id, amount)
        await ctx.send(f"🪙 A kind stranger gave you **${amount}**!")

    @commands.command(name="work")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        jobs = ["Software Developer", "Digital Artist", "Burger Flipper", "Discord Mod"]
        job = random.choice(jobs)
        pay = random.randint(500, 1500)
        db.update_wallet(ctx.author.id, pay)
        await ctx.send(f"💼 You worked as a **{job}** and earned **${pay:,}**!")

    @commands.command(name="pay", aliases=["send"])
    async def pay(self, ctx, member: discord.Member, amount: int):
        if member.id == ctx.author.id: return await ctx.send("❌ You can't pay yourself!")
        if amount <= 0: return await ctx.send("❌ You must pay at least $1.")
        
        sender_data = db.get_user(ctx.author.id)
        if sender_data[1] < amount: return await ctx.send("❌ Insufficient funds!")

        db.update_wallet(ctx.author.id, -amount)
        db.update_wallet(member.id, amount)
        await ctx.send(f"✅ Sent **${amount:,}** to **{member.display_name}**!")

    @commands.command(name="slots")
    async def slots(self, ctx, amount: int):
        user_data = db.get_user(ctx.author.id)
        if user_data[1] < amount: return await ctx.send("❌ Insufficient funds!")
        if amount <= 0: return await ctx.send("❌ Bet at least $1.")

        emojis = "🍎🍊🍇💎"
        result = [random.choice(emojis) for _ in range(3)]
        machine = " | ".join(result)

        if len(set(result)) == 1:
            winnings = amount * 5
            db.update_wallet(ctx.author.id, winnings)
            await ctx.send(f"🎰 **{machine}** 🎰\nJACKPOT! You won **${winnings:,}**!")
        elif len(set(result)) == 2:
            winnings = amount * 2
            db.update_wallet(ctx.author.id, winnings)
            await ctx.send(f"🎰 **{machine}** 🎰\nNice! You won **${winnings:,}**!")
        else:
            db.update_wallet(ctx.author.id, -amount)
            await ctx.send(f"🎰 **{machine}** 🎰\nLost **${amount:,}**.")

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        top_users = db.get_leaderboard()
        description = ""
        for i, (user_id, total) in enumerate(top_users, start=1):
            # Try to get from cache first
            user = self.bot.get_user(user_id)
            
            # If not in cache, try to fetch from Discord API
            if user is None:
                try:
                    user = await self.bot.fetch_user(user_id)
                except:
                    user = None

            name = user.display_name if user else f"Unknown ({user_id})"
            description += f"**{i}. {name}** — ${total:,}\n"

        embed = discord.Embed(
            title="🌍 Global Leaderboard", 
            description=description, 
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx, amount: str):
        """Move money from your wallet to your bank."""
        user_data = db.get_user(ctx.author.id)
        wallet = user_data[1]

        if amount.lower() == "all":
            amount = wallet
        else:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send("❌ Please enter a valid number or 'all'.")

        if amount <= 0: return await ctx.send("❌ You can't deposit nothing!")
        if wallet < amount: return await ctx.send("❌ You don't have that much in your wallet!")

        db.deposit(ctx.author.id, amount)
        await ctx.send(f"🏦 Deposited **${amount:,}** into your bank!")

    @commands.command(name="withdraw", aliases=["with"])
    async def withdraw(self, ctx, amount: str):
        """Move money from your bank to your wallet."""
        user_data = db.get_user(ctx.author.id)
        bank = user_data[2]

        if amount.lower() == "all":
            amount = bank
        else:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send("❌ Please enter a valid number or 'all'.")

        if amount <= 0: return await ctx.send("❌ You can't withdraw nothing!")
        if bank < amount: return await ctx.send("❌ You don't have that much in your bank!")

        db.withdraw(ctx.author.id, amount)
        await ctx.send(f"💵 Withdrew **${amount:,}** from your bank!")

    @commands.command(name="rob")
    @commands.cooldown(1, 300, commands.BucketType.user) # 5-minute cooldown
    async def rob(self, ctx, member: discord.Member):
        """Try to steal money from another user's wallet!"""
        if member.id == ctx.author.id:
            return await ctx.send("❌ You can't rob yourself. That's just moving money between pockets.")

        # Get balances
        robber_data = db.get_user(ctx.author.id)
        victim_data = db.get_user(member.id)
        
        victim_wallet = victim_data[1]
        
        if victim_wallet < 200:
            return await ctx.send(f"❌ **{member.display_name}** is too poor to rob. Leave them alone!")

        # Success chance (40% success)
        chance = random.randint(1, 10)
        
        if chance <= 4:
            # Success! Steal between 20% and 100% of their wallet
            stolen = random.randint(int(victim_wallet * 0.2), victim_wallet)
            db.update_wallet(ctx.author.id, stolen)
            db.update_wallet(member.id, -stolen)
            await ctx.send(f"🥷 **SUCCESS!** You robbed **{member.display_name}** and got away with **${stolen:,}**!")
        else:
            # Failure! Pay a fine to the victim
            fine = random.randint(100, 500)
            db.update_wallet(ctx.author.id, -fine)
            db.update_wallet(member.id, fine)
            await ctx.send(f"🚔 **BUSTED!** You were caught trying to rob **{member.display_name}** and paid a **${fine}** fine to them!")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = int(error.retry_after // 60)
            seconds = int(error.retry_after % 60)
            await ctx.send(f"⏳ The heat is still on! Wait **{minutes}m {seconds}s** before robbing again.")

# No decorator needed here! 
    # This is a built-in function that discord.py looks for automatically.
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Slow down! Try again in **{error.retry_after:.1f}s**.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing information! Check the command usage.")
        else:
            print(f"Error in Cog: {error}")

async def setup(bot):
    await bot.add_cog(Economy(bot))