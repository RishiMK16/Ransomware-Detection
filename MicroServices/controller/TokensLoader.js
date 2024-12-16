const tokens_path='D:\\CODES\\Projects\\Ransomware_Desktop\\Tokens.json'

const fs = require("fs");

// Read the JSON file synchronously
const jsonData = fs.readFileSync(tokens_path, "utf-8");

// Parse the JSON string into a JavaScript object
const data = JSON.parse(jsonData);

module.exports={data} // `data` is now a JavaScript object (dictionary)
