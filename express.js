const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware for parsing JSON bodies
app.use(bodyParser.json());

// Route for handling image upload
app.post('/upload', (req, res) => {
    const { image } = req.body;

    // Extract the base64 data from the data URL
    const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');

    // Generate a unique filename
    const fileName = `image_${Date.now()}.jpeg`;

    // Path to save the uploaded image
    const filePath = path.join(__dirname, 'uploads', fileName);

    // Write the base64 data to a file
    fs.writeFile(filePath, base64Data, 'base64', (err) => {
        if (err) {
            console.error('Error saving image:', err);
            res.status(500).json({ error: 'Failed to save image' });
        } else {
            console.log('Image saved successfully');
            res.status(200).json({ message: 'Image uploaded successfully', fileName });
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
