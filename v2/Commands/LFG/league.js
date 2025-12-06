"use strict";

module.exports = {
    name: "league",
    description: "Pings the corresponding role to ask for a team to play some Power League games with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "767089540639752192") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#767089540639752192>."
            });
            return;
        }

        const leagueRoles = {
            "bronze": "849625503212240916",
            "silver": "849625566415683645",
            "gold": "849625660607299584",
            "diamond": "849625733257101343",
            "mythic": "849625844851015740",
            "legendary": "849625926512672808",
            "master": "849626058554605658"
        };

        const role = leagueRoles[args.shift()];
        if (!role) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "Invalid league role provided. Please double check the command usage (<#851063073136574474>)!"
            });
            return;
        }

        if (!message.member.roles.cache.get(role)) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: `You need the <@&${role}> role to use this command.`
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&${role}>: <@${message.member.id}> is looking for a teammate to do Power League with!`;
        if (args.length > 0) {
            msg += `\n> Message provided: **${args.join(" ")}**`;
        }

        await message.channel.send({
            content: msg,
            allowedMentions: {
                "parse": [
                    "users",
                    "roles"
                ]
            }
        });
    }
};