// Configuration Management - Defaulting to test session details
let config = {
    token: "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMTl81cm1HcHNlUHpOemQ3YzlON0tGbHhYUWlCVE0xdlkzUHpIUlBVLUk0In0.eyJleHAiOjE3NjkwMDQ5MjEsImlhdCI6MTc2ODk2ODkyMSwianRpIjoiN2MyNmNjZjctNmI1MC00YmY4LWE5ODktMzA2MzY4OGQ4Njc1IiwiaXNzIjoiaHR0cHM6Ly92NC1ub25wcm9kLWF1dGguc2ltcGxpZnlzYW5kYm94Lm5ldC9yZWFsbXMvcWEtaGVhbHRoY2FyZSIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiIwMTUwNGM3OC1mNTFmLTRiYzYtOTI3Zi03YjcxMmEyNDA0YzAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzaW1wbGlmeS1hdXRoLXNlcnZpY2UiLCJzaWQiOiJmODdkYjg2MC02YmFmLTQxNjktOWM5MC1lNjIzYThmZGI4YmEiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFhLWhlYWx0aGNhcmUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctdXNlcnMiLCJxdWVyeS1ncm91cHMiLCJxdWVyeS11c2VycyJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJzaW1wbGlmeS1hdXRoIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlcl91c2VybmFtZSI6InNpZGRodWdhZGFraDU3NitkZXdpZDAxQGdtYWlsLmNvbSIsImNsaWVudF90eXBlIjoiaW50ZXJuYWwiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzaWRkaHVnYWRha2g1NzYrZGV3aWQwMUBnbWFpbC5jb20ifQ.FGhPT0uAXV2M2wxIMaYaIH5bnaD-H3xd2YnZFZX52qN3qh46hryGQ4FElcg1xytsyAbbFrlq9y5U7Sl1MSKfa9ON9caxCzG77uCQbkVv5CTC1uAUj-iNNDlaqh_OMdrVi8nvJ88u-gVrz8NatFLJAZCHKzYW2piaHbLbAiS0xQkcYW_uWc96un1ud_STCIbmZzkXBzPuTBR_VGujUN3KjjV2qjJSlnetlk7TxNu_HQbv9OancVm_pYCM4vzTquASl0BhbGMaOni14PfBAJ_AX8Zn57SKj_4EHyNxhY-h1mMHSuSHJMSbsQFEjDH3GvSR0OBwf37u1GBVkHIRJ2_aoA",
    userId: "user-6",
    programId: "388d51a8-6416-4852-83ec-d040b7b11518",
    sessionId: null,
    apiBaseUrl: "http://127.0.0.1:8000/api/v1"
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
const chatHistoryList = document.getElementById('chat-history');

// Initialize logic
async function initApp() {
    // 1. Try to restore session from local storage or create new
    const savedSession = localStorage.getItem('simi_current_session');

    // Refresh session list
    await loadSessionList();

    if (savedSession) {
        console.log("Restoring session:", savedSession);
        config.sessionId = savedSession;
        // Load history for this session
        await loadChatHistory(savedSession);
    } else {
        // Create a new session automatically if none exists
        await startNewSession();
    }

    // UI Init
    document.getElementById('token-input').value = config.token;
    document.getElementById('program-id-input').value = config.programId;
    document.getElementById('user-id-input').value = config.userId;
}

// --- API Wrappers ---

async function apiStartChat(userId) {
    const res = await fetch(`${config.apiBaseUrl}/start-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
    });
    return await res.json();
}

async function apiGetSessions(userId) {
    const res = await fetch(`${config.apiBaseUrl}/sessions/${userId}`);
    return await res.json();
}

async function apiGetHistory(sessionId) {
    const res = await fetch(`${config.apiBaseUrl}/history/${sessionId}`);
    return await res.json();
}

// --- Session Management Functions ---

async function startNewSession() {
    try {
        const data = await apiStartChat(config.userId);
        config.sessionId = data.session_id;
        localStorage.setItem('simi_current_session', config.sessionId);

        // Clear UI
        messagesContainer.innerHTML = '';
        welcomeScreen.style.display = 'block';

        // Refresh sidebar
        await loadSessionList();

        console.log("New Session Started:", config.sessionId);
    } catch (e) {
        console.error("Failed to start session:", e);
        // Don't alert here to avoid spam if called multiple times, but log it
    }
}

async function loadSessionList() {
    try {
        const data = await apiGetSessions(config.userId);
        renderSessionList(data.sessions);
    } catch (e) {
        console.error("Failed to load sessions:", e);
    }
}

function renderSessionList(sessions) {
    if (!chatHistoryList) return;
    chatHistoryList.innerHTML = '<div class="history-label">Previous Chats</div>';

    const sorted = [...sessions].reverse();

    sorted.forEach(session => {
        const item = document.createElement('div');
        item.className = `history-item ${session.session_id === config.sessionId ? 'active' : ''}`;

        // Main click switches session
        item.onclick = (e) => {
            // Prevent switch if clicking menu
            if (e.target.closest('.session-menu-btn') || e.target.closest('.session-menu-dropdown')) return;
            switchSession(session.session_id);
        };

        item.innerHTML = `
            <i class="far fa-message"></i>
            <span>${session.title || session.session_id}</span>
            <button class="session-menu-btn" title="Options" onclick="toggleSessionMenu(event, '${session.session_id}')">
                <i class="fas fa-ellipsis-v"></i>
            </button>
            <div class="session-menu-dropdown" id="menu-${session.session_id}">
                <button onclick="deleteSession('${session.session_id}', event)">
                    <i class="fas fa-trash-alt"></i> Delete
                </button>
            </div>
        `;
        chatHistoryList.appendChild(item);
    });
}

window.toggleSessionMenu = function (e, sessionId) {
    e.stopPropagation();
    // Close others
    document.querySelectorAll('.session-menu-dropdown').forEach(el => {
        if (el.id !== `menu-${sessionId}`) el.classList.remove('show');
    });

    const menu = document.getElementById(`menu-${sessionId}`);
    if (menu) {
        menu.classList.toggle('show');
        const btn = e.currentTarget;
        btn.classList.toggle('active');
    }
};

window.deleteSession = async function (sessionId, e) {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this chat session?')) return;

    try {
        const response = await fetch(`${config.apiBaseUrl}/sessions/${sessionId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Check if we deleted the current session
            if (config.sessionId === sessionId) {
                // Clear current session
                localStorage.removeItem('simi_current_session');
                config.sessionId = null;
                messagesContainer.innerHTML = '';
                welcomeScreen.style.display = 'block';
            }
            // Refresh list
            await loadSessionList();
        } else {
            alert("Failed to delete session.");
        }
    } catch (err) {
        console.error("Delete error:", err);
        alert("Error deleting session.");
    }
};

// Close menus when clicking outside
window.addEventListener('click', () => {
    document.querySelectorAll('.session-menu-dropdown').forEach(el => el.classList.remove('show'));
    document.querySelectorAll('.session-menu-btn').forEach(el => el.classList.remove('active'));
});

async function switchSession(sessionId) {
    if (config.sessionId === sessionId) return;

    config.sessionId = sessionId;
    localStorage.setItem('simi_current_session', sessionId);

    // Update active class in sidebar
    document.querySelectorAll('.history-item').forEach(el => el.classList.remove('active'));
    // We would re-render list to set active, or just find it. Re-rendering is easier.
    loadSessionList(); // To update active state visually

    await loadChatHistory(sessionId);
}

async function loadChatHistory(sessionId) {
    messagesContainer.innerHTML = '';
    welcomeScreen.style.display = 'none'; // Hide welcome by default when loading history

    updateStatus("Loading history...");
    try {
        const data = await apiGetHistory(sessionId);
        const messages = data.messages || [];

        clearStatus();

        if (messages.length === 0) {
            welcomeScreen.style.display = 'block';
        } else {
            welcomeScreen.style.display = 'none';
            messages.forEach(pair => {
                // New format: { "user": "...", "ai": "..." }
                if (pair.user) {
                    appendMessage('user', pair.user, false);
                }
                if (pair.ai) {
                    appendMessage('ai', pair.ai, false);
                }
            });
            scrollToBottom();
        }
    } catch (e) {
        clearStatus();
        console.error("Error loading history", e);
        messagesContainer.innerHTML = '<div class="error-msg">Failed to load history</div>';
    }
}

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

    // ensure session exists
    if (!config.sessionId) {
        try {
            await startNewSession();
        } catch (e) {
            console.error("Autostart session failed", e);
        }
    }

    if (!config.sessionId) {
        clearStatus();
        appendMessage('ai', 'Error: Could not start chat session. Please try "New Chat" or check connection.');
        return;
    }

    try {
        const response = await fetch(`${config.apiBaseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'token': config.token,
                'programId': config.programId
            },
            body: JSON.stringify({
                message: text,
                userId: config.userId,
                sessionId: config.sessionId
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

function appendMessage(role, content, autoScroll = true) {
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
    if (autoScroll) scrollToBottom();
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

newChatBtn.onclick = async (e) => {
    e.preventDefault();
    await startNewSession();
};

// --- New Header Action Buttons ---
const resetSessionBtn = document.getElementById('reset-session-btn');
const clearChatBtn = document.getElementById('clear-chat-btn');

// Clear Chat (UI Only) - Same as New Chat
if (clearChatBtn) {
    clearChatBtn.onclick = newChatBtn.onclick;
}

// Reset Session (Backend + UI)
// NOTE: This resets the entire user memory, not just a session. 
// We might want to change this to delete the current session instead?
// For now, keeping as is but maybe we should alias it to deleteSession
if (resetSessionBtn) {
    resetSessionBtn.onclick = async (e) => {
        e.preventDefault();

        const originalIcon = resetSessionBtn.innerHTML;
        resetSessionBtn.innerHTML = '<i class="fas fa-spin fa-sync-alt"></i>';
        resetSessionBtn.disabled = true;

        try {
            // For now calling reset still
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
                messagesContainer.innerHTML = '';
                messagesContainer.appendChild(welcomeScreen);
                welcomeScreen.style.display = 'block';
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

    // Check for JSON with ui_action
    if (content.includes('ui_action') && content.includes('show_completion_buttons')) {
        try {
            const firstBrace = content.indexOf('{');
            const lastBrace = content.lastIndexOf('}');

            if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
                const potentialJson = content.substring(firstBrace, lastBrace + 1);
                const data = JSON.parse(potentialJson);

                if (data.ui_action === "show_completion_buttons" && data.draft_data) {
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
        const listMatch = line.match(/^\s*[-*?]\s+(.*)/) || line.match(/Option:\s*(.*)/i);

        if (listMatch) {
            const optionText = listMatch[1].trim().replace(/<\/?[^>]+(>|$)/g, "");
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

// Start App
initApp();
