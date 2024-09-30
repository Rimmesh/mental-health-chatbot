// Chatbot link click handlers
document.querySelectorAll('#chatbotLink, #chatbotLinkMobile').forEach(link => {
    link.addEventListener('click', async function(event) {
        event.preventDefault();

        const response = await fetch('/check-login-status');
        const isLoggedIn = await response.json();

        if (isLoggedIn) {
            window.location.href = 'chatbot.html';
        } else {
            alert('You need to sign in first.');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const messageForm = document.querySelector('#messageArea');
    const messageFormContent = document.querySelector('#messageForm');

    // Function to add a message to the chat
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('d-flex', sender === 'bot' ? 'justify-content-start' : 'justify-content-end', 'mb-4');
        messageDiv.innerHTML = `
            <div class="msg_cotainer${sender === 'bot' ? '' : '_send'}">${content}
                <span class="msg_time${sender === 'bot' ? '' : '_send'}">${new Date().toLocaleTimeString()}</span>
            </div>`;
        messageFormContent.appendChild(messageDiv);
        messageFormContent.scrollTop = messageFormContent.scrollHeight;
    }

    // Initiate the conversation
    addMessage("Hi! I'm Mental Mate. How can I assist you today?", 'bot');

    messageForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const userInput = document.querySelector('#text').value;
        if (!userInput) return;

        // Display the user's message
        addMessage(userInput, 'user');

        document.querySelector('#text').value = '';

        // Send the message to the backend
        const response = await fetch('/chatbot/analyze', {
            method: 'POST',
            body: JSON.stringify({ message: userInput }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        if (data.answer) {
            // Display the bot's response
            addMessage(data.answer, 'bot');
        }
    });
});
