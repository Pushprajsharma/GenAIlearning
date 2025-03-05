const chatBox = document.getElementById('messages');
const chatInput = document.getElementById('questionInput');
var sendButton = document.getElementById('askButton');
const voiceButton = document.getElementById('voiceButton');

// sendButton.addEventListener('click', sendMessage);
// voiceButton.addEventListener('click', startVoiceRecognition);

voiceButton.addEventListener('click',()=>{
    startVoiceRecognition();
    console.log("voice button clicked")
})


sendButton.addEventListener('click',()=>{
    console.log("fired")
    const message = chatInput.value.trim();
    console.log(message)
    if (message !== '') {
        appendMessage('You', message);
        callAPI(message);
        chatInput.value = '';
    }
})

function sendMessage() {
    
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function callAPI(question) {

    console.log("API is called")

    let url = 'http://127.0.0.1:5000/ask?q='+question;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        } 
    })
    .then(response => response.json())
    .then(data => appendMessage('Bot', data.answer))
    .catch(error => console.error('Error:', error));
}

function startVoiceRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
    };
    recognition.start();
}
