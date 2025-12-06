"use strict";

module.exports = {
    name: "quests",
    description: "Pings the `Quests` role to ask for a team to do quests with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "851064466803130408") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#851064466803130408>."
            });
            return;
        }

        if (!message.member.roles.cache.get("849643821398228992")) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "You need the <@&849643821398228992> role to use this command."
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&849643821398228992>: <@${message.member.id}> is looking for a teammate to do quests with!`;
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