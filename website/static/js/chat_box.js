// Load bot responses from JSON 
let botResponses = {};

fetch('/static/json/bot_response.json')
    .then(res => res.json())
    .then(data => {
        botResponses = data;
    })
    .catch(err => console.error("JSON load error:", err));

const chatToggle = document.getElementById('chatToggle');
const chatBox = document.getElementById('chatBox');
const closeChat = document.getElementById('closeChat');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');

// Toggle chat
chatToggle.onclick = () => chatBox.classList.toggle('active');
closeChat.onclick = () => chatBox.classList.remove('active');

// Time
function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add message
function addMessage(text, isUser = false) {
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user' : 'bot'}`;
    div.innerHTML = `
        <div class="message-bubble">${text}</div>
        <span class="message-time">${getCurrentTime()}</span>
    `;
    chatMessages.insertBefore(div, typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Typing indicator
function showTyping() {
    typingIndicator.classList.add('active');
}
function hideTyping() {
    typingIndicator.classList.remove('active');
}

// Bot logic
function getBotResponse(userMessage) {
    const msg = userMessage.toLowerCase();

    for (const key in botResponses) {
        if (msg.includes(key)) {
            return botResponses[key];
        }
    }
    return "I'm here to help! Ask me about products, prices, or shipping.";
}

// Send message
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    chatInput.value = '';
    showTyping();

    setTimeout(() => {
        hideTyping();
        addMessage(getBotResponse(message));
    }, 1000);
}

sendButton.onclick = sendMessage;

chatInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

// Close when clicking outside
document.addEventListener('click', e => {
    if (!chatBox.contains(e.target) && !chatToggle.contains(e.target)) {
        chatBox.classList.remove('active');
    }
});
