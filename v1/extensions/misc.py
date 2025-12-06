import discord
import random

from const import DVY_ID
from discord.ext import commands
from discord.ui import Select, View

class Miscellaneous(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx):
        if ctx.guild.id == DVY_ID:
            async def cb(inter):
                dd = {"Main Menu": [basic, starter_opt], "LFG": [lfg, lfg_opt], "Verification": [verification, verification_opt], "Admins": [admins, admins_opt]}
                dropdown.options = dd[inter.data["values"][0]][1]
                await inter.response.edit_message(embed=dd[inter.data["values"][0]][0], view=view)

            basic = discord.Embed(title="<a:a_diversity:782269564678438922> DVY Bot help!", color=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")
            basic.add_field(name="All community commands", value=f"`d!help`: Well, this 😅\n`d!ping`: Ping the bot and get response latency.\n`d!deadchat`: Pings `@Chat Revival Team`.\n> You must have the role yourself to execute this command.")
            basic.set_footer(icon_url=ctx.author.display_avatar.url, text="Parameters marked with <> are required, [] are optional")

            lfg = discord.Embed(title="<a:a_diversity:782269564678438922> DVY Bot help!", color=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")
            lfg.add_field(name="All LFG commands", value="> **Note:** __You need to use each command at its respective channel.__\n\n`d!push <rank> [message]`:\nPing the corresponding role (that matches the specified `rank`) with message `message` (if any).\n- Valid rank roles: `r20`, r25`, `r30`, `r35`\n\n`d!league <league> [message]`:\nPing the corresponding role (that matches the specified `league`) with message `message` (if any).\n- Valid league roles: `bronze`, `silver`, `gold`, `diamond`, `mythic`, `legendary`, `masters`\n\n`d!weekend [message]`:\nPings the weekend event role with message `message` (if any).\n- Aliases: `d!weekendevents` | `d!we`\n\n`d!1v1 [message]`:\nPings the 1v1 role with message `message` (if any).\n\n`d!champ [message]`:\nPings the championship role with message `message` (if any).\n- Aliases: `d!cc` | `d!championship`\n\n`d!scrims [message]`:\nPings the scrims role with message `message` (if any).\n\n`d!quests [message]`:\nPings the quests role with message `message` (if any).")
            lfg.set_footer(icon_url=ctx.author.display_avatar.url, text="Parameters marked with <> are required, [] are optional")

            verification = discord.Embed(title="<a:a_diversity:782269564678438922> DVY Bot help!", color=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")
            verification.add_field(name="All Verification commands", value="> **Note:** __You need to have the `@Staff Team` role to use these commands.__\n\n`d!update <club> <member(s)>`: Updates the given `member(s)` to the specified `club` and edits their nickname accordingly. If many members are given, they are all updated to the same club. Using this on an unverified member sends a welcoming message (in such a case, this can only be used in the verification channel).\n\n`d!ustats <member> <stat role(s)>`: Grant/Update the `stat role(s)` for `member`. If many roles are specified, separate them with a `/`.\n\n`d!verify`: Purges the latest 1000 messages and sends a verification message providing instructions. Can only be used in the verification channel.")
            verification.set_footer(icon_url=ctx.author.display_avatar.url, text="Parameters marked with <> are required, [] are optional")

            admins = discord.Embed(title="<a:a_diversity:782269564678438922> DVY Bot help!", color=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")
            admins.add_field(name="All commands restricted to admins", value="> **Note:** __You need to have the `@Administrator` role to use these commands.__\n\n`d!promote <member> [role]`: Promote `member` to `role` (if specified). If `role` isn't specified, promote `member` to the next staff role in the role hierarchy.\n\n`d!demote <member> [role]`: Demote `member` to `role` (if specified, lowest must be \"Verification Staff\"). If `role` isn't specified, demote `member` to the previous staff role in the role hierarchy, or completely it.\n\n`d!roster`: Send an embed with the staff roster. Can only be used in the roster channel.\n\n`d!addclub <tag(s)>`: Add one or more club tag(s) in the bot's storage to be registered as official DVY clubs.\n\n`d!removeclub <tag(s)>`: Remove one or more official DVY club tag(s).\n\n`d!clubs`: Display all DVY clubs, their stats and an application form.")
            admins.set_footer(icon_url=ctx.author.display_avatar.url, text="Parameters marked with <> are required, [] are optional")

            starter_opt = [discord.SelectOption(label="LFG", description="All commands related to LFG (Looking For Games)", emoji="🎮"), discord.SelectOption(label="Verification", description="All commands related to verifying/updating members", emoji="🔎"), discord.SelectOption(label="Admins", description="All commands restricted to server admins (+Head Mods in some occasions)", emoji="🛡️")]
            lfg_opt = [discord.SelectOption(label="Main Menu", description="All the basic commands, available to everyone", emoji="⚙️"), discord.SelectOption(label="Verification", description="All commands related to verifying/updating members", emoji="🔎"), discord.SelectOption(label="Admins", description="All commands restricted to server admins (+Head Mods in some occasions)", emoji="🛡️")]
            verification_opt = [discord.SelectOption(label="Main Menu", description="All the basic commands, available to everyone", emoji="⚙️"), discord.SelectOption(label="LFG", description="All commands related to LFG (Looking For Games)", emoji="🎮"), discord.SelectOption(label="Admins", description="All commands restricted to server admins (+Head Mods in some occasions)", emoji="🛡️")]
            admins_opt = [discord.SelectOption(label="Main Menu", description="All the basic commands, available to everyone", emoji="⚙️"), discord.SelectOption(label="LFG", description="All commands related to LFG (Looking For Games)", emoji="🎮"), discord.SelectOption(label="Verification", description="All commands related to verifying/updating members", emoji="🔎")]

            dropdown = Select(custom_id="browse_command_sections", placeholder="Browse Command Sections...", options=starter_opt)
            dropdown.callback = cb

            view = View(dropdown, timeout=None)
            resp = await ctx.author.send(embed=basic, view=view)
            self.client.add_view(view, message_id=resp.id)

            await ctx.message.add_reaction("<:GreenTick:800399486501257216>")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        responses = [
            "Fully operational!",
            "Just the usual.",
            "Beep boop",
            "Sweating ladder?",
            "Sweating Power League?",
            "What you up to?",
            "#BestBot",
            "\*insert random response here*"
        ]

        special_responses = {
            232563872974897152: "stupid pedo 🤨",
            529433085473849356: "nerd 😀",
            730766572574212186: "L bozo + ratio",
            926802964742561852: "\*insert keyboard mash here*",
            708161272742412359: "😀",
            690247481417531419: "weirdo",
            730812565311193099: "weirdo",
            690267372292014122: "dead",
            829124161656848394: "true",
            686199242108305663: "\"ever heard of sarcasm?\"",
            616569586778767395: "omg",
            852969181699899456: "that one dead neek",
            685426672941531140: "SIUUUU",
            503106259940147200: "fuck u from very far away",
            361267387426799616: "dat trim doe",
            323215056126869505: "pro deadlifter",
            852868174059798538: "icl fam u movin real brazy, come hounslow I'll pattern u up",
            701894952250114157: "nellie! it's time for a walk!"
        }

        resp = None
        chance = random.randint(0, 100)
        if chance <= 35:
            resp = special_responses.get(ctx.author.id)

        if not resp:
            resp = random.choice(responses)
        await ctx.send(f"{resp}\n> **{self.client.latency*1000:.2f}**ms")

    @commands.command()
    @commands.cooldown(1, 3000, commands.BucketType.default)
    async def deadchat(self, ctx):
        if ctx.guild.id == DVY_ID:
            deadchat_role = discord.utils.get(ctx.author.roles, id=767394777888325632)
            if deadchat_role:
                await ctx.message.delete()
                return await ctx.send(f"{deadchat_role.mention}: **Report for duty! <#706633062414548992> is now dead! Please teleport over here and help us make it active again!** <:dyna_nice:766714386458345505>\n||Reported by: `{ctx.author.display_name}`||", allowed_mentions=discord.AllowedMentions(roles=True))
            await ctx.send(f"You must have the chat revival team ({deadchat_role.mention}) role to use this command.")


def setup(client):
    client.add_cog(Miscellaneous(client))
