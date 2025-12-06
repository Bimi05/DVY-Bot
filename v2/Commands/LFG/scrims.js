"use strict";

module.exports = {
    name: "scrims",
    description: "Pings the `Scrims` role to ask for a team to do scrims with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "839865005511671808") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#839865005511671808>."
            });
            return;
        }

        if (!message.member.roles.cache.get("839866655018057768")) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "You need the <@&839866655018057768> role to use this command."
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&839866655018057768>: <@${message.member.id}> is looking for a teammate to do scrims with!`;
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