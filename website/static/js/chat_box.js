// Elements
const chatToggle = document.getElementById('chatToggle');
const chatBox = document.getElementById('chatBox');
const closeChat = document.getElementById('closeChat');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');


chatToggle.onclick = () => chatBox.classList.toggle('active');
closeChat.onclick = () => chatBox.classList.remove('active');

// Close when clicking outside
document.addEventListener('click', e => {
    if (!chatBox.contains(e.target) && !chatToggle.contains(e.target)) {
        chatBox.classList.remove('active');
    }
});

// Time formatter
function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add message to UI
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

// CSRF helper (Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

// JSON BOT (Fallback)
let botResponses = {};

fetch('/static/json/bot_response.json')
    .then(res => res.json())
    .then(data => {
        botResponses = data;
    })
    .catch(err => console.warn("JSON bot not loaded:", err));

function getJsonBotResponse(userMessage) {
    const msg = userMessage.toLowerCase();

    for (const key in botResponses) {
        if (msg.includes(key)) {
            return botResponses[key];
        }
    }
    return "I'm here to help! Ask me about products, prices, or shipping.";
}

// Send message (AI first, JSON fallback)
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    chatInput.value = '';
    showTyping();

    fetch("/chatbot/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `message=${encodeURIComponent(message)}`
    })
    .then(res => {
        if (!res.ok) throw new Error("AI failed");
        return res.json();
    })
    .then(data => {
        hideTyping();
        addMessage(data.reply);
    })
    .catch(err => {
        hideTyping();
        const fallbackReply = getJsonBotResponse(message);
        addMessage(fallbackReply);
        console.warn("Using JSON fallback:", err);
    });
}

// Events
sendButton.onclick = sendMessage;

chatInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

