"use strict";

const DiscordJS = require("discord.js");

module.exports = {
    name: "roster",
    description: "",
    cooldown: 0,

    /**
     * @param {DiscordJS.Message} message
     */
    async execute(message) {
        await message.channel.sendTyping();
        await message.guild.members.fetch({ force: true });

        const hierarchy = [
            "779555024170254398",
            "779556357174329344",
            "755539981195542690",
            "840954783149588560",
            "759095518084202496",
            "759083819453513809",
            "806589031378845737",
            "771858032644325396"
        ];

        const alts = [
            "904468888140537966",
            "926802964742561852",
            "879790392344731688",
            "646094261783363666",
            "690247481417531419",
            "986420345307299960",
            "1057282236031963176"
        ];

        const roster = new DiscordJS.EmbedBuilder()
            .setTitle("Diversity Staff Roster")
            .setColor("#01BB70")
            .setThumbnail("https://i.imgur.com/GlZttyo.gif");

        const unique = [];
        for (const position of hierarchy) {
            const people = [];
            const role = await message.guild.roles.fetch(position, { force: true });
            for (const member of role.members) {
                if ((!alts.includes(member[0])) && (!unique.includes(member[0]))) {
                    people.push(`<@${member[1].user.id}>`);
                    unique.push(member[0]);
                }
            }

            roster.addFields([{
                name: `__${role.name}__`,
                value: people.join("\n") + "\n\u200b",
                inline: false
            }]);
        }

        await message.channel.send({
            embeds: [roster]
        });
    }
};
