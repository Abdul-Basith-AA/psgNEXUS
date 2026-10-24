require('dotenv').config();
const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Load Knowledge Base & Permissions
const knowledgeBase = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'knowledgeBase.json'), 'utf-8'));
const permissions = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'permissions.json'), 'utf-8'));

// Optional Gemini Client Setup
let geminiAI = null;
if (process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY.trim() !== '') {
  try {
    const { GoogleGenAI } = require('@google/genai');
    geminiAI = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY.trim() });
    console.log('✓ Gemini AI initialized successfully.');
  } catch (err) {
    console.log('ℹ Gemini SDK not configured or key invalid. Local fallback active.');
  }
} else {
  console.log('ℹ No GEMINI_API_KEY found in .env. Running on built-in PSG Campus AI Engine (100% offline-ready).');
}

// ========================
// PAGE ROUTES (PSG TECH DUMMY PORTAL)
// ========================
app.get('/', (req, res) => {
  res.render('home', { title: 'PSG College of Technology | Official Portal', currentPage: '/' });
});

app.get('/about', (req, res) => {
  res.render('about', { title: 'About Us | PSG Tech', currentPage: '/about' });
});

app.get('/academics', (req, res) => {
  res.render('academics', { title: 'Academics & Syllabus | PSG Tech', currentPage: '/academics' });
});

app.get('/admissions', (req, res) => {
  res.render('admissions', { title: 'Admissions & Fee Structure | PSG Tech', currentPage: '/admissions' });
});

app.get('/forms', (req, res) => {
  res.render('forms', { title: 'Online Form Filling & Student Services | PSG Tech', currentPage: '/forms' });
});

app.get('/facilities', (req, res) => {
  res.render('facilities', { title: 'Campus Facilities & Hostels | PSG Tech', currentPage: '/facilities' });
});

app.get('/contact', (req, res) => {
  res.render('contact', { title: 'Contact & Helpdesk | PSG Tech', currentPage: '/contact' });
});

// ========================
// CHATBOT API ENGINE
// ========================
app.post('/api/chat', async (req, res) => {
  try {
    const { message, role, userDetails, currentPage } = req.body;

    if (!message || message.trim() === '') {
      return res.status(400).json({ reply: 'Please enter a valid query.' });
    }

    const cleanMsg = message.trim().toLowerCase();
    const activeRole = (role || 'visitor').toLowerCase();

    // ------------------------------------------------------------------
    // GUARDRAIL 1: Strictly Bound Within College Limits (Out-of-Scope)
    // ------------------------------------------------------------------
    const isOutOfScope = checkOutOfScope(cleanMsg);
    if (isOutOfScope) {
      return res.json({
        status: 'out_of_scope',
        reply: 'I am PSG Nexus, an AI assistant dedicated exclusively to PSG College of Technology queries (academics, admissions, facilities, and campus administration). Please ask questions related to PSG Tech.'
      });
    }

    // ------------------------------------------------------------------
    // GUARDRAIL 2: Role-Based Access Control (RBAC) & Document Security
    // ------------------------------------------------------------------
    const restriction = checkDocumentRestriction(cleanMsg, activeRole);
    if (restriction.restricted) {
      return res.json({
        status: 'restricted',
        reply: restriction.message,
        role: activeRole
      });
    }

    // ------------------------------------------------------------------
    // ACTION 3: Automatic Page Redirection Detection
    // ------------------------------------------------------------------
    const redirectAction = checkNavigationRedirect(cleanMsg, currentPage);
    if (redirectAction) {
      return res.json({
        status: 'redirect',
        reply: redirectAction.reply,
        redirectUrl: redirectAction.url,
        redirectName: redirectAction.name,
        redirectDelay: 1800,
        role: activeRole
      });
    }

    // ------------------------------------------------------------------
    // ACTION 4: Role-Specific Answers from Campus Knowledge Base
    // ------------------------------------------------------------------
    const localMatch = findLocalFAQ(cleanMsg, activeRole);
    if (localMatch) {
      return res.json({
        status: 'success',
        reply: localMatch.answer,
        redirectUrl: localMatch.redirect || null,
        redirectDelay: localMatch.redirect ? 2000 : null,
        role: activeRole
      });
    }

    // ------------------------------------------------------------------
    // ACTION 5: Generative AI (Gemini) if API Key is configured
    // ------------------------------------------------------------------
    if (geminiAI) {
      try {
        const aiResponse = await generateGeminiReply(message, activeRole, userDetails, currentPage);
        return res.json({
          status: 'success',
          reply: aiResponse,
          role: activeRole
        });
      } catch (aiErr) {
        console.error('Gemini API call failed, falling back to local reasoning:', aiErr.message);
      }
    }

    // ------------------------------------------------------------------
    // ACTION 6: Intelligent Default Campus Guidance
    // ------------------------------------------------------------------
    const smartFallback = generateCampusFallback(cleanMsg, activeRole);
    return res.json({
      status: 'success',
      reply: smartFallback.reply,
      suggestedQuestions: smartFallback.suggestions,
      role: activeRole
    });

  } catch (error) {
    console.error('Error in /api/chat:', error);
    res.status(500).json({ reply: 'An error occurred while processing your query. Please try again.' });
  }
});

