// Configuration Management - Defaulting to test session details
let config = {
    token: "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMTl81cm1HcHNlUHpOemQ3YzlON0tGbHhYUWlCVE0xdlkzUHpIUlBVLUk0In0.eyJleHAiOjE3Njg2MDE1NDgsImlhdCI6MTc2ODU2NTU0OCwianRpIjoiYTc3NDc2MjItMjlmYS00MmRhLWJjNTgtYmJhYjg2MzVmYWVkIiwiaXNzIjoiaHR0cHM6Ly92NC1ub25wcm9kLWF1dGguc2ltcGxpZnlzYW5kYm94Lm5ldC9yZWFsbXMvcWEtaGVhbHRoY2FyZSIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiJlNDc5NWM0Ni1kMDUxLTQxYWItYjNjYS1hNGE0YWUzNDg0ZDAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzaW1wbGlmeS1hdXRoLXNlcnZpY2UiLCJzaWQiOiIwNWM3NzkyMy0wZjcyLTRjMTEtYTEzOC1hZGYyM2RjMTUxMGQiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFhLWhlYWx0aGNhcmUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbImltcGVyc29uYXRpb24iLCJ2aWV3LXVzZXJzIiwicXVlcnktZ3JvdXBzIiwicXVlcnktdXNlcnMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoic2ltcGxpZnktYXV0aCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInByZWZlcnJlcl91c2VybmFtZSI6ImFkbWluIiwiY2xpZW50X3R5cGUiOiJpbnRlcm5hbCIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwidXNlclR5cGUiOiJzdXBlcl91c2VyIn0.c_IFeG6p0oNW4pNuWjEOVh5vBn2kwNbkT4I7rKGTl9XaEm9hy486u6MMbhsTHcNkoGrtu8-ALVd8lML6KZ8BxBBtdyKu4kzt5zWPv1t-k8a40wWsW2HHmIZdtidHOnejEWJNcddLdeqn-PLPw4bkefOtecr8Pj1jqeo7_KRhPEgHjyAxSTF-FOw9-Yzasv1kVqpdi6lBgnTZOdHJg_pSzmlHpCWFFi-PNJR6lcLZUpUayl29SWe1QTfa6QEop79l2rfIl1tHfjnLYc3WCg42-qHdfOnCQ0MJuDNxHbiMKiv1OMFF37z5VFY_VAzYwYfRpsOfKT3XNxY6KtnhQxAXUA",
    userId: "user-456",
    programId: "388d51a8-6416-4852-83ec-d040b7b11518"
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

// Status Indicator Helpers
function updateStatus(text) {
    let statusEl = document.getElementById('status-indicator');
    if (!statusEl) {
        statusEl = document.createElement('div');
        statusEl.id = 'status-indicator';
        statusEl.className = 'status-msg';
        statusEl.innerHTML = `
            <div class="status-content">
                <i class="fas fa-circle-notch fa-spin"></i>
                <span id="status-text">${text}</span>
            </div>
        `;
        messagesContainer.appendChild(statusEl);
    } else {
        const textEl = document.getElementById('status-text');
        if (textEl) textEl.innerText = text;
    }
    scrollToBottom();
}

function clearStatus() {
    const statusEl = document.getElementById('status-indicator');
    if (statusEl) statusEl.remove();
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

    // Initial Status
    updateStatus("Thinking...");

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

        if (!response.ok) {
            clearStatus();
            appendMessage('ai', 'Error: Failed to connect to server.');
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // Process complete messages separated by \n\n
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // Keep incomplete chunk

            for (const line of lines) {
                if (line.startsWith('status:')) {
                    updateStatus(line.substring(7));
                } else if (line.startsWith('result:')) {
                    clearStatus();
                    appendMessage('ai', line.substring(7));
                } else if (line.startsWith('error:')) {
                    clearStatus();
                    appendMessage('ai', '❌ Error: ' + line.substring(6));
                }
                scrollToBottom();
            }
        }
    } catch (error) {
        clearStatus();
        appendMessage('ai', 'Connection Error: Make sure your FastAPI server is running.');
        console.error(error);
    } finally {
        // Ensure status is gone if something broke loops
    }
}

