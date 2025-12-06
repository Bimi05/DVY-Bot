"use strict";

module.exports = {
    name: "push",
    description: "Pings the corresponding role to ask for a team to push a rank on ladder with.",
    cooldown: 3600,

    async execute(message, args) {
        if (message.channelId !== "767090495540822036") {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "This command can only be used in <#767090495540822036>."
            });
            return;
        }

        const pushRoles = {
            "r25": "767122614106849280",
            "r30": "767122780835282944",
            "r35": "767122869255536682"
        };

        const role = pushRoles[args.shift()];
        if (!role) {
            message.client.reset_cooldown(this, message.author);
            await message.channel.send({
                content: "Invalid rank role provided. Please double check the command usage (<#851063073136574474>)!"
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
        let msg = `<@&${role}>: <@${message.member.id}> is looking for a teammate to push ladder with!`;
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