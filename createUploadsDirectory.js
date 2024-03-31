const fs = require('fs');
const path = require('path');

// Directory path
const directory = path.join(__dirname, 'uploads');

// Check if the directory exists
if (!fs.existsSync(directory)) {
    // Create the directory if it doesn't exist
    fs.mkdirSync(directory);
    console.log('Uploads directory created successfully.');
} else {
    console.log('Uploads directory already exists.');
}
