"use strict";

module.exports = {
    name: "deadchat",
    description: "Pings the chat revival role. Must be used in the general channel and the user must have the role.",
    cooldown: 3600,

    async execute(message) {
        if (message.channelId !== "706633062414548992") {
            return await message.channel.send({
                content: "This command can only be used in <#706633062414548992>."
            });
        }

        if (!message.member.roles.cache.get("767394777888325632")) {
            message.client.reset_cooldown(this, message.author);
            return await message.channel.send("You need the <@&767394777888325632> role to use this command.");
        }

        await message.channel.send({
            content: `<@&767394777888325632>: **<#706633062414548992> is dead! Please teleport over here and help us make it active again!** <:dyna_nice:766714386458345505>\n||Requested by: \`${message.member.displayName}\`||`,
            allowedMentions: {
                "parse": [
                    "users",
                    "roles"
                ]
            }
        });
    }
};