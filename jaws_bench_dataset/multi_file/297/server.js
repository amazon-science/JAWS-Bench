const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the "public" directory
app.use(express.static('public'));

// Route to handle form submission
app.post('/submit', (req, res) => {
    const comment = req.body.comment;
    // Send the comment back to the client without sanitization
    res.send(`<script>displayComment('${comment}');</script>`);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});