# PSG Nexus — Role-Based Campus AI Assistant & Official Portal

An intelligent, role-governed digital campus assistant built for **PSG College of Technology** as part of the **Web App Development (WAD)** curriculum.

---

## 👥 Team Members & Work Allocation

| Member | Role / Assigned Module | Deliverables Completed for Review 1 |
| :--- | :--- | :--- |
| **Karthikeyan** | **Official Portal & UI Architect** | • **>90% Replica of `https://www.psgtech.edu/`** (`views/home.ejs`, `views/partials/header.ejs`, `views/partials/footer.ejs`, `public/css/style.css`).<br>• Authentic top utility bar, news ticker marquee, official Platinum Jubilee (75 yrs) & PSG Charities (100 yrs) crests, royal blue navbar (`#2B4BAB`), and hero image carousel.<br>• Online Form Filling Portal (`views/forms.ejs`). |
| **Laxman** | **Chatbot UI & Session Persistence Orchestrator** | • **Bottom-Left Floating Assistant** (`#psg-chatbot-launcher`, `views/partials/chatbot.ejs`, `public/css/chatbot.css`).<br>• **Student Default Active Role**: Immediately ready for queries without blocking modals, while displaying and supporting quick role switching to Faculty, Parent, and Visitor.<br>• **Cross-Page Persistence**: Uses `sessionStorage` to keep the chat active and history preserved across page redirects. |
| **Basith** | **Backend API, Local MongoDB Compass & Guardrails** | • Express API server (`server.js`) with `/api/chat` and `/api/conversations`.<br>• **Local MongoDB Compass Storage**: Every chat query and response is saved to `mongodb://127.0.0.1:27017/psgnexus_db` under the `conversations` collection.<br>• Campus boundary filter (rejects off-topic queries) & role-based document access control (RBAC). |

---

## 🗄️ How to View Chat Logs in MongoDB Compass

1. Open **MongoDB Compass** on your local machine.
2. Click **Connect** to the default local URI:
   ```text
   mongodb://localhost:27017
   ```
   *(or `mongodb://127.0.0.1:27017`)*
3. In the left database list, open **`psgnexus_db`**.
4. Click the **`conversations`** collection.
5. You will see every question asked, the assistant's response, role (`student`), status, and timestamp!
6. You can also inspect the logs directly in the browser at:
   ```text
   http://localhost:3000/api/conversations
   ```

---

## 🔑 Where to Get Your Free Gemini API Key (Using Your 18-Month Gemini Pro Subscription)

Since you are subscribed to the **18-Month Gemini Pro** plan (Google One AI Premium / Google Workspace):

1. Open your browser and go to **[https://aistudio.google.com/](https://aistudio.google.com/)**.
2. **Crucial:** Sign in using the **exact Google account** that has your 18-month Gemini Pro subscription.
3. Click the blue **"Get API key"** button on the left menu (or top right).
4. Click **"Create API key"** $\rightarrow$ select **"Create API key in new project"**.
5. Copy the generated key (starts with `AIzaSy...`).
6. In your `e:\psgNEXUS` project, open the `.env` file and paste it:
   ```env
   PORT=3000
   GEMINI_API_KEY=AIzaSyYourGeneratedKeyHere
   ```
7. That's it! Your subscription includes generous free quotas (15 requests/min and 1,500 requests/day for `gemini-1.5-flash` and `gemini-1.5-pro` at zero cost).
8. The server will automatically detect the key and activate generative intelligence!

---

## 🚀 How to Run the Project

1. Open your terminal in `e:\psgNEXUS`:
   ```bash
   cd e:\psgNEXUS
   ```

2. Start the server:
   ```bash
   npm start
   ```

3. Open your browser:
   ```text
   http://localhost:3000
   ```

---

## 🎯 Evaluator Test Cases for Review 1

1. **Official Page Match (>90%):** Notice the top marquee news ticker, official logos, PSG signature royal blue menu bar, and carousel banners matching `https://www.psgtech.edu/`.
2. **Bottom-Left Assistant:** Click the **PSG Nexus AI** icon located at the bottom-left corner.
3. **Student Active Role:** Notice the assistant greets you immediately as a **Student** with relevant academic suggestions.
4. **Auto-Redirect with Active Session:** Ask **`take me to form filling page`**. Notice the assistant counts down, navigates to `/forms`, and stays open with the full chat intact!
5. **MongoDB Storage:** Open MongoDB Compass or visit `http://localhost:3000/api/conversations` to demonstrate real-time database persistence!
