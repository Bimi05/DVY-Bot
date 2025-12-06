"use strict";

module.exports = {
    name: "champ",
    description: "Pings the `Championship` role to ask for a team to do the current challenge with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "810485897321644053") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#810485897321644053>."
            });
            return;
        }

        if (!message.member.roles.cache.get("809399188378353726")) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "You need the <@&809399188378353726> role to use this command."
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&809399188378353726>: <@${message.member.id}> is looking for a teammate to do the championship with!`;
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