"use strict";

module.exports = {
    name: "1v1",
    description: "Pings the `1v1` role to ask for a 1v1 challenge.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "810510255138144296") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#810510255138144296>."
            });
            return;
        }

        if (!message.member.roles.cache.get("792062568805433345")) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "You need the <@&792062568805433345> role to use this command."
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&792062568805433345>: <@${message.member.id}> is looking for an opponent to 1v1!`;
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