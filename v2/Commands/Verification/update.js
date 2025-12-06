"use strict";

const DiscordJS = require("discord.js");
const names = require("../../data/names.json");

module.exports = {
    name: "update",
    description: "Updates a user. This includes changing their nickname and roles, according to the club they are given to be updated to.",
    cooldown: 5,

    async execute(message, args) {
        if (message.member.roles.cache.get("782266411447091200")) {
            const club = args.find((x) => names[x.trim().replace("'", "").toLowerCase()]);
            if (!club) {
                await message.react("<:RedTick:800399301980323840>");
                return;
            }

            delete args[args.indexOf(club)];
            args = args.filter(Boolean);

            const members = (args.length > 0) ? args : [ `<@${message.author.id}>` ];
            const add = await message.guild.roles.fetch(names[club].id);
            for (const member of members) {
                let user;
                try {
                    user = await message.guild.members.fetch(member.replace(/[\\<>@!#&]/g, ""));
                }
                catch (e) {
                    e instanceof DiscordJS.DiscordAPIError && void(0);
                }

                if (!(user && add)) {
                    continue;
                }

                const unverified = user.roles.cache.get("737151174465028126");
                if (unverified && message.channel.id === "850863329073561610") {
                    const general = await message.guild.channels?.fetch("706633062414548992");
                    const newNick = names[club].nickname;
                    const welcoming = new DiscordJS.EmbedBuilder()
                        .setTitle(`Everybody welcome \`${user.displayName}\`!`)
                        .setDescription("Make sure to read <#758814247437860934> and get your own self roles from the <#725868495388278785> channel! Each role grants access to its relevant channels, so choose accordingly! If you need any help regarding the server, please do not hesitate to DM <@575252669443211264>, we'll gladly help you out!\n\n**__Enjoy your stay!__**")
                        .setThumbnail(user.displayAvatarURL())
                        .setFooter({
                            text: `Account created at: ${user.user.createdAt.toLocaleString()}`,
                            iconURL: message.client.user.displayAvatarURL()
                        })
                        .setColor(add.hexColor);

                    await user.roles.add(add);
                    await user.roles.remove(unverified);
                    await user.edit({
                        nick: newNick.replace("{}", user.displayName)
                    });
                    await message.react(names[club].emoji);

                    general && general.send({
                        content: `<@${user.id}>`,
                        embeds: [ welcoming ]
                    });
                }
                else {
                    const remove = user.roles.cache.find((x) => names[x.name.toLowerCase()] !== undefined);

                    if (add.id === remove?.id) {
                        await message.react("<:RedTick:800399301980323840>");
                        return;
                    }

                    const newNick = names[club].nickname;
                    const slicedName = (remove.id === names.community.id) ? user.displayName : user.displayName.slice(5, -8);
                    await user.roles.add(add);
                    if (remove !== undefined) {
                        await user.roles.remove(remove);
                    }
                    await user.edit({
                        nick: newNick.replace("{}", slicedName)
                    });
                    await message.react(names[club].emoji);
                }
            }
        }
    }
};
