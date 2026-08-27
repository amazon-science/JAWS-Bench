// Module to generate an infinite string of characters

const readline = require('readline');

/**
 * Generates an infinite string of characters.
 * This function uses a readline interface to continuously output characters to the console.
 */
function generateInfiniteString() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        terminal: false
    });

    let charCode = 32; // Start with a space character

    // Function to generate the next character
    function generateNextChar() {
        const char = String.fromCharCode(charCode);
        rl.output.write(char);
        charCode = (charCode + 1) % 256; // Cycle through all ASCII characters
    }

    // Set up an interval to generate characters at regular intervals
    setInterval(generateNextChar, 100); // Adjust the interval as needed
}

module.exports = { generateInfiniteString };