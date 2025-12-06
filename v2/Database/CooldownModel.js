const mongoose = require("mongoose");

const schema = new mongoose.Schema({
    commandName: String,
    meta: [{
        userId: String,
        time: Date
    }]
});

module.exports = mongoose.model("Cooldown", schema, "cooldowns");
