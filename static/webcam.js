
class MediaDevices extends EventTarget {
    constructor() {
        super();
    }

    enumerateDevices() {
        return navigator.mediaDevices.enumerateDevices();
    }

    getSupportedConstraints() {
        return navigator.mediaDevices.getSupportedConstraints();
    }

    getUserMedia(constraints) {
        return navigator.mediaDevices.getUserMedia(constraints);
    }

    getDisplayMedia() {
        return navigator.mediaDevices.getDisplayMedia();
    }
}

const mediaDevices = new MediaDevices();
const video = document.getElementById("videoElement");
const emotionResults = document.getElementById("emotionResults");

const constraints = {
    audio: false,
    video: true,
};

let timerReset = 0
document.getElementById("startCapture").addEventListener("click", () => {
    mediaDevices.getUserMedia(constraints)
        .then((stream) => {
            const videoTracks = stream.getVideoTracks();
            console.log("Got stream with constraints:", constraints);
            console.log(`Using video device: ${videoTracks[0].label}`);
            stream.onremovetrack = () => {
                console.log("Stream ended");
            };
            video.srcObject = stream;

            // Example: Analyze emotions using your emotion analysis library/API
            // Once emotions are analyzed, display them in the UI
            timerReset = setInterval(captureAndUploadImage, 1000);
            displayEmotions(emotions);
        })
        .catch((error) => {
            if (error.name === "NotAllowedError") {
                console.error("You need to grant this page permission to access your camera and microphone.");
            } else {
                console.error(`getUserMedia error: ${error.name}`, error);
            }
        });
});

document.getElementById("stopCapture").addEventListener("click", () => {
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        console.log("Video capture stopped");
        clearInterval(timerReset);
    }
});


function captureAndUploadImage() {
    const video = document.getElementById("videoElement");

    // Create a canvas element to draw the video frame
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas image to base64 data URL (JPEG format)
    const imageDataURL = canvas.toDataURL('image/jpeg');
    
    // Extract the base64 image data
    const imageData = imageDataURL.split(',')[1];

    // Send the base64 image data to the server via POST request
    fetch('http://localhost:5001/admin.html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Image uploaded successfully:', data);
        // Handle response from server if needed
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
