const chatBody = document.getElementById('chat-body');
const chatInput = document.getElementById('user-input'); 
const sendButton = document.getElementById('send-btn');

function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerHTML = `<span>${text}</span>`;
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function showTyping() {
    const typing = document.createElement("div"); 
    typing.classList.add('typing');
    typing.id = "typing";
    typing.innerText = "Bot is typing...";
    chatBody.appendChild(typing);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

async function sendMessage() {
    const message = chatInput.value.trim();  
    if (!message) return;

    appendMessage(message, 'user');
    chatInput.value = ''; 
    showTyping();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: SESSION_ID, message })
        });

        const data = await res.json();
        removeTyping();
        appendMessage(data.response, "bot"); 
    } catch (err) {
        removeTyping();
        appendMessage("Sorry, something went wrong. Please try again later.", "bot");
    }
}

sendButton.addEventListener('click', sendMessage);

chatInput.addEventListener('keydown', (e) => { 
    if (e.key === 'Enter') sendMessage();
});