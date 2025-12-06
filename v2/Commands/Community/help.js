"use strict";

const DiscordJS = require("discord.js");

module.exports = {
    name: "help",
    description: "Help text for help command, pretty neat right?",
    cooldown: 3,

    async execute(message, args) {
        if (args.length > 0) {
            const command = message.client.commands.get(args.shift().trim().toLowerCase()) ?? "Unknown command";
            const commandHelpEmbed = new DiscordJS.EmbedBuilder()
                .setTitle(`Command help: ${command?.name}` ?? "There's no such command!")
                .setDescription((command !== "Unknown command" ? command.description : "The command specified could not be found."))
                .setColor("#01BB70");

            return await message.author.send({
                embeds: [commandHelpEmbed]
            });
        }

        /*
        * --- NOTE --- *
        * LFG commands embed note: "Every command can only be used at its respective channel, if the user also has the appropriate role."
        * Verification commands embed note: "You need the @Staff Team role to use any of these commands."
        * Administration commands embed note: "You need any role from @Administrator or higher to use any of these commands."
        */

        const helpEmbed = new DiscordJS.EmbedBuilder()
            .setTitle("halp")
            .setDescription("wtf u doing lol")
            .setColor("#01BB70");

        const verifEmbed = new DiscordJS.EmbedBuilder()
            .setTitle("verification shi")
            .setDescription("wtf u doing lol")
            .setColor("#01BB70");

        const lfgEmbed = new DiscordJS.EmbedBuilder()
            .setTitle("carry me to r30 pls")
            .setDescription("wtf u doing lol")
            .setColor("#01BB70");

        const adminEmbed = new DiscordJS.EmbedBuilder()
            .setTitle("swing the ban hammer lads")
            .setDescription("wtf u doing lol")
            .setColor("#01BB70");

        await message.author.send({
            embeds: [helpEmbed]
        });
    }
};