function scrollToBottom() {
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
    scrollToBottom();
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
    welcomeScreen.style.display = 'block';
};

// --- New Header Action Buttons ---
const resetSessionBtn = document.getElementById('reset-session-btn');
const clearChatBtn = document.getElementById('clear-chat-btn');

// Clear Chat (UI Only) - Same as New Chat
if (clearChatBtn) {
    clearChatBtn.onclick = newChatBtn.onclick;
}

// Reset Session (Backend + UI)
if (resetSessionBtn) {
    resetSessionBtn.onclick = async (e) => {
        e.preventDefault();

        // Visual feedback
        const originalIcon = resetSessionBtn.innerHTML;
        resetSessionBtn.innerHTML = '<i class="fas fa-spin fa-sync-alt"></i>';
        resetSessionBtn.disabled = true;

        try {
            const response = await fetch('http://localhost:8000/api/v1/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: config.userId
                })
            });

            if (response.ok) {
                // Clear UI as well
                messagesContainer.innerHTML = '';
                messagesContainer.appendChild(welcomeScreen);
                welcomeScreen.style.display = 'block';
                // Optional: Show a toast? For now just reset UI is clear enough.
            } else {
                alert("Failed to reset session on server.");
            }
        } catch (error) {
            console.error("Reset Error:", error);
            alert("Connection error during reset.");
        } finally {
            resetSessionBtn.innerHTML = originalIcon;
            resetSessionBtn.disabled = false;
        }
    };
}

function formatContent(content) {
    if (!content) return '';

    // Check for JSON with ui_action (sent by submit_job tool)
    // We look for the string "ui_action" and then attempt to parse the widest possible JSON block
    if (content.includes('ui_action') && content.includes('show_completion_buttons')) {
        try {
            const firstBrace = content.indexOf('{');
            const lastBrace = content.lastIndexOf('}');

            if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
                const potentialJson = content.substring(firstBrace, lastBrace + 1);
                const data = JSON.parse(potentialJson);

                if (data.ui_action === "show_completion_buttons" && data.draft_data) {
                    // Replace the JSON part with the rendered summary, keeping any preceding text
                    const textBefore = content.substring(0, firstBrace);
                    const textAfter = content.substring(lastBrace + 1);
                    return formatContent(textBefore) + renderSummary(data.draft_data) + formatContent(textAfter);
                }
            }
        } catch (e) {
            console.error("JSON parse error in summary detection", e);
        }
    }

    // Check if the content is a JSON Summary (legacy fallback)
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
    return `
        <div class="job-summary-card">
            <h3>Ready to Create Job?</h3>
            <p>We have collected all the necessary details. Click below to simply create the vacancy.</p>
            <button class="create-job-btn" onclick='createJob()'>
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
            },
            body: JSON.stringify({
                userId: config.userId
            })
        });

        const result = await response.json();
        if (response.ok) {
            appendMessage('ai', '🎉 **Success!** Your job vacancy has been created successfully!');
            console.log("VMS Response:", result.vms_response);
            btn.innerHTML = '<i class="fas fa-check"></i> Job Created';
        } else {
            appendMessage('ai', '❌ **Error:** ' + (result.detail || 'Failed to create job.'));
            btn.innerHTML = '<i class="fas fa-rocket"></i> Create Vacancy Now';
            btn.disabled = false;
        }
    } catch (error) {
        console.error("Network Error:", error);
        appendMessage('ai', '🚫 **Connection Error:** Could not reach the API.');
        btn.innerHTML = '<i class="fas fa-rocket"></i> Create Vacancy Now';
        btn.disabled = false;
    }
};
