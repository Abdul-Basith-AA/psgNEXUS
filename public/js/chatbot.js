/**
 * PSG NEXUS - Official College AI Client-Side Engine
 * Inspired by samp.html: Modern Glassmorphism, Bouncy Transitions & Cross-Page Persistence
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const launcher = document.getElementById('psg-chatbot-launcher');
  const chatWindow = document.getElementById('psg-chatbot-window');
  const closeBtn = document.getElementById('psg-close-chat-btn');
  const resetBtn = document.getElementById('psg-reset-chat-btn');
  const chatMessages = document.getElementById('psg-chat-messages');
  const typingIndicator = document.getElementById('psg-typing-indicator');
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

  // SVG Bot Avatar template for bot messages
  const botAvatarSvg = `
    <div class="psg-msg-avatar">
      <svg viewBox="0 0 100 100">
        <path d="M50 10 L85 25 V50 C85 75 50 90 50 90 C50 90 15 75 15 50 V25 Z" fill="none" stroke="#0a2c66" stroke-width="8"/>
        <circle cx="50" cy="45" r="18" fill="#0066cc"/>
      </svg>
    </div>
  `;

  // =========================================================================
  // 1. INITIALIZATION ON PAGE LOAD
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
  // 2. OPEN / CLOSE TOGGLE (Smooth Bouncy Animation)
  // =========================================================================
  function openChat() {
    chatWindow.classList.remove('chat-hidden');
    chatWindow.classList.add('chat-visible');
    isOpen = true;
    sessionStorage.setItem('psg_chat_isOpen', 'true');

    // Hide notification badge when opened
    const badge = launcher ? launcher.querySelector('.psg-fab-badge') : null;
    if (badge) badge.style.display = 'none';

    scrollToBottom();
    setTimeout(() => {
      if (chatInput) chatInput.focus();
    }, 350);
  }

  function closeChat() {
    chatWindow.classList.remove('chat-visible');
    chatWindow.classList.add('chat-hidden');
    isOpen = false;
    sessionStorage.setItem('psg_chat_isOpen', 'false');
  }

  if (launcher) {
    launcher.addEventListener('click', () => {
      if (chatWindow.classList.contains('chat-visible')) {
        closeChat();
      } else {
        openChat();
      }
    });
  }

  if (closeBtn) closeBtn.addEventListener('click', closeChat);

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) {
      closeChat();
    }
  });

  // =========================================================================
  // 3. ROLE MANAGEMENT (Student default, all roles switchable)
  // =========================================================================
  function updateRoleBadge() {
    if (roleBadge) {
      roleBadge.textContent = activeRole.toUpperCase();
    }
    sessionStorage.setItem('psg_chat_role', activeRole);
  }

  function showRoleSelector() {
    if (!roleModalContainer) return;
    roleModalContainer.style.display = 'block';
    roleModalContainer.innerHTML = `
      <div class="psg-role-selector-card">
        <h5>Institutional Role Selector</h5>
        <div class="text-muted">Active Role: <strong>${activeRole.toUpperCase()}</strong>. Select a role to test contextual permissions:</div>
        <div class="psg-role-grid">
          <button type="button" class="psg-role-item-btn ${activeRole === 'student' ? 'active' : ''}" data-role="student">👨‍🎓 Student</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'faculty' ? 'active' : ''}" data-role="faculty">👨‍🏫 Faculty / Staff</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'parent' ? 'active' : ''}" data-role="parent">👨‍👩‍👧 Parent</button>
          <button type="button" class="psg-role-item-btn ${activeRole === 'visitor' ? 'active' : ''}" data-role="visitor">🌐 Visitor / Alumni</button>
        </div>
        <button type="button" class="psg-role-done-btn" id="psg-cancel-role-switch">Done</button>
        <div style="clear: both;"></div>
      </div>
    `;

    const btns = roleModalContainer.querySelectorAll('.psg-role-item-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        activeRole = btn.getAttribute('data-role');
        updateRoleBadge();
        roleModalContainer.style.display = 'none';

        appendBotMessage(`Switched active session to **${activeRole.toUpperCase()}**. Responses and document permissions are now tailored to this role.`);
      });
    });

    document.getElementById('psg-cancel-role-switch')?.addEventListener('click', () => {
      roleModalContainer.style.display = 'none';
    });
  }

  if (switchRoleBtn) {
    switchRoleBtn.addEventListener('click', () => {
      if (roleModalContainer && roleModalContainer.style.display === 'block') {
        roleModalContainer.style.display = 'none';
      } else {
        showRoleSelector();
      }
    });
  }

  // =========================================================================
  // 4. MESSAGE RENDERING & SESSION PERSISTENCE
  // =========================================================================
  function addInitialWelcomeMessage() {
    const welcomeText = `Hi! I'm the **PSGNexus AI**. 👋\n\nI can help you with admissions, placements, syllabus, CAT marks, hostel rules, and online form filling. What do you need?`;

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
    chatMessages.innerHTML = '';
    if (roleModalContainer) {
      chatMessages.appendChild(roleModalContainer);
    }
    messages.forEach(msg => renderSingleMessage(msg));
    scrollToBottom();
  }

  function renderSingleMessage(msg) {
    const msgRow = document.createElement('div');
    msgRow.className = `psg-message-row ${msg.sender} ${msg.status || ''}`;

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

    if (msg.sender === 'user') {
      msgRow.innerHTML = `
        <div style="max-width: 82%;">
          <div class="psg-bubble-user">
            ${formattedText}
          </div>
          <div class="psg-msg-time">${msg.time}</div>
        </div>
      `;
    } else {
      msgRow.innerHTML = `
        ${botAvatarSvg}
        <div style="max-width: 84%; flex: 1;">
          <div class="psg-bubble-bot">
            <div>${formattedText}</div>
            ${redirectHtml}
          </div>
          <div class="psg-msg-time">${msg.time}</div>
          ${chipsHtml}
        </div>
      `;
    }

    // Attach listeners for clickable chips
    const chipBtns = msgRow.querySelectorAll('.psg-chip');
    chipBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-chip');
        handleUserQuery(query);
      });
    });

    chatMessages.appendChild(msgRow);
  }

  function saveMessagesToStorage() {
    sessionStorage.setItem('psg_chat_messages', JSON.stringify(messages));
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
      });
    }, 40);
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
  // 5. TYPING INDICATOR
  // =========================================================================
  function setTyping(isTyping) {
    if (!typingIndicator) return;
    if (isTyping) {
      typingIndicator.classList.remove('hidden');
      scrollToBottom();
    } else {
      typingIndicator.classList.add('hidden');
    }
  }

  // =========================================================================
  // 6. QUERY HANDLING & BACKEND MONGODB SYNC
  // =========================================================================
  async function handleUserQuery(query) {
    if (!query || query.trim() === '') return;

    appendUserMessage(query);
    setTyping(true);

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
      setTyping(false);

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
      setTyping(false);
      appendBotMessage(
        '⚠️ Could not connect to the campus server. Please verify your Node.js server is running.',
        'error'
      );
    }
  }

  // Form Submit Listener
  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = chatInput.value.trim();
      if (query) {
        chatInput.value = '';
        handleUserQuery(query);
      }
    });
  }

  // Clear Chat History Button
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
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
