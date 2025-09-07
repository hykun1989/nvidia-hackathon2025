document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newChatBtn = document.getElementById('newChatBtn');

    let currentChatId = Date.now().toString();

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        appendMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: [{
                        role: 'user',
                        content: message
                    }],
                    stream: true
                })
            });

            const reader = response.body.getReader();
            let accumulatedResponse = '';

            while (true) {
                const {done, value} = await reader.read();
                if (done) break;

                const text = new TextDecoder().decode(value);
                accumulatedResponse += text;

                // Update the last assistant message with accumulated response
                const lastMessage = document.querySelector('.assistant-message');
                if (lastMessage) {
                    lastMessage.innerHTML = marked(accumulatedResponse);
                } else {
                    appendMessage(accumulatedResponse, 'assistant');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            appendMessage('发生错误，请稍后重试。', 'assistant');
        }
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message mb-4 p-4 rounded ${
            sender === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-100'
        } max-w-3xl`;
        messageDiv.innerHTML = sender === 'assistant' ? marked(text) : text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

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
    });
});
