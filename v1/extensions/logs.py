import aiosqlite
import aiohttp
import asyncio
import discord
import json

from discord.ext import commands

class Logs(commands.Cog):
    logs_memo = {}

    def __init__(self, client: commands.Bot):
        self.client = client
        self._session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    async def get_logs_for(self, tag):
        async with self._session.get(f"https://api.brawlapi.com/v1/clublog/{tag}", headers={"User-Agent": "Diversity Bot/Club Logs"}) as session:
            try:
                resp = json.loads(await session.text())
            except (TypeError, json.JSONDecodeError):
                resp = await session.text()
        return resp

    async def get_log_from_mode(self, mode):
        player_joined = discord.Embed()
        player_left = discord.Embed()
        player_promoted = discord.Embed()
        player_demoted = discord.Embed()
        description_changed = discord.Embed()
        req_trophies_changed = discord.Embed()
        type_changed = discord.Embed()

        match = {
            "join": player_joined,
            "leave": player_left,
            "promote": player_promoted,
            "demote": player_demoted,
            "desc": description_changed,
            "req": req_trophies_changed,
            "type": type_changed
        }

        try:
            log = match[mode]
        except KeyError:
            return None
        else:
            return log


    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def logadd(self, ctx, tag, channel: discord.TextChannel = None):
        tag = tag.strip().strip("#").upper()
        inv = [char for char in tag if char not in set("0289PYLQGRJCUV")]
        if inv:
            return await ctx.send("Please ensure the tag provided is a **valid** in-game club tag.\nInvalid characters: {}".format(", ".join(inv)))

        #* info and items
        channel = channel or ctx.channel
        async with aiosqlite.connect("main.db") as main:
            async with main.execute("") as cursor:
                res = {item[0] for item in await cursor.fetchall()}

            if tag in res:
                await ctx.message.add_reaction("<:RedTick:800399301980323840>")
            else:
                await main.execute("INSERT INTO logs(tag, channel_id) VALUES(?, ?)", (tag, channel.id))
                await main.commit()

        res = await self.get_logs_for(tag)
        # logs = self.logs_memo.setdefault(tag, res["history"])
        # if logs != res["history"]:
        #     to_log = [item for item in res["history"] if item not in logs]

        log_success = discord.Embed(title="Club Log Registration Successful!", description=f"{res['club']['name']}'s logs are now being tracked.\nAny changes will be posted to {channel.mention}!", colour=0x2ecc71)
        await ctx.send(embed=log_success)

    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def logremove(self, ctx, tag):
        async with aiosqlite.connect("main.db") as main:
            await main.execute("")
        await ctx.send("<a:loading:771414970637877248> work in progress...")

    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def logs(self, ctx):
        await ctx.send("<a:loading:771414970637877248> work in progress...")


def setup(client):
    client.add_cog(Logs(client))
