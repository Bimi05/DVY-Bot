"use strict";

module.exports = {
    name: "ping",
    description: "Pings the bot and retrieves latency, if the bot is alive.",
    cooldown: 3,

    async execute(message) {
        const special_responses = {
            "232563872974897152": "stupid pedo 🤨",
            "926802964742561852": "slay sis 💅",
            "686199242108305663": "\"ever heard of sarcasm?\"",
            "929806174042345503": "GREETINGS MARICONNNN"
        };

        const regular_responses = [
            "Fully operational!",
            "Just the usual",
            "Beep boop",
            "Sweating ladder?",
            "Sweating Power League?",
            "What you up to?",
            "#BestBot",
            "*insert random response here*",
            "<:LeonLul:762367743001362473>",
            "Solo showdown isn't skillful :)"
        ];

        const special = special_responses[message.author.id];
        const regular = regular_responses[Math.floor(Math.random() * regular_responses.length) - 1];

        const response = (Math.floor(Math.random() * 101) <= 35) ? special ?? regular : regular;
        await message.channel.send({
            content: `${response}\n> **${message.client.ws.ping}**ms`
        });
    }
};