// Helper: Check Out-of-Scope Queries
function checkOutOfScope(msg) {
  const offTopicKeywords = [
    'movie', 'cinema', 'bollywood', 'hollywood', 'song', 'joke', 'dating',
    'cricket score', 'ipl score', 'football score', 'recipe', 'how to cook',
    'bitcoin', 'crypto', 'stock market', 'election', 'politics',
    'weather in delhi', 'weather in mumbai', 'weather in usa',
    'write a python calculator', 'write code for snake game'
  ];

  return offTopicKeywords.some(keyword => msg.includes(keyword));
}

// Helper: Check Document & Sensitive Information Restrictions
function checkDocumentRestriction(msg, role) {
  for (const item of knowledgeBase.restrictedKeywords) {
    const matched = item.keywords.some(k => msg.includes(k));
    if (matched) {
      if (item.restrictedFor.includes(role)) {
        return {
          restricted: true,
          message: item.message
        };
      }
    }
  }
  return { restricted: false };
}

// Helper: Check Navigation & Redirection
function checkNavigationRedirect(msg, currentPage) {
  const navigationTriggers = [
    {
      keywords: ['form filling', 'fill form', 'bonafide form', 'leave form', 'apply bonafide', 'certificate form', 'take me to form', 'go to form', 'open form'],
      url: '/forms',
      name: 'Online Form Filling Portal',
      reply: 'Sure! Redirecting you directly to the PSG Tech Form Filling Portal for Bonafide certificates, leave slips, and requisitions.'
    },
    {
      keywords: ['admission', 'fees page', 'fee structure', 'cutoff', 'apply for admission', 'take me to admission', 'go to admission'],
      url: '/admissions',
      name: 'Admissions & Fees Portal',
      reply: 'Taking you to the Admissions & Fee Structure page for comprehensive eligibility and tuition fee details.'
    },
    {
      keywords: ['syllabus', 'curriculum', 'academics page', 'take me to syllabus', 'show syllabus', 'go to academics'],
      url: '/academics',
      name: 'Academics & Syllabus Repository',
      reply: 'Redirecting you to the Academics & Syllabus repository to download course regulations and semester curricula.'
    },
    {
      keywords: ['hostel', 'library', 'sports facility', 'facilities page', 'take me to facility', 'hostel facilities'],
      url: '/facilities',
      name: 'Campus Facilities',
      reply: 'Redirecting you to the Campus Facilities overview covering hostels, G.R.D. Memorial Library, and sports infrastructure.'
    },
    {
      keywords: ['about page', 'about psg', 'history of psg', 'principal profile', 'nirf ranking'],
      url: '/about',
      name: 'About PSG Tech',
      reply: 'Navigating to the About PSG Tech section highlighting heritage, accreditations, and institutional excellence.'
    },
    {
      keywords: ['contact page', 'reach us', 'emergency contact', 'office phone', 'contact number'],
      url: '/contact',
      name: 'Contact & Helpdesk',
      reply: 'Opening the Contact Directory with office intercom extensions and campus email helplines.'
    },
    {
      keywords: ['home page', 'go home', 'main portal'],
      url: '/',
      name: 'Home Portal',
      reply: 'Returning to the PSG College of Technology homepage.'
    }
  ];

  for (const nav of navigationTriggers) {
    if (nav.keywords.some(k => msg.includes(k))) {
      // Avoid redundant redirect if already on that exact page
      if (currentPage === nav.url) {
        return null;
      }
      return nav;
    }
  }
  return null;
}

