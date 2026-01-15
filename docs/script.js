const API_URL = "http://localhost:3000/api/assist";

// Elements
const startBtn = document.querySelector('.btn-primary');
const readTextBtn = document.querySelectorAll('.btn-ghost')[0];
const explainBtn = document.querySelectorAll('.btn-ghost')[1];
const navBtn = document.querySelectorAll('.btn-ghost')[2];
const insightText = document.querySelector('.insight-text');

/**
 * Main function to communicate with the Python backend
 */
async function sendToVision(mode) {
    insightText.innerHTML = "<strong>AI:</strong> Processing your request...";

    try {
        // In a production app, you would capture a frame from a <video> element here
        // For your portfolio demo, we'll assume a file input or a placeholder blob
        const formData = new FormData();
        
        // This is where you'd append the actual image data
        // formData.append('image', blob, 'capture.jpg'); 
        formData.append('mode', mode);

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            insightText.innerHTML = `<strong>AI (${mode}):</strong> "${data.description}"`;
            // Trigger Text-to-Speech (TTS) for accessibility
            speak(data.description);
        } else {
            insightText.innerText = "Error: " + data.message;
        }
    } catch (err) {
        insightText.innerText = "Connection failed. Check if backend is running.";
    }
}

/**
 * Accessibility feature: Converts the AI text into speech
 */
function speak(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
}

// Event Listeners
readTextBtn.addEventListener('click', () => sendToVision('text'));
explainBtn.addEventListener('click', () => sendToVision('diagram'));
navBtn.addEventListener('click', () => sendToVision('navigation'));
