import aiosqlite
import discord
import bstats

from const import DVY_ID, LEAGUES, STAFF, NAMES
from discord.ext import commands, tasks
from discord.ui import View, Button, Select

class Administration(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.api = bstats.Client(open("./tokens/bs_api.txt", "r", encoding="UTF-8").readline())

    def filter_tag(self, tag):
        tag = tag.strip().upper()
        for char in tag:
            if char not in "#0289PYLQGRJCUV":
                return -1
        return tag

    async def get_clubs(self):
        async with aiosqlite.connect("main.db") as main:
            async with main.execute("SELECT * FROM clubs") as cur:
                res = await cur.fetchall()
                tags = [item[0] for item in res]

            club_c, member_c, trophy_c = 0, 0, 0
            trophies, details = [], []

            for club_tag in tags:
                c = await self.api.get_club(club_tag)

                club_c += 1
                member_c += len(c.members)
                trophy_c += c.trophies

                trophies.append(c.trophies)
                details.append((c.name, c.tag, c.required_trophies, len(c.members), c.type))

            info = {}
            for item in sorted(tuple(zip(trophies, details)), reverse=True):
                info[item[1][1]] = {
                    "name": item[1][0],
                    "trophies": f"<:Trophy:819862621502308402> {item[0]}",
                    "req": f"<:SilverTrophy:911605011828604928> {item[1][2]}",
                    "members": f"<:Club:819862621209493504> {item[1][3]}",
                    "_type": f"<:Info:819862620861104130> {item[1][4]}"
                }

            total = []
            head_embed = discord.Embed(title="Diversity Clubs", colour=0x01bb70)
            head_embed.add_field(name="Total Clubs", value=f"<:Club:819862621209493504> {club_c}")
            head_embed.add_field(name="Total Trophies", value=f"<:Trophy:819862621502308402> {trophy_c:,}".replace(",", " "))
            head_embed.add_field(name="Total Members", value=f"<:Info:819862620861104130> **{member_c}**/{club_c * 30}")
            head_embed.set_thumbnail(url="https://imgur.com/GlZttyo.gif")
            total.append((head_embed, None))

            counter, LIMIT = 0, 15
            embed = discord.Embed(title="Diversity Clubs", colour=0x01bb70).set_thumbnail(url="https://imgur.com/GlZttyo.gif").set_footer(icon_url="https://imgur.com/GlZttyo.gif", text="If you'd like to apply to any of these clubs, please select them in the dropdown below!")

            dropdown = Select(custom_id="club_viewer", placeholder="Select club to apply to...")
            options_list = []
            for tag, details in info.items():
                # if int(details["trophies"].split()[-1]) > 500000: #* filters out <500k club trophy clubs (9/1/2024 - useless)
                embed.add_field(name=f"{details['name']}\n({tag})", value=f"**{details['trophies']}**\n**{details['req']}**\n**{details['members']}**/30\n**{details['_type']}**\n\u200b")
                emoji_name = details["name"].lower().split()
                emoji = emoji_name[0].strip().replace("'", "").replace("’", "")
                if not emoji.endswith("s"):
                    emoji += "s"

                #! update emoji config first and then re-enable this
                # try:
                #     emm = NAMES[emoji]
                # except KeyError:
                #     continue
                # else:
                #     options_list.append(discord.SelectOption(label=f"{details['name']} ({tag})", value=tag, emoji=emm["emoji"]))
                options_list.append(discord.SelectOption(label=f"{details['name']} ({tag})", value=tag))
                counter += 1
                if counter == LIMIT:
                    counter = 0
                    dropdown.options = options_list
                    options_list = []
                    total.append((embed, dropdown))
                    dropdown = Select(custom_id="club_viewer", placeholder="Select club to apply to...")
                    embed = discord.Embed(title="Diversity Clubs", colour=0x01bb70).set_thumbnail(url="https://imgur.com/GlZttyo.gif").set_footer(icon_url="https://imgur.com/GlZttyo.gif", text="If you'd like to apply to any of these clubs, please select them in the dropdown below!")
            else:
                if embed not in total:
                    dropdown.options = options_list
                    options_list = []
                    total.append((embed, dropdown))

            return total

    async def set_club_application(self, dropdown):
        async def app(inter):
            club = await self.api.get_club(inter.data["values"][0])
            roles = {"Member": [], "Senior": [], "Vice President": [], "President": []}
            for member in club.members:
                for key, value in LEAGUES.items():
                    if key < member.trophies:
                        tr_badge = value
                roles.get(member.role).append(f"{tr_badge} `{member.trophies}` - **{member.name}**")

            cl = discord.Embed(title=f"{club.name} Overview\n({club.tag})", colour=0x01bb70)
            cl.add_field(name="Total trophies", value=f"<:Trophy:819862621502308402> {club.trophies}", inline=False)
            cl.add_field(name="Required trophies", value=f"<:SilverTrophy:911605011828604928> {club.required_trophies}", inline=False)
            cl.add_field(name="Member count", value=f"<:Club:819862621209493504> **{len(club.members)}**/30", inline=False)
            cl.add_field(name="Club type", value=f"<:Info:819862620861104130> {club.type}", inline=False)
            cl.add_field(name="Description", value=f"`{club.description}`", inline=False)
            cl.add_field(name=f"Top Members (Total: {len(roles['Member'])})", value="\n".join(roles['Member'][:5]), inline=False)
            if roles["Senior"]:
                cl.add_field(name=f"Top Seniors (Total: {len(roles['Senior'])})", value="\n".join(roles['Senior'][:5]), inline=False)
            if roles["Vice President"]:
                cl.add_field(name=f"Top Vice Presidents (Total: {len(roles['Vice President'])})", value="\n".join(roles['Vice President'][:5]), inline=False)
            cl.add_field(name="President", value=roles["President"][0], inline=False)

            async def confirm(inter):
                await inter.response.send_message("Please check your DMs.", ephemeral=True)
                await inter.user.send("Please provide a screenshot of your profile like this:")
                await inter.user.send("https://cdn.discordapp.com/attachments/769531283655098368/989643271376601108/IMG_1282.png")

                attachment_msg = await self.client.wait_for("message", check=lambda i: i.author.id == inter.user.id, timeout=None)
                while not attachment_msg.attachments:
                    await inter.user.send("Please ensure that you provide the screenshot as an attachment.")
                    attachment_msg = await self.client.wait_for("message", check=lambda i: i.author.id == inter.user.id, timeout=None)
                pres_chat = await self.client.fetch_channel(782294461199286302)
                await pres_chat.send(f"A new member would like to join **{club.name}**!\nThis is their profile.\n\nTheir Discord is: {inter.user.mention}\n**Please alert the club's owner to get in contact with the member about joining!**", file=await attachment_msg.attachments[0].to_file())
                await inter.edit_original_message(view=None)
                await inter.followup.send(f"{inter.user.mention} Your application was sent successfully!", ephemeral=True)

            async def deny(inter):
                await inter.response.edit_message(view=None)
                await inter.followup.send("Process Cancelled!", ephemeral=True)

            apply_con = Button(style=discord.ButtonStyle.green, label="Apply", emoji="<:GreenTick:800399486501257216>", custom_id="apply_to_club")
            apply_con.callback = confirm

            apply_deny = Button(style=discord.ButtonStyle.red, label="Cancel", emoji="<:RedTick:800399301980323840>", custom_id="deny_application")
            apply_deny.callback = deny

            view = View(apply_con, apply_deny, timeout=300)
            await inter.response.send_message(content="Here are the club's stats\nPlease click on the \"Apply\" button if you wish to confirm your application.", embed=cl, view=view, ephemeral=True)
            if await view.wait():
                await inter.edit_original_message(view=None)
        dropdown.callback = app


    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.refresh_clubs.start()

    @tasks.loop(minutes=30)
    async def refresh_clubs(self):
        async with aiosqlite.connect("main.db") as main:
            async with main.execute("SELECT * FROM club_embeds") as cursor:
                ids = await cursor.fetchall()

            if ids:
                total = await self.get_clubs()
                total.pop(0)
                our_clubs = await self.client.fetch_channel(735917551703556136)
                for i, msg_id in enumerate(ids):
                    await self.set_club_application(total[i][1])
                    view = View(total[i][1], timeout=None)
                    self.client.add_view(view, message_id=msg_id[0])

                    m = await our_clubs.fetch_message(msg_id[0])
                    await m.edit(embed=total[i][0], view=view)

    @refresh_clubs.before_loop
    async def before_refresh_clubs(self):
        await self.client.wait_until_ready()


    @commands.command()
    @commands.has_any_role(840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def promote(self, ctx, member: discord.Member, *, role=None):
        if ctx.guild.id == DVY_ID:
            if member == ctx.author:
                return await ctx.message.add_reaction("<:RedTick:800399301980323840>")

            async with aiosqlite.connect("main.db") as main:
                async with main.execute("SELECT * FROM roster") as cursor:
                    from callbacks import roster

                    roster_id = await cursor.fetchone()
                    chn = await self.client.fetch_channel(796828098631827536)
                    ros = await chn.fetch_message(roster_id[0])

            staff_team = discord.utils.get(ctx.guild.roles, id=782266411447091200)
            verification_staff = discord.utils.get(ctx.guild.roles, id=STAFF["verification staff"])
            if role is None:
                seen = {}
                for key, value in STAFF.items():
                    temp = discord.utils.get(ctx.guild.roles, id=value)
                    seen[temp.id] = False
                    if temp in member.roles:
                        seen[temp.id] = True

                if any(seen.values()):
                    items = [(key, value) for key, value in seen.items()]
                    for num, thing in enumerate(items[::-1]):
                        if thing[1]:
                            role_to_add = discord.utils.get(ctx.guild.roles, id=items[::-1][num-1][0])
                            break
                else:
                    role_to_add = verification_staff

                if role_to_add.name.lower() != "administrator":
                    if staff_team not in member.roles:
                        await member.add_roles(staff_team, reason=f"Promoted by {ctx.author}.")
                    await member.add_roles(role_to_add, reason=f"Promoted by {ctx.author}.")
                    resp = await roster(self.client)
                    await ros.edit(embed=resp[0])
                    return await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
                await ctx.message.add_reaction("<:RedTick:800399301980323840>")
            else:
                for key, value in STAFF.items():
                    if key == role.lower():
                        role_to_add = discord.utils.get(ctx.guild.roles, id=value)

                    if role_to_add.name.lower() != "administrator":
                        if role_to_add in member.roles:
                            return await ctx.send(f"**{member}** already has the {role_to_add.mention} role!")

                        if staff_team not in member.roles:
                            await member.add_roles(staff_team, reason=f"Promoted by {ctx.author}.")
                        await member.add_roles(role_to_add, reason=f"Promoted by {ctx.author}.")
                        resp = await roster(self.client)
                        await ros.edit(embed=resp[0])
                        return await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
                    await ctx.message.add_reaction("<:RedTick:800399301980323840>")

    @commands.command()
    @commands.has_any_role(840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def demote(self, ctx, member: discord.Member, *, role=None):
        if ctx.guild.id == DVY_ID:
            if member == ctx.author:
                return await ctx.message.add_reaction("<:RedTick:800399301980323840>")

            async with aiosqlite.connect("main.db") as main:
                async with main.execute("SELECT * FROM roster") as cursor:
                    from callbacks import roster

                    roster_id = await cursor.fetchone()
                    chn = await self.client.fetch_channel(796828098631827536)
                    ros = await chn.fetch_message(roster_id[0])

            staff_team = discord.utils.get(ctx.guild.roles, id=782266411447091200)
            if not role:
                seen = {}
                for key, value in STAFF.items():
                    r = discord.utils.get(ctx.guild.roles, id=value)
                    seen[r.id] = False
                    if r in member.roles:
                        seen[r.id] = True

                temp = [val for val, item in seen.items() if item == True]
                staff_ids = [staff_role_id for staff_role_id in STAFF.values()]
                role_to_remove = discord.utils.get(member.roles, id=temp[-1])
                if len(temp) >= 2:
                    for num, val in enumerate(staff_ids[::-1]):
                        if staff_ids[::-1][num] == temp[-1]:
                            role_to_add = discord.utils.get(ctx.guild.roles, id=staff_ids[::-1][num+1])
                            if role_to_add not in member.roles:
                                await member.add_roles(role_to_add, reason=f"Demoted by {ctx.author}.")
                            await member.remove_roles(role_to_remove, reason=f"Demoted by {ctx.author}.")
                            resp = await roster(self.client)
                            await ros.edit(embed=resp[0])
                            return await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
                await member.remove_roles(role_to_remove, reason=f"Demoted by {ctx.author}.")
                if staff_team in member.roles:
                    await member.remove_roles(staff_team, reason=f"Demoted by {ctx.author}.")
                resp = await roster(self.client)
                await ros.edit(embed=resp[0])
                await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
            else:
                for key, value in STAFF.items():
                    if key == role.lower():
                        role_to_add = discord.utils.get(ctx.guild.roles, id=value)
                        all_roles = [member_role for member_role in member.roles[::-1] if member_role.name.lower() in STAFF]
                        roles_to_remove = []
                        for i, r in enumerate(all_roles):
                            if role.lower() == r.name.lower():
                                for t in all_roles[:i+1]:
                                    roles_to_remove.append(t)
                        await member.add_roles(role_to_add, reason=f"Demoted by {ctx.author}.")
                        for item in roles_to_remove[:-1]:
                            await member.remove_roles(item, reason=f"Demoted by {ctx.author}.")
                        resp = await roster(self.client)
                        await ros.edit(embed=resp[0])
                        await ctx.message.add_reaction("<:GreenTick:800399486501257216>")

    @commands.command()
    @commands.has_any_role(840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roster(self, ctx):
        if ctx.guild.id == DVY_ID and ctx.channel.id == 796828098631827536:
            async def callback(inter):
                alts = {904468888140537966, 879790392344731688, 646094261783363666, 690247481417531419}
                all_ids = [id_ for id_ in STAFF.values()][::-1]
                memo = set()
                embed = discord.Embed(title="Diversity Staff Roster!", colour=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")

                for role in all_ids[:-1]:
                    final = []
                    r = discord.utils.get(ctx.guild.roles, id=role)
                    for member in r.members:
                        if member.id not in alts and member.name not in memo:
                            final.append(member.mention)
                            memo.add(member.name)
                    embed.add_field(name=f"__{r.name}__", value="\n".join(final) + "\n\u200b", inline=False)
                await inter.response.edit_message(embed=embed)

            alts = {904468888140537966, 879790392344731688, 646094261783363666, 690247481417531419}
            all_ids = [id_ for id_ in STAFF.values()][::-1]
            memo = set()
            embed = discord.Embed(title="Diversity Staff Roster!", colour=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")

            for role in all_ids[:-1]:
                final = []
                r = discord.utils.get(ctx.guild.roles, id=role)
                for member in r.members:
                    if member.id not in alts and member.name not in memo:
                        final.append(member.mention)
                        memo.add(member.name)
                embed.add_field(name=f"__{r.name}__", value="\n".join(final) + "\n\u200b", inline=False)

            refresh = Button(style=discord.ButtonStyle.green, label="Update", custom_id="refresh_roster", emoji="🔄")
            refresh.callback = callback

            view = View(refresh, timeout=None)
            roster = await ctx.send(embed=embed, view=view)
            async with aiosqlite.connect("main.db") as main:
                await main.execute("UPDATE roster SET id=?", (roster.id,))
                await main.execute("UPDATE views SET message_id=? WHERE command=?", (roster.id, "roster"))
                await main.commit()
            self.client.add_view(view, message_id=roster.id)

    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def addclub(self, ctx, *tags):
        async with aiosqlite.connect("main.db") as main:
            async with main.execute("SELECT * FROM clubs") as cur:
                res = set(item[0] for item in await cur.fetchall())

            binary, invalid, existent = [], [], []
            for i, tag in enumerate(tags):
                tag = self.filter_tag(tag)
                binary.append(False)
                if tag == -1:
                    invalid.append(tags[i])
                elif tag in res:
                    existent.append(tags[i])
                else:
                    await main.execute("INSERT INTO clubs(tag) VALUES(?)", (tag,))
                    binary[-1] = True

            await main.commit()
            if all(binary):
                return await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
            elif any(binary):
                message = ""
                if invalid:
                    message += "Some given club tags are incorrect.\n```\n{}\n```\n".format(", ".join(invalid))
                if existent:
                    message += "Some given club tags are already registered.\n```\n{}\n```\n".format(", ".join(existent))

                if message:
                    return await ctx.send(message)
            await ctx.message.add_reaction("<:RedTick:800399301980323840>")

    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def removeclub(self, ctx, *tags):
        async with aiosqlite.connect("main.db") as main:
            async with main.execute("SELECT * FROM clubs") as cur:
                res = set(item[0] for item in await cur.fetchall())

            binary, non_existent = [], []
            for i, tag in enumerate(tags):
                tag = self.filter_tag(tag)
                binary.append(False)
                if tag not in res:
                    await main.execute(f"DELETE FROM clubs WHERE tag={tag}")
                    binary[-1] = True
                    continue
                non_existent.append(tags[i])
            await main.commit()
            if all(binary):
                return await ctx.message.add_reaction("<:GreenTick:800399486501257216>")
            elif any(binary):
                return await ctx.send("Some of the given club tags are not registered.\n```\n{}\n```".format(", ".join(non_existent)))
            await ctx.message.add_reaction("<:RedTick:800399301980323840>")

    @commands.command()
    @commands.has_any_role(759095518084202496, 840954783149588560, 755539981195542690, 779556357174329344, 779555024170254398)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clubs(self, ctx):
        async with aiosqlite.connect("main.db") as main:
            placeholder = await ctx.send("<a:loading:771414970637877248> Working...")
            clubs = await self.get_clubs()
            await ctx.message.delete()
            await placeholder.delete()
            await ctx.send(embed=clubs.pop(0)[0])
            for club_embed, dd in clubs:
                await self.set_club_application(dd)
                view = View(dd, timeout=None)
                resp = await ctx.send(embed=club_embed, view=view)
                if ctx.channel.id == 735917551703556136:
                    await main.execute("DELETE FROM club_embeds")
                    await main.execute("INSERT INTO club_embeds(id) VALUES(?)", (resp.id,))
                    await main.commit()
                self.client.add_view(view, message_id=resp.id)

def setup(client):
    client.add_cog(Administration(client))
