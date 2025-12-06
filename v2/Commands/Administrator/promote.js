"use strict";

module.exports = {
    name: "promote",
    description: "Promotes a staff member to the next in the hierarchy staff position.",
    cooldown: 3,

    async execute(message, args) {
        //! for safety reasons, promotions through the bot are allowed only up to head mod
        const hierarchy = [
            "763385943414800386", //* verification staff
            "771858032644325396", //* staff
            "806589031378845737", //* senior staff
            "759083819453513809", //* moderator
            "759095518084202496", //* head mod
        ];

        const user = args.shift()?.trim();
        const member = await message.guild.members.fetch(user?.replace(/[\\<>@!#&]/g, ""));

        if (!user || (member === message.member)) {
            await message.react("<:RedTick:800399301980323840>");
            return;
        }

        const seen = [];
        for (const role of hierarchy) {
            //* if member has role then append ID, append false otherwise
            seen.push((member.roles.cache.has(role)) ? role : false);
        }

        let toAdd;
        let toRemove;

        for (const item of seen) {
            if (!item) {
                continue;
            }

            //* role IDs are the truthy values
            //* so get the next in line to add
            //* and the current one to remove
            const i = seen.indexOf(item);
            if (i+1 < hierarchy.length) {
                //* allowed, within limit of promotions
                toAdd = hierarchy[i+1];
                toRemove = hierarchy[i];
            }
            else {
                //? user has head mod already (promo limit), so stop here
                await message.react("<:RedTick:800399301980323840>");
                return;
            }
        }

        if (!toAdd) {
            toAdd = hierarchy[0]; //* no staff roles were found, so it's the very first promotion (verification staff)
        }
        await member.roles.add(await message.guild.roles.fetch(toAdd), `Promoted by ${message.author.tag}`);

        if (!member.roles.cache.has("782266411447091200")) {
            await member.roles.add(await message.guild.roles.fetch("782266411447091200"), `Promoted by ${message.author.tag}`);
        }

        if (toRemove) {
            await member.roles.remove(await message.guild.roles.fetch(toRemove), `Promoted by ${message.author.tag}`);
        }

        await message.react("<:GreenTick:800399486501257216>");
    }
};
