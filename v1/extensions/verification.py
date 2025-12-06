import discord

from const import DVY_ID, NAMES, STATS
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_role(782266411447091200)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def update(self, ctx, name, *members: discord.Member):
        if ctx.guild.id == DVY_ID:
            if not members:
                members = (ctx.author,)

            for member in members:
                unverified = discord.utils.get(member.roles, id=737151174465028126)
                if unverified and ctx.channel.id == 850863329073561610:
                    for key, value in NAMES.items():
                        if name.lower() == key:
                            role = discord.utils.get(ctx.guild.roles, id=value["id"])
                            channel = self.client.get_channel(706633062414548992)

                            await member.edit(nick=value["nickname"].format(member.display_name))
                            await member.add_roles(role)
                            await member.remove_roles(unverified)
                            await channel.send(content=member.mention, embed=discord.Embed(title=f"Welcome `{member.display_name}`!", description="Please make sure to read <#758814247437860934> and assign your roles in the <#725868495388278785> channel in order to get access to the relevant channels. If you would like more information about our tournament's, then please read <#771398498943238185>. Anyone can sign up for the tournaments 😊. If you need help or have questions you can ask in general chat or DM <@575252669443211264>. Enjoy your stay!", colour=role.colour))
                            break
                else:
                    for key, value in NAMES.items():
                        if name.lower() == key:
                            role_to_add = discord.utils.get(ctx.guild.roles, id=value["id"])
                            role_to_remove = None
                            for param in NAMES:
                                role_to_remove = discord.utils.get(member.roles, id=NAMES[param]["id"])
                                if role_to_remove:
                                    await member.remove_roles(role_to_remove)
                                    break

                            if role_to_add.id == role_to_remove.id:
                                return await ctx.message.add_reaction("<:RedTick:800399301980323840>")

                            if role_to_remove.id == 762393947594293248:
                                await member.edit(nick=value["nickname"].format(member.display_name))
                            else:
                                await member.edit(nick=value["nickname"].format(member.display_name[5:-6]))
                            await member.add_roles(role_to_add)
                            break

            if name.lower() in NAMES:
                await ctx.message.add_reaction(NAMES[name.lower()]["emoji"])

    @commands.command()
    @commands.has_role(782266411447091200)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ustats(self, ctx, member: discord.Member, *, role):
        if ctx.guild.id == DVY_ID:
            member = member or ctx.author
            to_add = []
            for item in role.replace(" ", "").lower().split("/"):
                for thing in STATS:
                    if item in thing:
                        for key, value in thing.items():
                            if key == item:
                                role_to_add = discord.utils.get(ctx.guild.roles, id=value)
                                if role_to_add not in to_add:
                                    to_add.append(role_to_add)
                                    break

                        for key, value in thing.items():
                            r = discord.utils.get(member.roles, id=value)
                            if r is not None:
                                await member.remove_roles(r)

            if to_add:
                for item in to_add:
                    await member.add_roles(item)
                return await ctx.send(f"`{member.display_name}` has been granted the {', '.join([f'`{item.name}`' for item in to_add])} {'role' if len(to_add) == 1 else 'roles'}.")
            await ctx.message.add_reaction("<:RedTick:800399301980323840>")


    @commands.command()
    @commands.has_role(782266411447091200)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def verify(self, ctx):
        if ctx.guild.id == DVY_ID:
            if ctx.channel.id == 850863329073561610:
                await ctx.message.delete()
                await ctx.channel.purge(limit=1000, check=lambda i: not i.pinned)
                return await ctx.send(embed=discord.Embed(title="Welcome to Diversity!", description="**__To verify:__**\n__Post a screenshot containing your name highlighted in your club list, just like the example below!__\n> **If you aren't in any club, send a screenshot of the global or local leaderboards!**", colour=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif").set_image(url="https://cdn.discordapp.com/attachments/782256108449693696/970810968869318716/6DF91AD3-EEC7-4E90-9CDF-87D2CB1890D5.png"))
            await ctx.message.add_reaction("<:RedTick:800399301980323840>")


def setup(client):
    client.add_cog(Verification(client))
