"use strict";

module.exports = {
    name: "weekend",
    description: "Pings the `Weekend Events` role to ask for a team to do the current weekend event with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "767089586970034187") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#767089586970034187>."
            });
            return;
        }

        if (!message.member.roles.cache.get("767097985501888543")) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "You need the <@&767097985501888543> role to use this command."
            });
            return;
        }

        message.deletable && await message.delete();
        let msg = `<@&767097985501888543>: <@${message.member.id}> is looking for a teammate to do the weekend events with!`;
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