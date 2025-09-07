let currentChatId = Date.now().toString();

document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const newChatBtn = document.getElementById('newChatBtn');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    newChatBtn.addEventListener('click', () => {
        currentChatId = Date.now().toString();
        chatContainer.innerHTML = '';
        userInput.value = '';
    });

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        appendMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    chat_id: currentChatId
                })
            });

            const data = await response.json();
            appendMessage(data.response, 'assistant');
        } catch (error) {
            console.error('Error:', error);
            appendMessage('抱歉，发生了错误，请稍后重试。', 'assistant');
        }
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = sender === 'assistant' ? marked(text) : text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
