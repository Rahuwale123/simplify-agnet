// Configuration Management - Defaulting to test session details
let config = {
    token: "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMTl81cm1HcHNlUHpOemQ3YzlON0tGbHhYUWlCVE0xdlkzUHpIUlBVLUk0In0.eyJleHAiOjE3NjgzNDAzMDgsImlhdCI6MTc2ODMwNDMwOCwianRpIjoiY2U0MTUzZWUtMzYzNy00NGQwLWI3ZmYtNjYyZjIyZWNhYjc0IiwiaXNzIjoiaHR0cHM6Ly92NC1ub25wcm9kLWF1dGguc2ltcGxpZnlzYW5kYm94Lm5ldC9yZWFsbXMvcWEtaGVhbHRoY2FyZSIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiIwMTUwNGM3OC1mNTFmLTRiYzYtOTI3Zi03YjcxMmEyNDA0YzAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzaW1wbGlmeS1hdXRoLXNlcnZpY2UiLCJzaWQiOiIzYWU4ZGIxNC0yZmNjLTQ3ZWYtYmFlNC0zNmNlMjBkZWIzYjkiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFhLWhlYWx0aGNhcmUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctdXNlcnMiLCJxdWVyeS1ncm91cHMiLCJxdWVyeS11c2VycyJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJzaW1wbGlmeS1hdXRoIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlcl91c2VybmFtZSI6InNpZGRodWdhZGFraDU3NitkZXdpZDAxQGdtYWlsLmNvbSIsImNsaWVudF90eXBlIjoiaW50ZXJuYWwiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzaWRkaHVnYWRha2g1NzYrZGV3aWQwMUBnbWFpbC5jb20ifQ.W29dzAqozlFwbgRi_kOmbWQsxZKoBbNHSnlBLh8Hyec2tITsnS8nD2L31J6x4qkM8vgSpaLNA4si37i48v_jNJuWi36-HE2ZbqfLZuuWv4vKfyLt_YxFiM78ylVJv3iS2bpxy7_x8OTxLb4JYZxRXXGdPyGZUaGfiywwM29enmQ__2_IVN6NSUeaN4b0U8dGuEjnI4KDA9YQMrlOP3nW0KqMyFD_PqZ60GEx71jPTSzqX_vyKxMH5ybvRpsX5EGMg3lNUfjhGwgTVSEdD9p79wXeIj7i2po5jebTO7Dl4sE_CjtixYcozoVHyTfMa1jIk9vY8dIyoGzUMm7wJ5k7MQ",
    programId: "388d51a8-6416-4852-83ec-d040b7b11518",
    userId: "user-456"
};

// UI Elements
const messagesContainer = document.getElementById('messages-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat');
const welcomeScreen = document.getElementById('welcome-screen');
const modalOverlay = document.getElementById('modal-overlay');
const openSettings = document.getElementById('open-settings');
const closeSettings = document.getElementById('close-settings');
const saveSettings = document.getElementById('save-settings');

// Initialize Modal Inputs
document.getElementById('token-input').value = config.token;
document.getElementById('program-id-input').value = config.programId;
document.getElementById('user-id-input').value = config.userId;

// Auto-resize textarea
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
    sendBtn.disabled = userInput.value.trim() === '';
});

// Settings Modal Logic
openSettings.onclick = () => modalOverlay.style.display = 'flex';
closeSettings.onclick = () => modalOverlay.style.display = 'none';
modalOverlay.onclick = (e) => { if (e.target === modalOverlay) modalOverlay.style.display = 'none'; };

saveSettings.onclick = () => {
    config.token = document.getElementById('token-input').value;
    config.programId = document.getElementById('program-id-input').value;
    config.userId = document.getElementById('user-id-input').value;

    modalOverlay.style.display = 'none';
    alert('Settings Saved (Current Session Only)!');
};

// Chat Functions
function setInput(text) {
    userInput.value = text;
    userInput.dispatchEvent(new Event('input'));
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Clear and reset textarea
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    welcomeScreen.style.display = 'none';

    // Append User Message
    appendMessage('user', text);

    // Append Typing Indicator
    const typingId = appendTypingIndicator();

    try {
        const response = await fetch('http://localhost:8000/api/v1/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'token': config.token,
                'programId': config.programId
            },
            body: JSON.stringify({
                message: text,
                userId: config.userId
            })
        });

        const data = await response.json();
        removeElement(typingId);

        if (response.ok) {
            appendMessage('ai', data.content);
        } else {
            appendMessage('ai', 'Error: ' + (data.detail || 'Failed to get response from server. Check your settings and API server status.'));
        }
    } catch (error) {
        removeElement(typingId);
        appendMessage('ai', 'Connection Error: Make sure your FastAPI server is running at http://localhost:8000');
        console.error(error);
    }
}

