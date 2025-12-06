"use strict";

const stats = require("../../data/stats.json");

module.exports = {
    name: "ustats",
    description: "Updates a user's stats roles (trophies, 3v3/solo/duo wins).",
    cooldown: 5,

    async execute(message, args) {
        if (message.member.roles.cache.get("782266411447091200")) {
            const user = await message.guild.members.fetch(args.find((x) => /<@!*[0-9]+>/.test(x)));;
            delete args[args.indexOf(user)];

            if (!(user && args.filter(Boolean).length > 0)) {
                return await message.react("<:RedTick:800399301980323840>");
            }

            message.guild.members.fetch(user.replace(/[\\<>@!#&]/g, "").trim())
                .then(async (member) => {
                    const params = args.join("").replace(" ", "").split("/").map((item) => stats[item]).filter(Boolean);
                    const add = [];
                    const remove = member.roles.cache.filter((role) => /[0-9]+k\+/.test(role.name.toLowerCase()));

                    params.forEach(async (element) => add.push(await message.guild.roles.fetch(element)));

                    remove.size > 0 && await member.roles.remove(remove);
                    add.length > 0 && await member.roles.add(add);

                    await message.react("<:GreenTick:800399486501257216>");
                })
                .catch(async () => {
                    await message.react("<:RedTick:800399301980323940>")
                });
        }
    }
};