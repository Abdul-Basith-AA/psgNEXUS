require('dotenv').config();
const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// =========================================================================
// MONGODB LOCAL STORAGE INTEGRATION (Viewable in MongoDB Compass)
// =========================================================================
const MONGO_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/psgnexus_db';

const conversationSchema = new mongoose.Schema({
  role: { type: String, default: 'student' },
  userMessage: { type: String, required: true },
  botReply: { type: String, required: true },
  status: { type: String, default: 'success' },
  redirectUrl: { type: String, default: null },
  currentPage: { type: String, default: '/' },
  timestamp: { type: Date, default: Date.now }
});

const Conversation = mongoose.model('Conversation', conversationSchema);

let isMongoConnected = false;
mongoose.connect(MONGO_URI)
  .then(() => {
    isMongoConnected = true;
    console.log('✓ Connected to Local MongoDB Compass at mongodb://127.0.0.1:27017/psgnexus_db');
  })
  .catch((err) => {
    console.warn('⚠️ Local MongoDB connection pending. Check if MongoDB service is started.', err.message);
  });

// Load Knowledge Base & Permissions
const knowledgeBase = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'knowledgeBase.json'), 'utf-8'));
const permissions = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'permissions.json'), 'utf-8'));

// Optional Gemini Client Setup
let geminiAI = null;
if (process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY.trim() !== '') {
  try {
    const { GoogleGenAI } = require('@google/genai');
    geminiAI = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY.trim() });
    console.log('✓ Google Gemini AI initialized successfully.');
  } catch (err) {
    console.log('ℹ Gemini SDK key check failed. Running on local campus engine.');
  }
} else {
  console.log('ℹ No GEMINI_API_KEY configured yet. Running on built-in PSG Campus AI Engine.');
}

// =========================================================================
// PAGE ROUTES (MATCHING OFFICIAL PSGTECH.EDU PORTAL)
// =========================================================================
app.get('/', (req, res) => {
  res.render('home', { title: 'PSG College of Technology', currentPage: '/' });
});

app.get('/about', (req, res) => {
  res.render('about', { title: 'About Us | PSG College of Technology', currentPage: '/about' });
});

app.get('/academics', (req, res) => {
  res.render('academics', { title: 'Academics & Syllabus | PSG College of Technology', currentPage: '/academics' });
});

app.get('/admissions', (req, res) => {
  res.render('admissions', { title: 'Admissions 2026 | PSG College of Technology', currentPage: '/admissions' });
});

app.get('/forms', (req, res) => {
  res.render('forms', { title: 'Online Form Filling Portal | PSG College of Technology', currentPage: '/forms' });
});

app.get('/facilities', (req, res) => {
  res.render('facilities', { title: 'Campus Facilities & Hostels | PSG College of Technology', currentPage: '/facilities' });
});

app.get('/contact', (req, res) => {
  res.render('contact', { title: 'Contact | PSG College of Technology', currentPage: '/contact' });
});

