/**
 * PSG NEXUS - Client-Side Intelligent Chatbot & Cross-Page Persistence Engine
 * Position: Bottom-Left | Default Role: Student (with all roles switchable)
 * Local MongoDB Storage enabled via Express /api/chat
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const launcher = document.getElementById('psg-chatbot-launcher');
  const chatWindow = document.getElementById('psg-chatbot-window');
  const closeBtn = document.getElementById('psg-close-chat-btn');
  const minimizeBtn = document.getElementById('psg-minimize-chat-btn');
  const chatBody = document.getElementById('psg-chat-body');
  const chatForm = document.getElementById('psg-chat-form');
  const chatInput = document.getElementById('psg-chat-input');
  const roleBadge = document.getElementById('psg-active-role-badge');
  const switchRoleBtn = document.getElementById('psg-switch-role-btn');
  const roleModalContainer = document.getElementById('psg-role-modal-container');

  // State in Memory: Student is default!
  let activeRole = sessionStorage.getItem('psg_chat_role') || 'student';
  let userDetails = JSON.parse(sessionStorage.getItem('psg_chat_details') || '{"rollNo":"26MX101","dept":"Computer Applications"}');
  let messages = JSON.parse(sessionStorage.getItem('psg_chat_messages') || '[]');
  let isOpen = sessionStorage.getItem('psg_chat_isOpen') === 'true';

  // =========================================================================
  // INITIALIZATION ON PAGE LOAD
  // =========================================================================
  function initChatbot() {
    updateRoleBadge();

    if (messages.length === 0) {
      addInitialWelcomeMessage();
    } else {
      renderAllMessages();
    }

    if (isOpen) {
      openChat();
    }
  }

  // =========================================================================
  // OPEN / CLOSE TOGGLE
  // =========================================================================
  function openChat() {
    chatWindow.classList.remove('hidden');
    isOpen = true;
    sessionStorage.setItem('psg_chat_isOpen', 'true');
    scrollToBottom();
    setTimeout(() => chatInput.focus(), 200);
  }

  function closeChat() {
    chatWindow.classList.add('hidden');
    isOpen = false;
    sessionStorage.setItem('psg_chat_isOpen', 'false');
  }

  launcher.addEventListener('click', () => {
    if (chatWindow.classList.contains('hidden')) {
      openChat();
    } else {
      closeChat();
    }
  });

  if (closeBtn) closeBtn.addEventListener('click', closeChat);
  if (minimizeBtn) minimizeBtn.addEventListener('click', closeChat);

  // =========================================================================
  // ROLE MANAGEMENT (Student default, all roles switchable)
  // =========================================================================
  function updateRoleBadge() {
    roleBadge.textContent = activeRole.toUpperCase();
    sessionStorage.setItem('psg_chat_role', activeRole);
  }

  function showRoleSelector() {
    if (!roleModalContainer) return;
    roleModalContainer.style.display = 'block';
    roleModalContainer.innerHTML = `
      <div class="psg-role-selector-card">
        <h5>Institutional Role Selector</h5>
        <div class="small text-muted">Currently active: <strong>${activeRole.toUpperCase()}</strong>. You can switch to test role permissions:</div>
        <div class="psg-role-grid">
          <button type="button" class="psg-role-item-btn ${activeRole === 'student' ? 'active' : ''}" data-role="student">👨‍🎓 Student</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'faculty' ? 'active' : ''}" data-role="faculty">👨‍🏫 Faculty / Staff</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'parent' ? 'active' : ''}" data-role="parent">👨‍👩‍👧 Parent</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'visitor' ? 'active' : ''}" data-role="visitor">🌐 Visitor / Alumni</button>
        </div>
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-outline-secondary" id="psg-cancel-role-switch">Done</button>
        </div>
      </div>
    `;

    const btns = roleModalContainer.querySelectorAll('.psg-role-item-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        activeRole = btn.getAttribute('data-role');
        updateRoleBadge();
        roleModalContainer.style.display = 'none';

        // Add a notification in chat
        appendBotMessage(`Switched active session to **${activeRole.toUpperCase()}**. Responses and document permissions are now tailored to this role.`);
      });
    });

    document.getElementById('psg-cancel-role-switch')?.addEventListener('click', () => {
      roleModalContainer.style.display = 'none';
    });
  }

  if (switchRoleBtn) {
    switchRoleBtn.addEventListener('click', () => {
      if (roleModalContainer.style.display === 'block') {
        roleModalContainer.style.display = 'none';
      } else {
        showRoleSelector();
      }
    });
  }

  // =========================================================================
  // MESSAGE RENDERING & SESSION PERSISTENCE
  // =========================================================================
  function addInitialWelcomeMessage() {
    let welcomeText = `Hello! I am **PSG Nexus**, your official AI campus assistant for PSG College of Technology.\n\nI am here to guide you with syllabus details, examination rules, hostel timings, fees, and campus navigation.`;

    const defaultChips = [
      'Take me to form filling page',
      'What is the minimum attendance?',
      'Continuous Assessment marks',
      'Hostel in-times',
      'Show B.E. / MCA Syllabus'
    ];

    appendBotMessage(welcomeText, 'normal', null, null, defaultChips);
  }

  function appendUserMessage(text) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgObj = {
      sender: 'user',
      text: text,
      time: timeStr
    };
    messages.push(msgObj);
    saveMessagesToStorage();
    renderSingleMessage(msgObj);
    scrollToBottom();
  }

  function appendBotMessage(text, status = 'normal', redirectUrl = null, redirectName = null, chips = []) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgObj = {
      sender: 'bot',
      text: text,
      time: timeStr,
      status: status,
      redirectUrl: redirectUrl,
      redirectName: redirectName,
      chips: chips
    };
    messages.push(msgObj);
    saveMessagesToStorage();
    renderSingleMessage(msgObj);
    scrollToBottom();
  }

  function renderAllMessages() {
    chatBody.innerHTML = '';
    if (roleModalContainer) {
      chatBody.appendChild(roleModalContainer);
    }
    messages.forEach(msg => renderSingleMessage(msg));
    scrollToBottom();
  }

  function renderSingleMessage(msg) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `psg-message ${msg.sender} ${msg.status || ''}`;

    let formattedText = escapeHtml(msg.text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');

    let redirectHtml = '';
    if (msg.redirectUrl) {
      redirectHtml = `
        <div class="psg-redirect-banner">
          <div class="psg-redirect-spinner"></div>
          <div>
            <strong>Navigating:</strong> Opening ${escapeHtml(msg.redirectName || msg.redirectUrl)}...
          </div>
        </div>
      `;
    }

    let chipsHtml = '';
    if (msg.chips && msg.chips.length > 0) {
      chipsHtml = `<div class="psg-quick-chips">`;
      msg.chips.forEach(chip => {
        chipsHtml += `<button type="button" class="psg-chip" data-chip="${escapeHtml(chip)}">${escapeHtml(chip)}</button>`;
      });
      chipsHtml += `</div>`;
    }

    msgDiv.innerHTML = `
      <div class="psg-bubble">
        <div>${formattedText}</div>
        ${redirectHtml}
      </div>
      <div class="psg-msg-time">${msg.time}</div>
      ${chipsHtml}
    `;

    // Chip click handler
    const chipBtns = msgDiv.querySelectorAll('.psg-chip');
    chipBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-chip');
        handleUserQuery(query);
      });
    });

    chatBody.appendChild(msgDiv);
  }

  function saveMessagesToStorage() {
    sessionStorage.setItem('psg_chat_messages', JSON.stringify(messages));
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatBody.scrollTop = chatBody.scrollHeight;
    }, 50);
  }

  function escapeHtml(text) {
    if (!text) return '';
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }

  // =========================================================================
  // TYPING INDICATOR
  // =========================================================================
  let typingElement = null;

  function showTypingIndicator() {
    if (typingElement) return;
    typingElement = document.createElement('div');
    typingElement.className = 'psg-message bot';
    typingElement.innerHTML = `
      <div class="psg-typing-indicator">
        <div class="psg-typing-dot"></div>
        <div class="psg-typing-dot"></div>
        <div class="psg-typing-dot"></div>
      </div>
    `;
    chatBody.appendChild(typingElement);
    scrollToBottom();
  }

  function hideTypingIndicator() {
    if (typingElement) {
      typingElement.remove();
      typingElement = null;
    }
  }

  // =========================================================================
  // QUERY HANDLING & MONGODB SYNC
  // =========================================================================
  async function handleUserQuery(query) {
    if (!query || query.trim() === '') return;

    appendUserMessage(query);
    showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          role: activeRole,
          userDetails: userDetails,
          currentPage: window.location.pathname
        })
      });

      const data = await response.json();
      hideTypingIndicator();

      appendBotMessage(
        data.reply,
        data.status,
        data.redirectUrl,
        data.redirectName,
        data.suggestedQuestions || []
      );

      // AUTOMATIC REDIRECTION
      if (data.redirectUrl && data.redirectUrl !== window.location.pathname) {
        sessionStorage.setItem('psg_chat_isOpen', 'true');
        saveMessagesToStorage();

        setTimeout(() => {
          window.location.href = data.redirectUrl;
        }, data.redirectDelay || 1800);
      }

    } catch (error) {
      hideTypingIndicator();
      appendBotMessage(
        '⚠️ Could not connect to the campus server. Please verify your Node.js server is running.',
        'error'
      );
    }
  }

  // Form Submit Listener
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (query) {
      chatInput.value = '';
      handleUserQuery(query);
    }
  });

  // Clear Chat History Button
  const resetChatBtn = document.getElementById('psg-reset-chat-btn');
  if (resetChatBtn) {
    resetChatBtn.addEventListener('click', () => {
      if (confirm('Clear conversation history?')) {
        messages = [];
        sessionStorage.removeItem('psg_chat_messages');
        renderAllMessages();
        addInitialWelcomeMessage();
      }
    });
  }

  // Run initial setup
  initChatbot();
});
