// ==================== Configuration ====================
const API_BASE_URL = window.location.origin + '/api';
let currentSessionId = null;
let currentFile = null;
let messageCount = 0;

// ==================== DOM Elements ====================
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadBtn = document.getElementById('uploadBtn');
const sendBtn = document.getElementById('sendBtn');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');
const welcomeScreen = document.getElementById('welcomeScreen');
const inputArea = document.getElementById('inputArea');
const documentInfo = document.getElementById('documentInfo');
const sessionIdDisplay = document.getElementById('sessionId');
const sessionStatus = document.getElementById('sessionStatus');
const messageCountDisplay = document.getElementById('messageCount');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const newSessionBtn = document.getElementById('newSessionBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

// ==================== Utility Functions ====================
function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function formatTime() {
    return new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const iconSvg = {
        success: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="20 6 9 17 4 12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        error: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="2"/><line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/><line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/></svg>',
        info: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="2"/><line x1="12" y1="16" x2="12" y2="12" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="8" x2="12.01" y2="8" stroke-width="2" stroke-linecap="round"/></svg>'
    };
    
    toast.innerHTML = `
        <div class="toast-icon">${iconSvg[type]}</div>
        <div class="toast-message">${message}</div>
    `;
    
    document.getElementById('toastContainer').appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function showLoading(show = true) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

function updateSessionInfo() {
    if (currentSessionId) {
        sessionIdDisplay.textContent = currentSessionId.substring(0, 20) + '...';
        sessionIdDisplay.title = currentSessionId;
        sessionStatus.textContent = 'Active';
        sessionStatus.className = 'status-badge status-active';
    } else {
        sessionIdDisplay.textContent = 'Not started';
        sessionStatus.textContent = 'Inactive';
        sessionStatus.className = 'status-badge status-inactive';
    }
    messageCountDisplay.textContent = messageCount;
}

function enableChat() {
    welcomeScreen.style.display = 'none';
    chatMessages.style.display = 'flex';
    inputArea.style.display = 'block';
    sendBtn.disabled = false;
}

// ==================== File Upload ====================
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            fileInput.files = files;
            handleFileSelect();
        } else {
            showToast('Please upload a PDF file', 'error');
        }
    }
});

fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect() {
    const file = fileInput.files[0];
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
        showToast('Please select a PDF file', 'error');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showToast('File size must be less than 10MB', 'error');
        return;
    }
    
    currentFile = file;
    uploadArea.classList.add('has-file');
    uploadArea.innerHTML = `
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="14 2 14 8 20 8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p><strong>${file.name}</strong></p>
        <p style="font-size: 12px; color: #48bb78;">Ready to upload</p>
    `;
    uploadBtn.disabled = false;
}

uploadBtn.addEventListener('click', async () => {
    if (!currentFile) return;
    
    // Generate session ID if not exists
    if (!currentSessionId) {
        currentSessionId = generateSessionId();
        updateSessionInfo();
    }
    
    const formData = new FormData();
    formData.append('file', currentFile);
    formData.append('session_id', currentSessionId);
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }
        
        showToast(`Successfully processed ${data.filename}`, 'success');
        
        // Update document info
        documentInfo.innerHTML = `
            <p><strong>File:</strong> ${data.filename}</p>
            <p><strong>Pages:</strong> ${data.pages}</p>
            <p><strong>Chunks:</strong> ${data.chunks}</p>
            <p style="color: var(--success-color); margin-top: 8px;">✓ Ready to chat</p>
        `;
        
        // Enable chat
        enableChat();
        
        // Disable upload button
        uploadBtn.disabled = true;
        
    } catch (error) {
        console.error('Upload error:', error);
        showToast(error.message || 'Failed to upload PDF', 'error');
    } finally {
        showLoading(false);
    }
});

// ==================== Chat Functions ====================
function addMessage(role, text, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatarIcon = role === 'user' 
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="7" r="4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="message-sources">
                <strong>Sources:</strong>
                <ul>
                    ${sources.map(source => `<li>${source}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar ${role}-avatar">
            ${avatarIcon}
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-role">${role === 'user' ? 'You' : 'Assistant'}</span>
                <span class="message-time">${formatTime()}</span>
            </div>
            <div class="message-text">${text}</div>
            ${sourcesHtml}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    messageCount++;
    updateSessionInfo();
}

function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar assistant-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 2L2 7l10 5 10-5-10-5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function sendMessage() {
    const prompt = messageInput.value.trim();
    if (!prompt || !currentSessionId) return;
    
    // Add user message
    addMessage('user', prompt);
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable input while processing
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    // Show typing indicator
    addTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                session_id: currentSessionId
            })
        });
        
        const data = await response.json();
        
        removeTypingIndicator();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to get response');
        }
        
        // Add assistant message
        addMessage('assistant', data.answer, data.sources);
        
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        showToast(error.message || 'Failed to send message', 'error');
        addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.');
    } finally {
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// ==================== Input Handling ====================
sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

messageInput.addEventListener('input', () => {
    // Auto-resize textarea
    messageInput.style.height = 'auto';
    messageInput.style.height = messageInput.scrollHeight + 'px';
});

// ==================== Session Management ====================
clearHistoryBtn.addEventListener('click', async () => {
    if (!currentSessionId) {
        showToast('No active session', 'info');
        return;
    }
    
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${currentSessionId}/clear-history`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to clear history');
        }
        
        chatMessages.innerHTML = '';
        messageCount = 0;
        updateSessionInfo();
        showToast('Chat history cleared', 'success');
        
    } catch (error) {
        console.error('Clear history error:', error);
        showToast('Failed to clear history', 'error');
    }
});

newSessionBtn.addEventListener('click', () => {
    if (currentSessionId && !confirm('Start a new session? This will clear current chat.')) {
        return;
    }
    
    // Reset everything
    currentSessionId = null;
    currentFile = null;
    messageCount = 0;
    
    fileInput.value = '';
    uploadBtn.disabled = true;
    sendBtn.disabled = true;
    
    uploadArea.classList.remove('has-file');
    uploadArea.innerHTML = `
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p>Drop PDF here or click to upload</p>
    `;
    
    documentInfo.innerHTML = '<p class="text-muted">No document uploaded</p>';
    chatMessages.innerHTML = '';
    
    welcomeScreen.style.display = 'flex';
    chatMessages.style.display = 'none';
    inputArea.style.display = 'none';
    
    updateSessionInfo();
    showToast('Started new session', 'success');
});

// ==================== Health Check ====================
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('✅ API is healthy');
        } else {
            console.warn('⚠️ API health check failed:', data);
            showToast('API connection issues detected', 'error');
        }
    } catch (error) {
        console.error('❌ Health check failed:', error);
        showToast('Cannot connect to API', 'error');
    }
}

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 RAG Chatbot initialized');
    updateSessionInfo();
    checkHealth();
    
    // Focus on message input if chat is enabled
    if (inputArea.style.display === 'block') {
        messageInput.focus();
    }
});