// View saved MongoDB conversations directly in browser
app.get('/api/conversations', async (req, res) => {
  try {
    if (!isMongoConnected) {
      return res.json({ message: 'MongoDB is connecting or offline.', data: [] });
    }
    const logs = await Conversation.find().sort({ timestamp: -1 }).limit(50);
    res.json({ total: logs.length, database: 'psgnexus_db', collection: 'conversations', logs });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// =========================================================================
// CHATBOT API ENGINE & MONGODB STORAGE
// =========================================================================
app.post('/api/chat', async (req, res) => {
  try {
    const { message, role, userDetails, currentPage } = req.body;

    if (!message || message.trim() === '') {
      return res.status(400).json({ reply: 'Please enter a valid query.' });
    }

    const cleanMsg = message.trim().toLowerCase();
    const activeRole = (role || 'student').toLowerCase();

    let responsePayload = null;

    // ------------------------------------------------------------------
    // GUARDRAIL 1: Strictly Bound Within College Limits (Out-of-Scope)
    // ------------------------------------------------------------------
    const isOutOfScope = checkOutOfScope(cleanMsg);
    if (isOutOfScope) {
      responsePayload = {
        status: 'out_of_scope',
        reply: 'I am PSG Nexus, an AI assistant dedicated exclusively to PSG College of Technology queries (academics, admissions, facilities, and campus administration). Please ask questions related to PSG Tech.',
        redirectUrl: null
      };
    }

    // ------------------------------------------------------------------
    // GUARDRAIL 2: Role-Based Access Control (RBAC) & Document Security
    // ------------------------------------------------------------------
    if (!responsePayload) {
      const restriction = checkDocumentRestriction(cleanMsg, activeRole);
      if (restriction.restricted) {
        responsePayload = {
          status: 'restricted',
          reply: restriction.message,
          redirectUrl: null,
          role: activeRole
        };
      }
    }

    // ------------------------------------------------------------------
    // ACTION 3: Automatic Page Redirection Detection
    // ------------------------------------------------------------------
    if (!responsePayload) {
      const redirectAction = checkNavigationRedirect(cleanMsg, currentPage);
      if (redirectAction) {
        responsePayload = {
          status: 'redirect',
          reply: redirectAction.reply,
          redirectUrl: redirectAction.url,
          redirectName: redirectAction.name,
          redirectDelay: 1800,
          role: activeRole
        };
      }
    }

    // ------------------------------------------------------------------
    // ACTION 4: Role-Specific Answers from Campus Knowledge Base
    // ------------------------------------------------------------------
    if (!responsePayload) {
      const localMatch = findLocalFAQ(cleanMsg, activeRole);
      if (localMatch) {
        responsePayload = {
          status: 'success',
          reply: localMatch.answer,
          redirectUrl: localMatch.redirect || null,
          redirectDelay: localMatch.redirect ? 2000 : null,
          role: activeRole
        };
      }
    }

    // ------------------------------------------------------------------
    // ACTION 5: Generative AI (Gemini) if API Key is configured
    // ------------------------------------------------------------------
    if (!responsePayload && geminiAI) {
      try {
        const aiResponse = await generateGeminiReply(message, activeRole, userDetails, currentPage);
        responsePayload = {
          status: 'success',
          reply: aiResponse,
          redirectUrl: null,
          role: activeRole
        };
      } catch (aiErr) {
        console.error('Gemini API call failed, falling back to local reasoning:', aiErr.message);
      }
    }

    // ------------------------------------------------------------------
    // ACTION 6: Intelligent Default Campus Guidance
    // ------------------------------------------------------------------
    if (!responsePayload) {
      const smartFallback = generateCampusFallback(cleanMsg, activeRole);
      responsePayload = {
        status: 'success',
        reply: smartFallback.reply,
        suggestedQuestions: smartFallback.suggestions,
        redirectUrl: null,
        role: activeRole
      };
    }

    // ------------------------------------------------------------------
    // PERSIST TO MONGODB COMPASS (Local Storage)
    // ------------------------------------------------------------------
    if (isMongoConnected) {
      Conversation.create({
        role: activeRole,
        userMessage: message.trim(),
        botReply: responsePayload.reply,
        status: responsePayload.status,
        redirectUrl: responsePayload.redirectUrl || null,
        currentPage: currentPage || '/'
      }).catch(err => console.error('Failed to save to MongoDB:', err.message));
    }

    return res.json(responsePayload);

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
      roleGreeting = 'Hello, PSG Tech Student! Here is what I can assist you with right now:';
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
    reply: `${roleGreeting}\n• You can ask about course syllabi, CAT marks, attendance criteria, and hostel rules.\n• You can also ask me to automatically redirect you anywhere (e.g., "take me to form filling page").`,
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
  console.log(`🗄️ Local MongoDB: mongodb://127.0.0.1:27017/psgnexus_db`);
  console.log(`=================================================`);
});