function appendMessage(role, content) {
    const row = document.createElement('div');
    row.className = `message-row ${role}-msg`;

    const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
    const avatarClass = role === 'user' ? 'user-avatar' : 'ai-avatar';

    row.innerHTML = `
        <div class="message-content">
            <div class="message-avatar ${avatarClass}">
                <i class="fas ${avatarIcon}"></i>
            </div>
            <div class="text">${formatContent(content)}</div>
        </div>
    `;

    messagesContainer.appendChild(row);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function appendTypingIndicator() {
    const id = 'typing-' + Date.now();
    const row = document.createElement('div');
    row.className = 'message-row ai-msg';
    row.id = id;

    row.innerHTML = `
        <div class="message-content">
            <div class="message-avatar ai-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(row);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// Event Listeners
sendBtn.onclick = (e) => {
    e.preventDefault();
    sendMessage();
};

userInput.onkeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
};

newChatBtn.onclick = (e) => {
    e.preventDefault();
    messagesContainer.innerHTML = '';
    messagesContainer.appendChild(welcomeScreen);
    welcomeScreen.style.display = 'block';
};

function formatContent(content) {
    if (!content) return '';

    // Check if the content is a JSON Summary (sent when workflow is complete)
    if (content.includes('```json') && content.includes('"job_title"')) {
        try {
            const jsonStr = content.match(/```json\n([\s\S]*?)\n```/)[1];
            const data = JSON.parse(jsonStr);
            return renderSummary(data);
        } catch (e) {
            console.error("JSON parse error in summary", e);
        }
    }

    // Sanitize slightly and handle bold
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Handle Lists - Normal text but with clickable power
    const lines = formatted.split('\n');
    let htmlResult = [];

    lines.forEach(line => {
        // Match "- Name" or "* Name" or "Option: Name"
        const listMatch = line.match(/^\s*[-*•]\s+(.*)/) || line.match(/Option:\s*(.*)/i);

        if (listMatch) {
            const optionText = listMatch[1].trim().replace(/<\/?[^>]+(>|$)/g, ""); // strip html
            htmlResult.push(`<div class="text-option" onclick="handleOptionClick('${optionText.replace(/'/g, "\\'")}')">• ${listMatch[1]}</div>`);
        } else {
            if (line.trim()) {
                htmlResult.push(`<p>${line}</p>`);
            }
        }
    });

    return htmlResult.join('');
}

function renderSummary(data) {
    let fieldsHtml = '';
    for (const [key, value] of Object.entries(data)) {
        if (value && typeof value !== 'object') {
            const label = key.replace(/_/g, ' ').toUpperCase();
            fieldsHtml += `
                <div class="summary-item">
                    <span class="summary-label">${label}:</span>
                    <span class="summary-value">${value}</span>
                </div>`;
        }
    }

    return `
        <div class="job-summary-card">
            <h3>📋 Final Job Summary</h3>
            <div class="summary-list">
                ${fieldsHtml}
            </div>
            <button class="create-job-btn" onclick="createJob()">
                <i class="fas fa-rocket"></i> Create Vacancy Now
            </button>
        </div>
    `;
}

// Global handler for clicking an option
window.handleOptionClick = function (text) {
    userInput.value = text;
    sendMessage();
};

window.createJob = async function () {
    const btn = document.querySelector('.create-job-btn');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    btn.disabled = true;

    try {
        const response = await fetch('http://localhost:8000/api/v1/jobs/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'token': config.token,
                'programId': config.programId
            }
        });

        const result = await response.json();
        if (response.ok) {
            appendMessage('ai', '🎉 **Success!** Your job vacancy has been created successfully.');
            // Optionally clear history/reset
        } else {
            appendMessage('ai', '❌ **Error:** ' + (result.detail || 'Failed to create job.'));
            btn.innerHTML = '<i class="fas fa-rocket"></i> Create Vacancy Now';
            btn.disabled = false;
        }
    } catch (error) {
        appendMessage('ai', '🚫 **Connection Error:** Could not reach the creation API.');
        btn.innerHTML = '<i class="fas fa-rocket"></i> Create Vacancy Now';
        btn.disabled = false;
    }
};
