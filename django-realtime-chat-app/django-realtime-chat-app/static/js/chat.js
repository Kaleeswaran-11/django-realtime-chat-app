(function () {
    if (!window.chatConfig) return;

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const { currentUser, otherUser, roomName } = window.chatConfig;
    const chatLog = document.getElementById('chat-log');
    const chatInput = document.getElementById('chat-message-input');
    const chatForm = document.getElementById('chat-form');
    const typingIndicator = document.getElementById('typing-indicator');
    const presenceDot = document.getElementById('presence-dot');
    const presenceText = document.getElementById('presence-text');

    const chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomName}/`);
    const presenceSocket = new WebSocket(`${protocol}://${window.location.host}/ws/presence/`);

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function appendMessage(message, sender, timestamp) {
        const row = document.createElement('div');
        row.className = `message-row ${sender === currentUser ? 'sent' : 'received'}`;
        row.innerHTML = `
            <div class="message-bubble">
                <div>${message}</div>
                <div class="message-meta">${timestamp}</div>
            </div>`;
        chatLog.appendChild(row);
        scrollToBottom();
    }

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
            appendMessage(data.message, data.sender, data.timestamp);
        }
        if (data.type === 'typing') {
            typingIndicator.textContent = data.is_typing ? `${data.user} is typing...` : '';
        }
    };

    presenceSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'presence' && data.username === otherUser) {
            presenceDot.classList.remove('online', 'offline');
            presenceDot.classList.add(data.is_online ? 'online' : 'offline');
            presenceText.textContent = data.is_online ? 'Online' : 'Offline';
        }
    };

    let typingTimer;
    chatInput.addEventListener('input', function () {
        chatSocket.send(JSON.stringify({ type: 'typing', is_typing: true }));
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            chatSocket.send(JSON.stringify({ type: 'typing', is_typing: false }));
        }, 1000);
    });

    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;
        chatSocket.send(JSON.stringify({ receiver: otherUser, message }));
        chatInput.value = '';
        chatSocket.send(JSON.stringify({ type: 'typing', is_typing: false }));
    });

    scrollToBottom();
})();
