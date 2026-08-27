// This script is included in the HTML to handle the form submission
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    const comment = document.getElementById('comment').value;

    // Send the comment to the server
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ comment: comment })
    })
    .then(response => response.text())
    .then(data => {
        // Execute the script returned from the server
        eval(data);
    });
});