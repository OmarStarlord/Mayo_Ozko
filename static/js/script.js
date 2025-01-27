document.addEventListener("DOMContentLoaded", function () {
    // Get room ID, username, and CSRF token from the hidden input fields
    const roomId = document.getElementById("room-id").value;
    const username = document.getElementById("username").value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Initialize Pusher
    const pusher = new Pusher('b47d20482e4df2bf538c', {
        cluster: 'eu',
        forceTLS: true
    });

    // Subscribe to the room channel
    const channel = pusher.subscribe(`chat_${roomId}`);

    // Listen for 'new_message' event
    channel.bind('new_message', function (data) {
        if (data && data.sender && data.message && data.timestamp) {
            // Append the new message to the chat box
            const chatBox = document.getElementById("chat-box");
            const newMessage = document.createElement("div");
            newMessage.classList.add("chat-message", data.sender === username ? "user" : "friend");
            newMessage.innerHTML = `
                <div class="message-header"><strong>${data.sender}</strong></div>
                <p class="message-content">${data.message}</p>
                <span class="timestamp">${data.timestamp}</span>
            `;
            chatBox.appendChild(newMessage);

            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        } else {
            console.error("Invalid message data received:", data);
        }
    });

    // Send message on button click
    document.getElementById("chat-message-submit").addEventListener("click", function () {
        const messageContent = document.getElementById("chat-message-input").value.trim();

        if (messageContent) {
            fetch(`/rooms/${roomId}/send_message/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: JSON.stringify({ message: messageContent })
})
.then(response => {
    if (!response.ok) {
        return response.json().then(err => Promise.reject(err));
    }
    return response.json();
})
.then(data => {
    console.log('Message sent:', data);
    document.getElementById("chat-message-input").value = ""; // Clear input
})
.catch(error => {
    console.error('Error:', error);
    const errorMessage = error.error || 'Failed to send message';
    alert(`Error: ${errorMessage}`); // Or show in UI
});
        }
    }
    );


    const emojiButton = document.getElementById("emoji-button");
    const emojiPicker = document.getElementById("emoji-picker");
    const messageInput = document.getElementById("chat-message-input");

    emojiButton.addEventListener("click", function () {
        // Toggle emoji picker visibility
        emojiPicker.style.display = emojiPicker.style.display === "none" ? "block" : "none";
    });

    emojiPicker.addEventListener("emoji-click", event => {
        const emoji = event.detail.unicode; // Get the selected emoji
        messageInput.value += emoji; // Append emoji to the input field
    });

    // Hide the emoji picker if clicking outside
    document.addEventListener("click", function (event) {
        if (!emojiButton.contains(event.target) && !emojiPicker.contains(event.target)) {
            emojiPicker.style.display = "none";
        }
    });
}


);
