# PSG Nexus — Role-Based Campus AI Assistant & Portal

An intelligent, role-governed digital campus assistant built for **PSG College of Technology** for the **Web App Development (WAD)** course.

---

## 👥 Team Members & Work Allocation

| Member | Role / Assigned Module | Key Deliverables for Review 1 |
| :--- | :--- | :--- |
| **Karthikeyan** | **Campus Portal & Webpage Architect** | • Dummy PSG Tech Portal (`views/home.ejs`, `views/about.ejs`, `views/academics.ejs`, `views/admissions.ejs`, `views/forms.ejs`, `views/facilities.ejs`, `views/contact.ejs`).<br>• EJS shared layout partials (`header.ejs`, `footer.ejs`).<br>• Responsive Bootstrap 5 UI styling with PSG Navy (`#002B5C`) & Gold (`#C5A059`) aesthetics. |
| **Laxman** | **Chatbot UI & Session Persistence Orchestrator** | • Floating chatbot widget launcher & modal interface (`views/partials/chatbot.ejs`, `public/css/chatbot.css`).<br>• Interactive role onboarding flow (Student / Faculty / Parent / Visitor).<br>• Cross-page state management via `sessionStorage` (`psg_chat_messages`, `psg_chat_isOpen`).<br>• Animated auto-redirect notification timer. |
| **Basith** | **Backend API, Role Guardrails & AI Routing** | • Node.js & Express server configuration (`server.js`).<br>• Strict Out-of-Scope boundary filter (rejects non-PSG queries politely).<br>• Role-Based Access Control (RBAC) & document restriction engine (`data/permissions.json`).<br>• Multi-tier fallback architecture (Instant routing + Gemini API readiness). |

---

## 🛠️ Mandatory Tech Stack (Syllabus Compliant)

- **Backend:** Node.js + Express.js
- **Templates:** EJS (Embedded JavaScript)
- **Frontend:** Bootstrap 5.3 + Vanilla JavaScript (ES6) + CSS3
- **State Management:** Browser `sessionStorage` (chat history & widget persistence)
- **AI Integration:** Google GenAI SDK (`@google/genai`) with offline campus knowledge base fallback
- **Database:** Local JSON for Review 1 $\rightarrow$ MongoDB (Mongoose) for Review 2

---

## 🚀 How to Run the Project

1. **Open terminal in the project folder:**
   ```bash
   cd e:\psgNEXUS
   ```

2. **Start the server:**
   ```bash
   npm start
   ```
   *(or use `npm run dev` for automatic reloading on edits)*

3. **Open in browser:**
   ```text
   http://localhost:3000
   ```

---

## 🎯 Review 1 Demonstration Steps (For Faculty Review)

When presenting to **Ms. Kalyani A** on October 27, run through these test cases:

### Test Case 1: Active Chatbot Session across Page Redirect
1. Open `http://localhost:3000/`.
2. Click the floating **PSG Nexus AI** button at the bottom-right.
3. Select your role as **Student** (Roll: `26MX101`, Dept: `MCA`).
4. Type: **`take me to form filling page`**
5. **Observation:**
   - The bot replies: *"Sure! Redirecting you directly to the PSG Tech Form Filling Portal..."*
   - An animated countdown banner shows: *"Navigating: Loading Online Form Filling Portal..."*
   - The browser automatically navigates from `/` to `/forms`.
   - **Crucial Feature:** On the new `/forms` page, the chatbot **remains open**, with your roll number and previous conversation **completely preserved**!

### Test Case 2: Out-of-Scope Campus Boundary Filter
1. In the chat, type: **`Who won yesterday's cricket match?`** or **`Write python code for a calculator`**
2. **Observation:**
   - The bot responds: *"I am PSG Nexus, an AI assistant dedicated exclusively to PSG College of Technology queries... Please ask questions related to PSG Tech."*

### Test Case 3: Role-Based Access Control & Document Security
1. While logged in as **Student**, type: **`Show me faculty meeting minutes`**
2. **Observation:**
   - The bot flags a warning: *"⚠️ Access Restricted: Academic Council and internal staff meeting proceedings are classified for Faculty and Management members only."*
3. Click **"Switch Role"** in the chat header $\rightarrow$ select **Faculty / Staff**.
4. Ask the same question again: **`Show me faculty meeting minutes`**
5. **Observation:**
   - Access is **Granted**, giving links to staff intranet archives!

---

## 🔑 Adding Free Gemini API Key (When Claimed)

1. Open `.env` in the root folder.
2. Paste your Google AI Studio key:
   ```env
   PORT=3000
   GEMINI_API_KEY=AIzaSy...YourKeyHere
   ```
3. Restart the server (`npm start`). The assistant will automatically use Gemini 1.5 Flash for conversational intelligence while retaining all hard navigation routes and security guardrails!