// Helper: Find Role-Specific FAQs
function findLocalFAQ(msg, role) {
  const roleFaqs = knowledgeBase.faqByRole[role] || [];
  for (const faq of roleFaqs) {
    if (faq.keywords.some(k => msg.includes(k))) {
      return faq;
    }
  }
  return null;
}

// Helper: Fallback when not an exact match
function generateCampusFallback(msg, role) {
  let roleGreeting = '';
  let suggestions = [];

  switch (role) {
    case 'student':
      roleGreeting = 'As a registered PSG Tech student, I can assist you with:';
      suggestions = [
        'Take me to form filling page',
        'Download B.E./B.Tech Syllabus',
        'What are the hostel in-times?',
        'Minimum attendance required for End-Sem exams'
      ];
      break;
    case 'faculty':
      roleGreeting = 'Welcome, Faculty member. Here are common services I can assist with:';
      suggestions = [
        'Open staff leave application form',
        'Access Department Meeting Minutes',
        'Syllabus Revision Guidelines'
      ];
      break;
    case 'parent':
      roleGreeting = 'Welcome to PSG Tech Parent Assistance. Quick topics available:';
      suggestions = [
        'How can I pay tuition and hostel fees?',
        'Hostel Chief Warden contact details',
        'Go to Admissions & Eligibility page'
      ];
      break;
    default:
      roleGreeting = 'Welcome to PSG College of Technology! Common visitor queries:';
      suggestions = [
        'Take me to admissions page',
        'What is the TNEA cutoff for PSG Tech?',
        'Explore Campus Facilities & Hostels'
      ];
      break;
  }

  return {
    reply: `${roleGreeting}\n• You can ask about course syllabi, fee structures, admissions, and campus facilities.\n• You can also ask me to automatically redirect you anywhere (e.g., "take me to form filling page").`,
    suggestions: suggestions
  };
}

// Helper: Gemini AI Generator
async function generateGeminiReply(message, role, userDetails, currentPage) {
  const systemInstruction = `
    You are PSG Nexus, the official AI Digital Assistant for PSG College of Technology, Coimbatore.
    User Role: ${role}
    User Details: ${JSON.stringify(userDetails || {})}
    Current Webpage: ${currentPage}
    Rules:
    1. Answer professionally, concisely, and accurately about PSG Tech.
    2. Do NOT answer any non-college queries (politics, entertainment, external coding). Politely decline.
    3. If the user asks for confidential faculty files (payroll, question moderation banks) and is a student or visitor, strictly deny access.
    4. Keep responses within 2 to 4 sentences unless detailed instructions are requested.
  `;

  const response = await geminiAI.models.generateContent({
    model: 'gemini-1.5-flash',
    contents: message,
    config: {
      systemInstruction: systemInstruction,
      temperature: 0.7,
      maxOutputTokens: 250
    }
  });

  return response.text;
}

// Start Server
app.listen(PORT, () => {
  console.log(`=================================================`);
  console.log(`🚀 PSG Nexus Server is running on http://localhost:${PORT}`);
  console.log(`🎓 Team: Karthikeyan, Laxman, Basith`);
  console.log(`📌 Web App Development Project - PSG College of Tech`);
  console.log(`=================================================`);
});
