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
    video: true,
};

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
            const emotions = analyzeEmotionsFromVideoStream(stream);
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
    }
});
// Capture image and send it to the server
document.getElementById("captureImage").addEventListener("click", () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataURL = canvas.toDataURL('image/jpeg');

    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageDataURL }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Image uploaded successfully:', data);
        // Handle server response if needed
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
});

// Example functions for emotion analysis and displaying results
function analyzeEmotionsFromVideoStream(stream) {
    // Implement emotion analysis logic here
    // Return the analyzed emotions as an object
}

function displayEmotions(emotions) {
    // Display the analyzed emotions in the UI
    emotionResults.innerHTML = JSON.stringify(emotions);
}
