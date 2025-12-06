"use strict";

const DiscordJS = require("discord.js");
const mongoose = require("mongoose");
const path = require("path");
const fs = require("fs");

const config = require("./config.json");
const colouring = require("./colour");


const client = new DiscordJS.Client({
    presence: {
        "status": "online",
        "activities": [
            {
                "name": "with DVY members!",
                "type": DiscordJS.ActivityType.Playing
            }
        ]
    },

    allowedMentions: {
        "parse": ["users"]
    },

    intents: [
        DiscordJS.GatewayIntentBits.Guilds,
        DiscordJS.GatewayIntentBits.GuildMessages,
        DiscordJS.GatewayIntentBits.DirectMessages,
        DiscordJS.GatewayIntentBits.GuildMessageReactions,
        DiscordJS.GatewayIntentBits.DirectMessageReactions,
        DiscordJS.GatewayIntentBits.GuildMembers,
        DiscordJS.GatewayIntentBits.GuildEmojisAndStickers,
        DiscordJS.GatewayIntentBits.MessageContent
    ],

    partials: [
        DiscordJS.Partials.Channel
    ]
});

client.commands = new DiscordJS.Collection();
client.cooldowns = new Map();
client.reset_cooldown = (command, user) => client.cooldowns.get(command.name).delete(user.id);

console.log("--------------------------------------------------");

const base = path.join(__dirname, "Commands");
const categories = fs.readdirSync(base).filter((folder) => /[A-Z]\w+/g.test(folder));
for (const category of categories) {
    const dir = fs.readdirSync(path.join(base, category));

    console.log(`${colouring.black("[Loader]")} Started loading into ${colouring.red(category)} ${colouring.red("Commands")}`);
    for (const commandFile of dir) {
        const num = dir.indexOf(commandFile) + 1;
        const connector = (num < dir.length) ? "╠═════" : "╚═════";

        const command = require(path.join(base, category, commandFile));
        client.commands.set(command.name, command);

        console.log(`${colouring.black("[Loader]")} ${connector} Loaded ${colouring.green(commandFile)} (${num}/${dir.length})`);
    }
    console.log("--------------------------------------------------");
}

console.log(`${colouring.black("[Loader]")} ${colouring.green("All commands successfully loaded.")}`);
console.log("--------------------------------------------------");
client.once("ready", (client) => {
    console.log(`${colouring.black("[Loader]")} Logged in as ${colouring.red(client.user.tag)}!`);
    console.log("--------------------------------------------------");
});

// mongoose.connect(`mongodb+srv://${user}:${pass}@dvy-bot-cluster.haf4eny.mongodb.net/DVY-Bot?retryWrites=true&w=majority`)
//     .then(() => {
//         console.log(`${colouring.black("[Loader]")} ${colouring.green("Successfully established a MongoDB connection.")}`);
//         console.log("--------------------------------------------------");
//     });

const dbPath = path.join(__dirname, "Database");
const database = fs.readdirSync(dbPath);

console.log(`${colouring.black("[Debug]")} Started loading into ${colouring.red("Database models")}`);
for (const model of database) {
    const num = database.indexOf(model) + 1;
    const connector = (num < database.length) ? "╠═════" : "╚═════";

    require(path.join(dbPath, model));
    console.log(`${colouring.black("[Debug]")} ${connector} Loaded ${colouring.green(model)} (${num}/${database.length})`);
    console.log("--------------------------------------------------");
}

console.log(`${colouring.black("[Debug]")} ${colouring.green("All MongoDB models loaded successfully.")}`);
console.log("--------------------------------------------------");


client.on("messageCreate", async (message) => {
    if (/<@!*872609283743838248>/.test(message.content) && !message.author.bot) {
        await message.channel.send({
            content: "#StayDvystic <:LeonLul:762367743001362473>"
        });
    }

    if (message.content.trim().toLowerCase().startsWith(config.prefix)) {
        // const CooldownModel = require("./Database/CooldownModel");
        const args = message.content.trim().slice(config.prefix.length).split(/ +/);

        //! remove if statement when not in development
        if (message.author.id === "529433085473849356") {
            const command = client.commands.get(args.shift().toLowerCase());
            // const cooldown = new CooldownModel({
            //     commandName: command.name,
            //     meta: []
            // });

            // const item = await CooldownModel.findOne({commandName: command.name});
            // if (!item) {
            //     await cooldown.save();
            // }

            // const time = Date.now();
            // const mapping = await CooldownModel.findOne({
            //     commandName: command.name,
            //     meta: {
            //         user
            //     }
            // });

            // if (mapping.meta[message.author.id]) {
            //     const exp_time = mapping.meta.time + command.cooldown * 1000;
            //     if (time < exp_time) {
            //         return message.react("<:RedTick:800399301980323840>");
            //     }
            // }

            //! remove the .then() comments to enable cooldowns
            command.execute(message, args);
            // .then(async () => {
            //     await CooldownModel.findOneAndUpdate({
            //         commandName: command.name
            //     }, {

            //     });

            //     mapping.set(message.author.id, time);
            //     setTimeout(async () => {
            //         await CooldownModel.findOneAndDelete({});
            //     }, command.cooldown * 1000);
            // });
        }
    }
});

client.login(config.discord_token);
