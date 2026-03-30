(function () {
    if (!window.currentUsername) return;

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/`);
    const badge = document.getElementById('notification-badge');
    const list = document.getElementById('notification-list');

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type !== 'notification') return;

        badge.textContent = data.unread_count;
        const item = document.createElement('div');
        item.className = 'notification-item border-bottom pb-2 mb-2';
        item.innerHTML = `<strong>${data.sender}</strong><div class="small text-muted">${data.message}</div>`;
        if (list.querySelector('p')) list.innerHTML = '';
        list.prepend(item);
    };
})();
