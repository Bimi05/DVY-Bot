import discord
from discord.ext import commands

class LookingForGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def push(self, ctx, rank=None, *, message=None):
        if ctx.channel.id == 767090495540822036:
            if not rank:
                await ctx.command.reset_cooldown(ctx)
                return await ctx.send("Please mention a rank to push.")

            ranks = {"r20": 985550287542562927, "r25": 767122614106849280, "r30": 767122780835282944, "r35": 767122869255536682}
            role_id = ranks.get(rank.lower())
            if role_id:
                push_role = discord.utils.get(ctx.guild.roles, id=role_id)
                if push_role in ctx.author.roles:
                    pushing = f"{push_role.mention}: {ctx.author.mention} is looking for a teammate to push!"
                    if message:
                        pushing += f"\nMessage provided: **{message}**"
                    await ctx.message.delete()
                    return await ctx.send(pushing, allowed_mentions=discord.AllowedMentions(roles=True))
                await ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"You need the {push_role.mention} role to use this command.")
            await ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"The available ranks to ping and push are: {', '.join(ranks.keys())}.")
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#767090495540822036>.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def league(self, ctx, league=None, *, message=None):
        if ctx.channel.id == 767089540639752192:
            if league is None:
                return await ctx.send("Please mention a league to push.")

            leagues = {"bronze": 849625503212240916, "silver": 849625566415683645, "gold": 849625660607299584, "diamond": 849625733257101343, "mythic": 849625844851015740, "legendary": 849625926512672808, "master": 849626058554605658}
            league_id = leagues.get(league.lower())
            if league_id:
                league_role = discord.utils.get(ctx.guild.roles, id=league_id)
                if league_role in ctx.author.roles:
                    league_push = f"{league_role.mention}: {ctx.author.mention} is looking for a teammate to push in PL!"
                    if message:
                        league_push += f"\nMessage provided: **{message}**"
                    await ctx.message.delete()
                    return await ctx.send(league_push, allowed_mentions = discord.AllowedMentions(roles=True))
                await ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"You need the {league_role.mention} role to use this command.")
            await ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"The available leagues to push to are: {', '.join(leagues.keys())}.")
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#767089540639752192>.")

    @commands.command(aliases=("weekendevents", "we"))
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def weekend(self, ctx, *, message=None):
        if ctx.channel.id == 767089586970034187:
            weekend_event = f"{discord.utils.get(ctx.guild.roles, id=767097985501888543).mention}: {ctx.author.mention} is looking for a teammate to do this weekend event!"
            if message:
                weekend_event += f"\nMessage Provided: **{message}**"
            await ctx.message.delete()
            return await ctx.send(weekend_event, allowed_mentions=discord.AllowedMentions(roles=True))
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#767089586970034187>.")

    @commands.command(name="1v1")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def onevone(self, ctx, *, message=None):
        if ctx.channel.id == 810510255138144296:
            x1v1 = f"{discord.utils.get(ctx.guild.roles, id=792062568805433345).mention}: {ctx.author.mention} is looking for an opponent to 1v1!"
            if message:
                x1v1 += f"\nMessage Provided: **{message}**"
            await ctx.message.delete()
            return await ctx.send(x1v1, allowed_mentions=discord.AllowedMentions(roles=True))
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#810510255138144296>.")

    @commands.command(aliases=("cc", "championship"))
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def champ(self, ctx, *, message=None):
        if ctx.channel.id == 810485897321644053:
            championship = f"{discord.utils.get(ctx.guild.roles, id=809399188378353726).mention}: {ctx.author.mention} is looking for a teammate to do the championship!"
            if message:
                championship += f"\nMessage Provided: **{message}**"
            await ctx.message.delete()
            return await ctx.send(championship, allowed_mentions=discord.AllowedMentions(roles=True))
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#810485897321644053>.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def scrims(self, ctx, *, message=None):
        if ctx.channel.id == 839865005511671808:
            scrim = f"{discord.utils.get(ctx.guild.roles, id=839866655018057768).mention}: {ctx.author.mention} is looking for a scrim!"
            if message:
                scrim += f"\nMessage Provided: **{message}**"
            await ctx.message.delete()
            return await ctx.send(scrim, allowed_mentions=discord.AllowedMentions(roles=True))
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#839865005511671808>.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def quests(self, ctx, *, message=None):
        if ctx.channel.id == 851064466803130408:
            quest = f"{discord.utils.get(ctx.guild.roles, id=849643821398228992).mention}: {ctx.author.mention} is looking for a teammate to do quests!"
            if message:
                quest += "\nMessage Provided: **{message}**"
            await ctx.message.delete()
            return await ctx.send(quest, allowed_mentions=discord.AllowedMentions(roles=True))
        await ctx.command.reset_cooldown(ctx)
        await ctx.send("This command can only be used in <#851064466803130408>.")


def setup(client):
    client.add_cog(LookingForGames(client))
