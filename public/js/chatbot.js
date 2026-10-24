/**
 * PSG NEXUS - Client-Side Intelligent Chatbot & Cross-Page Persistence Engine
 * Authors: Karthikeyan, Laxman, Basith
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
  const onboardingContainer = document.getElementById('psg-onboarding-container');

  // State in Memory
  let activeRole = sessionStorage.getItem('psg_chat_role') || null;
  let userDetails = JSON.parse(sessionStorage.getItem('psg_chat_details') || '{}');
  let messages = JSON.parse(sessionStorage.getItem('psg_chat_messages') || '[]');
  let isOpen = sessionStorage.getItem('psg_chat_isOpen') === 'true';

  // =========================================================================
  // INITIALIZATION ON PAGE LOAD
  // =========================================================================
  function initChatbot() {
    updateRoleUI();

    if (activeRole) {
      if (onboardingContainer) onboardingContainer.style.display = 'none';
      if (messages.length === 0) {
        addInitialWelcomeMessage();
      } else {
        renderAllMessages();
      }
    } else {
      showOnboardingCard();
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
    if (activeRole) {
      setTimeout(() => chatInput.focus(), 200);
    }
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
  // ROLE ONBOARDING MANAGEMENT
  // =========================================================================
  function updateRoleUI() {
    if (activeRole) {
      roleBadge.textContent = activeRole.toUpperCase();
      roleBadge.className = `psg-role-tag role-${activeRole}`;
    } else {
      roleBadge.textContent = 'GUEST';
    }
  }

  function showOnboardingCard() {
    if (!onboardingContainer) return;
    onboardingContainer.style.display = 'block';
    onboardingContainer.innerHTML = `
      <div class="psg-onboarding-card">
        <div class="psg-onboarding-title">Welcome to PSG Nexus</div>
        <div class="psg-onboarding-sub">Select your institutional role to personalize answers & access privileges:</div>
        
        <div class="psg-role-selector-grid">
          <button type="button" class="psg-role-btn active" data-role="student">👨‍🎓 Student</button>
          <button type="button" class="psg-role-btn" data-role="faculty">👨‍🏫 Faculty / Staff</button>
          <button type="button" class="psg-role-btn" data-role="parent">👨‍👩‍👧 Parent</button>
          <button type="button" class="psg-role-btn" data-role="visitor">🌐 Visitor / Alumni</button>
        </div>

        <div id="psg-role-fields">
          <div class="psg-details-group">
            <label>Roll Number (e.g., 26MX101):</label>
            <input type="text" id="input-roll-no" placeholder="Enter roll number" value="${userDetails.rollNo || ''}">
          </div>
          <div class="psg-details-group">
            <label>Department:</label>
            <select id="input-dept">
              <option value="Computer Applications (MCA)">Computer Applications (MCA)</option>
              <option value="Computer Science & Engg (CSE)">Computer Science & Engg (CSE)</option>
              <option value="Information Technology (IT)">Information Technology (IT)</option>
              <option value="Mechanical Engg">Mechanical Engg</option>
              <option value="Electrical & Electronics (EEE)">Electrical & Electronics (EEE)</option>
            </select>
          </div>
        </div>

        <button type="button" class="psg-start-btn" id="psg-confirm-role-btn">Access PSG Nexus</button>
      </div>
    `;

    // Role button listeners
    const roleBtns = onboardingContainer.querySelectorAll('.psg-role-btn');
    let selectedRole = 'student';

    roleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        roleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedRole = btn.getAttribute('data-role');
        renderRoleFields(selectedRole);
      });
    });

    const confirmBtn = document.getElementById('psg-confirm-role-btn');
    confirmBtn.addEventListener('click', () => {
      activeRole = selectedRole;
      sessionStorage.setItem('psg_chat_role', activeRole);

      if (activeRole === 'student') {
        const roll = document.getElementById('input-roll-no')?.value || '26MX101';
        const dept = document.getElementById('input-dept')?.value || 'MCA';
        userDetails = { rollNo: roll, dept: dept };
      } else if (activeRole === 'faculty') {
        const staffId = document.getElementById('input-staff-id')?.value || 'PSG-FAC-404';
        userDetails = { staffId: staffId, dept: 'Computing' };
      } else {
        const name = document.getElementById('input-name')?.value || 'Campus Guest';
        userDetails = { name: name };
      }

      sessionStorage.setItem('psg_chat_details', JSON.stringify(userDetails));
      updateRoleUI();
      onboardingContainer.style.display = 'none';

      if (messages.length === 0) {
        addInitialWelcomeMessage();
      } else {
        renderAllMessages();
      }
    });
  }

  function renderRoleFields(role) {
    const fieldsContainer = document.getElementById('psg-role-fields');
    if (!fieldsContainer) return;

    if (role === 'student') {
      fieldsContainer.innerHTML = `
        <div class="psg-details-group">
          <label>Roll Number (e.g., 26MX101):</label>
          <input type="text" id="input-roll-no" placeholder="Enter roll number" value="26MX101">
        </div>
        <div class="psg-details-group">
          <label>Department:</label>
          <select id="input-dept">
            <option value="Computer Applications (MCA)">Computer Applications (MCA)</option>
            <option value="Computer Science & Engg (CSE)">Computer Science & Engg (CSE)</option>
            <option value="Information Technology (IT)">Information Technology (IT)</option>
            <option value="Mechanical Engg">Mechanical Engg</option>
          </select>
        </div>
      `;
    } else if (role === 'faculty') {
      fieldsContainer.innerHTML = `
        <div class="psg-details-group">
          <label>Staff ID (e.g., PSG-FAC-102):</label>
          <input type="text" id="input-staff-id" placeholder="Enter staff identifier" value="PSG-FAC-102">
        </div>
      `;
    } else {
      fieldsContainer.innerHTML = `
        <div class="psg-details-group">
          <label>Your Name:</label>
          <input type="text" id="input-name" placeholder="Enter your full name" value="Guest">
        </div>
      `;
    }
  }

  if (switchRoleBtn) {
    switchRoleBtn.addEventListener('click', () => {
      showOnboardingCard();
    });
  }

  // =========================================================================
  // MESSAGE RENDERING & SESSION PERSISTENCE
  // =========================================================================
  function addInitialWelcomeMessage() {
    let welcomeText = `Hello! I am PSG Nexus, your official AI campus assistant for PSG College of Technology.`;
    
    if (activeRole === 'student') {
      welcomeText += `\n\nWelcome back, **${userDetails.rollNo || 'Student'}** (${userDetails.dept || 'Engineering'}). You have authenticated access to syllabi, academic calendars, and online form applications.`;
    } else if (activeRole === 'faculty') {
      welcomeText += `\n\nGreetings, Faculty Member (**${userDetails.staffId || 'Staff'}**). You have authorized access to internal circulars, syllabus revision memos, and staff leave portals.`;
    } else if (activeRole === 'parent') {
      welcomeText += `\n\nWelcome to the PSG Tech Parent Portal. How can I assist you with fee schedules, hostel amenities, or academic schedules today?`;
    } else {
      welcomeText += `\n\nWelcome to PSG Tech! Feel free to ask about admissions, TNEA cutoffs, departments, or campus facilities.`;
    }

    const defaultChips = [
      'Take me to form filling page',
      'Show B.E. Syllabus',
      'Admissions & Fees',
      'Hostel timings'
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
    if (onboardingContainer && onboardingContainer.style.display !== 'none') {
      chatBody.appendChild(onboardingContainer);
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
            <strong>Navigating:</strong> Loading ${escapeHtml(msg.redirectName || msg.redirectUrl)}...
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

    // Attach chip click listeners
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
  // SEND QUERY TO BACKEND
  // =========================================================================
  async function handleUserQuery(query) {
    if (!query || query.trim() === '') return;

    if (!activeRole) {
      openChat();
      showOnboardingCard();
      return;
    }

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

      // AUTOMATIC REDIRECTION WITH ACTIVE SESSION
      if (data.redirectUrl && data.redirectUrl !== window.location.pathname) {
        // Ensure state is locked in sessionStorage before page transition
        sessionStorage.setItem('psg_chat_isOpen', 'true');
        saveMessagesToStorage();

        setTimeout(() => {
          window.location.href = data.redirectUrl;
        }, data.redirectDelay || 1800);
      }

    } catch (error) {
      hideTypingIndicator();
      appendBotMessage(
        '⚠️ Could not connect to the campus server. Please check if your Node server is running.',
        'error'
      );
    }
  }

  // Handle Chat Form Submit
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
      if (confirm('Clear chat history for this session?')) {
        messages = [];
        sessionStorage.removeItem('psg_chat_messages');
        renderAllMessages();
        addInitialWelcomeMessage();
      }
    });
  }

  // Run initialization
  initChatbot();
});
