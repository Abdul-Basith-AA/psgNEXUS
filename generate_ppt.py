import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    C_NAVY = RGBColor(27, 41, 75)       # #1B294B
    C_BLUE = RGBColor(43, 75, 171)      # #2B4BAB
    C_GOLD = RGBColor(197, 160, 89)     # #C5A059
    C_DARK = RGBColor(33, 37, 41)       # #212529
    C_GRAY = RGBColor(108, 117, 125)    # #6C757D
    C_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="PSG COLLEGE OF TECHNOLOGY • DEPARTMENT OF COMPUTER APPLICATIONS"):
        # Header banner shape
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = C_NAVY
        header_shape.line.color.rgb = C_GOLD
        header_shape.line.width = Pt(2.5)

        # Category text
        txBox1 = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf1 = txBox1.text_frame
        p1 = tf1.paragraphs[0]
        p1.text = category.upper()
        p1.font.name = 'Arial'
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_GOLD

        # Title text
        txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.6))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.name = 'Arial'
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE

        # Footer line
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.05), Inches(13.333), Inches(0.45))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = C_NAVY
        footer_line.line.color.rgb = C_NAVY

        tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.7), Inches(0.35))
        tf_foot = tx_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "26MX17 WEB APPLICATION DEVELOPMENT • REVIEW 1 • TEAM 1 (PSG NEXUS)"
        p_foot.font.name = 'Arial'
        p_foot.font.size = Pt(10)
        p_foot.font.color.rgb = C_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.color.rgb = C_NAVY

    # Title Card Inner
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = C_GOLD
    card1.line.width = Pt(3)

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.1), Inches(10.7), Inches(1.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "PSG COLLEGE OF TECHNOLOGY, COIMBATORE - 641 004"
    p.font.name = 'Arial'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    p_sub = tf.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "DEPARTMENT OF COMPUTER APPLICATIONS • 26MX17 WEB APPLICATION DEVELOPMENT"
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(11)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_GRAY

    p_proj = tf.add_paragraph()
    p_proj.alignment = PP_ALIGN.CENTER
    p_proj.text = "\nPSG NEXUS (CHAT-BOT)"
    p_proj.font.name = 'Arial'
    p_proj.font.size = Pt(32)
    p_proj.font.bold = True
    p_proj.font.color.rgb = C_NAVY

    p_tag = tf.add_paragraph()
    p_tag.alignment = PP_ALIGN.CENTER
    p_tag.text = "Intelligent Role-Based Campus Digital Assistant & Navigation Portal"
    p_tag.font.name = 'Arial'
    p_tag.font.size = Pt(14)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_GOLD

    # Columns for Guide and Team
    tb_guide = s1.shapes.add_textbox(Inches(1.8), Inches(4.3), Inches(4.5), Inches(2.0))
    tf_g = tb_guide.text_frame
    p_g_hdr = tf_g.paragraphs[0]
    p_g_hdr.text = "PROJECT GUIDE:"
    p_g_hdr.font.name = 'Arial'
    p_g_hdr.font.size = Pt(13)
    p_g_hdr.font.bold = True
    p_g_hdr.font.color.rgb = C_BLUE

    p_g_name = tf_g.add_paragraph()
    p_g_name.text = "Ms. J. GOWRI THANGAM\nAssistant Professor\nDepartment of Computer Applications\nPSG College of Technology"
    p_g_name.font.name = 'Arial'
    p_g_name.font.size = Pt(11)
    p_g_name.font.color.rgb = C_DARK

    tb_team = s1.shapes.add_textbox(Inches(7.2), Inches(4.3), Inches(4.8), Inches(2.0))
    tf_t = tb_team.text_frame
    p_t_hdr = tf_t.paragraphs[0]
    p_t_hdr.text = "TEAM MEMBERS (TEAM 1):"
    p_t_hdr.font.name = 'Arial'
    p_t_hdr.font.size = Pt(13)
    p_t_hdr.font.bold = True
    p_t_hdr.font.color.rgb = C_BLUE

    p_t_names = tf_t.add_paragraph()
    p_t_names.text = "• LAXMAN B (26MX209)\n• KARTHIKEYAN S (26MX110)\n• MOHAMED ABDUL BASITH A A (26MX115)"
    p_t_names.font.name = 'Arial'
    p_t_names.font.size = Pt(11.5)
    p_t_names.font.bold = True
    p_t_names.font.color.rgb = C_NAVY

    # -------------------------------------------------------------
    # SLIDE 2: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Acknowledgement")

    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(5.0))
    tf = tb.text_frame

    items = [
        ("Dr. N. ILAYARAJA", "Head of the Department, Department of Computer Applications, for providing overall guidance, institutional facilities, and motivation."),
        ("Ms. A. KALYANI", "MCA Programme Coordinator & Course Coordinator (26MX17 WAD), for curriculum structure, continuous monitoring, and valuable review instructions."),
        ("Ms. J. GOWRI THANGAM", "Faculty Project Guide, for consistent technical feedback, review dairy verification, and architecture suggestions."),
        ("FACULTY REVIEW PANEL", "Review Panel Members and Department Faculty, for evaluating our Review 1 deliverables and providing constructive suggestions for project enhancement.")
    ]

    for title, desc in items:
        p_t = tf.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.name = 'Arial'
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = C_BLUE
        p_t.space_before = Pt(12)

        p_d = tf.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.name = 'Arial'
        p_d.font.size = Pt(12.5)
        p_d.font.color.rgb = C_DARK

    # -------------------------------------------------------------
    # SLIDE 3: PROJECT OVERVIEW (BULLETED FORMAT ONLY)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Project Overview")

    tb = s3.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2))
    tf = tb.text_frame

    bullets_s3 = [
        "Interactive Digital Campus Assistant: Seamlessly integrated as an interactive widget on the PSG College website.",
        "Unified Single-Point Guide: Delivers fast information across syllabi, departments, admissions, fees, hostel rules, and forms.",
        "Persistent In-Browser Session: Chatbot remains active and remembers conversation history across page navigation using browser sessionStorage.",
        "Intelligent Autonomous Page Redirection: Automatically navigates users to target pages (e.g., from Home to Online Forms Portal) without resetting the chat.",
        "Role-Based Access Control (RBAC): Provides tailored assistance for Students, Faculty, Parents, and Visitors while protecting confidential staff records.",
        "Local Database Persistence: Automatically stores user queries, responses, and roles in local MongoDB Compass (psgnexus_db.conversations) for campus analytics."
    ]

    for b in bullets_s3:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.name = 'Arial'
        p.font.size = Pt(14)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 4: ANALYSIS OF THE EXISTING SYSTEM
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Analysis of the Existing System")

    # Left Box: Existing Features
    card_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_LIGHT
    card_l.line.color.rgb = C_BLUE

    tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    p_lh = tf_l.paragraphs[0]
    p_lh.text = "EXISTING SYSTEM FEATURES"
    p_lh.font.name = 'Arial'
    p_lh.font.size = Pt(15)
    p_lh.font.bold = True
    p_lh.font.color.rgb = C_BLUE

    feats = [
        "Central Information Hub: Publishes circulars, department news, tenders, and events (psgtech.edu).",
        "Transactional Student Services: Studzone portal allows viewing internal marks and fee payment challans.",
        "Traditional Menu Navigation: Organized into multi-level dropdown menus and external PDF links.",
        "Static FAQ & Contact Forms: General contact numbers and grievance emails."
    ]
    for f in feats:
        p = tf_l.add_paragraph()
        p.text = f"• {f}"
        p.font.name = 'Arial'
        p.font.size = Pt(12)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(10)

    # Right Box: Missing Features
    card_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = RGBColor(255, 245, 245)
    card_r.line.color.rgb = RGBColor(220, 53, 69)

    tb_r = s4.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_r = tb_r.text_frame
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "IDENTIFIED MISSING FEATURES"
    p_rh.font.name = 'Arial'
    p_rh.font.size = Pt(15)
    p_rh.font.bold = True
    p_rh.font.color.rgb = RGBColor(200, 35, 51)

    miss = [
        "No Conversational Assistance: Lacks an interactive virtual guide to immediately answer repetitive queries.",
        "High Information Retrieval Latency: Students must search across multiple sub-pages to locate rules (75% attendance, CAT marks).",
        "Zero Automated Navigation: Cannot redirect users directly to relevant online forms or syllabus repositories.",
        "Lack of Cross-Page Continuity: Conventional forms or widgets reset upon clicking another page link.",
        "Absence of Role-Based Security: Anyone sees static links, but no contextual filtering exists for visitors vs faculty."
    ]
    for m in miss:
        p = tf_r.add_paragraph()
        p.text = f"• {m}"
        p.font.name = 'Arial'
        p.font.size = Pt(12)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 5: LITERATURE SURVEY OF THE EXISTING SYSTEM
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Survey of the Existing System")

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    tf = tb.text_frame

    survey = [
        ("1. Official Institutional Portals (e.g., psgtech.edu)", 
         "Standard university websites provide comprehensive information but rely strictly on static hierarchical menus. Studies show students spend substantial time navigating sub-domains to locate routine circulars and syllabus copies."),
        ("2. Standalone Chatbot Systems in Higher Education", 
         "Existing higher education chatbots function mostly as isolated popups on single landing pages. When a user clicks an internal link, the chat context resets, causing communication drop-off and frustration."),
        ("3. Traditional Contact Forms & Static FAQs", 
         "Static FAQ pages fail to address user queries dynamically, and 'Contact Us' forms suffer from delayed response times (24-48 hours) for common procedural questions."),
        ("4. The Proposed PSG Nexus Approach", 
         "Combines a responsive college portal replica with a persistent, bottom-left AI assistant using client-side sessionStorage, automated page redirection, and role-governed document security.")
    ]

    for title, desc in survey:
        p_t = tf.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.name = 'Arial'
        p_t.font.size = Pt(13.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_BLUE
        p_t.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.name = 'Arial'
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = C_DARK

    # -------------------------------------------------------------
    # SLIDE 6: TOOLS AND TECHNOLOGIES TO BE USED
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Tools and Technologies to be Used")

    tech_categories = [
        ("FRONTEND & CLIENT UI", "HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3", "Responsive replica of psgtech.edu, carousels, cards, floating chatbot widget with animated pulse ring."),
        ("SERVER & TEMPLATING", "Node.js & Express.js, EJS (Embedded JavaScript)", "Asynchronous server script, modular MVC routing, reusable EJS partials (header.ejs, footer.ejs, chatbot.ejs)."),
        ("SESSION & PERSISTENCE", "Browser sessionStorage & Express Sessions", "Preserves chat history, user role, and active widget state across page reloads without database overhead."),
        ("DATABASE & STORAGE", "MongoDB (Local Storage) & MongoDB Compass", "Mongoose ODM models storing query text, bot responses, user roles, status, and timestamps in 'psgnexus_db'."),
        ("AI / NLP ENGINE", "Built-in Campus Knowledge Base & Google GenAI SDK", "50+ offline PSG Tech topics with keyword scoring; optional Gemini 1.5 Flash API for natural answering.")
    ]

    top_y = 1.5
    for cat, tools, desc in tech_categories:
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_y), Inches(11.7), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = C_LIGHT
        box.line.color.rgb = C_BLUE
        box.line.width = Pt(1.5)

        tb_box = s6.shapes.add_textbox(Inches(1.0), Inches(top_y + 0.05), Inches(11.3), Inches(0.85))
        tf_b = tb_box.text_frame
        p_b1 = tf_b.paragraphs[0]
        p_b1.text = f"{cat}:  {tools}"
        p_b1.font.name = 'Arial'
        p_b1.font.size = Pt(12)
        p_b1.font.bold = True
        p_b1.font.color.rgb = C_BLUE

        p_b2 = tf_b.add_paragraph()
        p_b2.text = f"• {desc}"
        p_b2.font.name = 'Arial'
        p_b2.font.size = Pt(10.5)
        p_b2.font.color.rgb = C_DARK

        top_y += 1.08

    # -------------------------------------------------------------
    # SLIDE 7: MAJOR ENTITIES INVOLVED IN THE PROPOSED PROJECT
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Major Entities Involved in the Proposed Project")

    entities = [
        ("STUDENT (26MX Roll No, Dept)", "Default active role in PSG Nexus. Accesses attendance criteria (75%), CAT continuous assessment marks, CGPA calculations, syllabus downloads, hostel rules, and online form submissions."),
        ("FACULTY / STAFF (Staff ID)", "Elevated administrative privileges. Accesses staff leave application forms, syllabus revision guidelines, and confidential academic council / department meeting records."),
        ("PARENT & PROSPECTIVE STUDENT", "Focuses on institutional credentials. Accesses tuition fee structures, TNEA cutoff marks, hostel warden phone numbers, and admission eligibility guidelines."),
        ("VISITOR & ALUMNI", "Explores public institutional facts. Accesses campus travel directions, G.R.D. Memorial Library details, NIRF rankings, and alumni network resources (Laudea)."),
        ("CAMPUS ADMINISTRATOR", "Monitors interaction analytics via MongoDB Compass. Tracks frequently searched student queries to identify information gaps and update circulars.")
    ]

    tb = s7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    tf = tb.text_frame

    for ent, desc in entities:
        p_e = tf.add_paragraph()
        p_e.text = f"• {ent}"
        p_e.font.name = 'Arial'
        p_e.font.size = Pt(13)
        p_e.font.bold = True
        p_e.font.color.rgb = C_BLUE
        p_e.space_before = Pt(8)

        p_ed = tf.add_paragraph()
        p_ed.text = f"   Role & Access: {desc}"
        p_ed.font.name = 'Arial'
        p_ed.font.size = Pt(11)
        p_ed.font.color.rgb = C_DARK

    # -------------------------------------------------------------
    # SLIDE 8: MAJOR FUNCTIONALITIES OF THE SYSTEM (30% FOR REVIEW 1)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Major Functionalities of the System (Review 1 Deliverables)")

    tb = s8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    tf = tb.text_frame

    funcs = [
        ("1. Official Website Replica (>90% Match)", "Replicated top utility bar with news marquee, official logos (75 & 100 yrs), royal blue navigation header (#2B4BAB), hero carousel, portal tiles, and 4-column footer."),
        ("2. Bottom-Left Assistant Widget", "Embedded floating AI launcher in the bottom-left corner with glowing cyber-cyan ring (#38BDF8) and active 'STUDENT' default role."),
        ("3. Multi-Page Redirection Engine", "Automatically redirects users to specific routes (e.g., /forms or /academics) upon verbal request with an animated 2-second countdown."),
        ("4. Cross-Page Session Continuity", "Utilizes browser sessionStorage to keep the chat window open and preserve all conversation history across page navigation."),
        ("5. Out-of-Scope Boundary Guardrail", "Scans incoming queries for non-college topics (movies, cricket, gaming) and responds with polite institutional boundary notices."),
        ("6. Role-Based Document Access Control (RBAC)", "Restricts confidential faculty meeting records and staff salary slips when queried by Students, but authorizes them for Faculty."),
        ("7. Local MongoDB Compass Storage", "Asynchronously records all conversations into local MongoDB (psgnexus_db.conversations) with browser endpoint verification.")
    ]

    for title, desc in funcs:
        p_f = tf.add_paragraph()
        p_f.text = f"• {title}:  {desc}"
        p_f.font.name = 'Arial'
        p_f.font.size = Pt(11.5)
        p_f.font.color.rgb = C_DARK
        p_f.space_before = Pt(7)

    # -------------------------------------------------------------
    # SLIDE 9: WORK FLOW OF THE PROJECT
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Work Flow of the Project")

    # Add Flow Diagram Image if exists
    if os.path.exists('docs_assets/flow_diagram.png'):
        s9.shapes.add_picture('docs_assets/flow_diagram.png', Inches(0.8), Inches(1.35), width=Inches(7.2))
        
        # Right text summary
        tb_wf = s9.shapes.add_textbox(Inches(8.3), Inches(1.4), Inches(4.3), Inches(5.2))
        tf_wf = tb_wf.text_frame
        p_wfh = tf_wf.paragraphs[0]
        p_wfh.text = "WORKFLOW STAGES:"
        p_wfh.font.name = 'Arial'
        p_wfh.font.size = Pt(14)
        p_wfh.font.bold = True
        p_wfh.font.color.rgb = C_BLUE

        wf_steps = [
            "1. User Access: Opens portal, launcher toggles chat.",
            "2. Role Identification: Default Student role verified.",
            "3. Boundary Filtering: Checks if query is college-related.",
            "4. Security Check: Evaluates document access permissions.",
            "5. Intent Matching: Checks if query requests page navigation.",
            "6. Query Answering: Fast lookup via local campus knowledge base or Gemini API.",
            "7. Dual Persistence: Writes document to MongoDB & saves state in sessionStorage.",
            "8. Smooth Transition: Navigates page with open chat session."
        ]
        for step in wf_steps:
            p = tf_wf.add_paragraph()
            p.text = f"• {step}"
            p.font.name = 'Arial'
            p.font.size = Pt(10)
            p.font.color.rgb = C_DARK
            p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 10: BPMN DIAGRAM OF THE PROJECT
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "BPMN Diagram of the Entire Project")

    if os.path.exists('docs_assets/bpmn_diagram.png'):
        s10.shapes.add_picture('docs_assets/bpmn_diagram.png', Inches(0.8), Inches(1.35), width=Inches(8.2))

        tb_bpmn = s10.shapes.add_textbox(Inches(9.2), Inches(1.4), Inches(3.4), Inches(5.2))
        tf_b = tb_bpmn.text_frame
        p_bh = tf_b.paragraphs[0]
        p_bh.text = "3 SWIMLANES:"
        p_bh.font.name = 'Arial'
        p_bh.font.size = Pt(13)
        p_bh.font.bold = True
        p_bh.font.color.rgb = C_BLUE

        b_steps = [
            "User Lane: Interacts with portal, submits queries, and clicks quick prompt chips.",
            "Client UI Lane: Serializes chat history into sessionStorage and executes redirection timers.",
            "Express Server Lane: Evaluates guardrails, processes intent, generates answer, and logs to MongoDB.",
            "End Event: User lands on destination page with active assistant conversation."
        ]
        for bs in b_steps:
            p = tf_b.add_paragraph()
            p.text = f"• {bs}"
            p.font.name = 'Arial'
            p.font.size = Pt(10)
            p.font.color.rgb = C_DARK
            p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 11: ALL UI PAGES OF THE COMPLETE PROJECT
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "UI Pages of the Complete Project (Running Prototype)")

    if os.path.exists('docs_assets/screenshot1_portal.png') and os.path.exists('docs_assets/screenshot2_assistant.png'):
        # Left screenshot: Portal
        s11.shapes.add_picture('docs_assets/screenshot1_portal.png', Inches(0.8), Inches(1.4), width=Inches(7.2))
        tb_cap1 = s11.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(7.2), Inches(0.8))
        tf_c1 = tb_cap1.text_frame
        p_c1 = tf_c1.paragraphs[0]
        p_c1.text = "• Figure A: Official PSG Tech Portal Replica with Bottom-Left Floating Launcher"
        p_c1.font.name = 'Arial'
        p_c1.font.size = Pt(10.5)
        p_c1.font.bold = True
        p_c1.font.color.rgb = C_BLUE

        # Right screenshot: Chatbot Window
        s11.shapes.add_picture('docs_assets/screenshot2_assistant.png', Inches(8.3), Inches(1.4), width=Inches(4.2))
        tb_cap2 = s11.shapes.add_textbox(Inches(8.3), Inches(6.1), Inches(4.2), Inches(0.8))
        tf_c2 = tb_cap2.text_frame
        p_c2 = tf_c2.paragraphs[0]
        p_c2.text = "• Figure B: Interactive Chatbot (Student Role, Quick Chips & Redirection)"
        p_c2.font.name = 'Arial'
        p_c2.font.size = Pt(10.5)
        p_c2.font.bold = True
        p_c2.font.color.rgb = C_BLUE

    # -------------------------------------------------------------
    # SLIDE 12: TIMELINE OF THE PROJECT (8 WEEKS PLAN)
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Timeline of the Project (8-Week Work Plan)")

    timeline_data = [
        ("WEEKS 1 - 2", "Requirement Gathering & Architecture Design", "Analyzed campus workflows, drafted WAD design document, set up Git repository in VS Code."),
        ("WEEK 3", "Frontend Replica & EJS Layout Modeling", "Built psgtech.edu UI replica, responsive Bootstrap 5 components, and shared EJS partials."),
        ("WEEK 4 (CURRENT)", "REVIEW 1: 30% Workable Modules Completion", "Persistent chatbot widget, auto-redirection engine, sessionStorage state, and local MongoDB Compass logging."),
        ("WEEK 5", "Knowledge Base Expansion & AI Optimization", "Enhanced local knowledge base with 50+ topics, integrated Gemini 1.5 Flash SDK, and tuned guardrails."),
        ("WEEK 6", "Online Services & Digital Certificate Module", "Functional Bonafide application, hostel pass generation, and duplicate hall ticket requisition workflow."),
        ("WEEK 7", "Testing, Security Auditing & RBAC Hardening", "Cross-browser verification, mobile responsiveness testing, and security rule assessment."),
        ("WEEK 8", "FINAL REVIEW: Deployment & Documentation", "Full platform demonstration, viva evaluation, work diary completion, and repository handoff.")
    ]

    top_y = 1.45
    for wk, title, desc in timeline_data:
        box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_y), Inches(11.7), Inches(0.72))
        box.fill.solid()
        if "CURRENT" in wk:
            box.fill.fore_color.rgb = RGBColor(254, 243, 199)
            box.line.color.rgb = C_GOLD
            box.line.width = Pt(2)
        else:
            box.fill.fore_color.rgb = C_LIGHT
            box.line.color.rgb = C_BLUE
            box.line.width = Pt(1)

        tb_box = s12.shapes.add_textbox(Inches(0.9), Inches(top_y + 0.04), Inches(11.5), Inches(0.65))
        tf_b = tb_box.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = f"• {wk}:  {title} — {desc}"
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_NAVY if "CURRENT" in wk else C_DARK

        top_y += 0.77

    # -------------------------------------------------------------
    # SLIDE 13: CONCLUSION SLIDE
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Conclusion & Review 1 Summary")

    tb = s13.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2))
    tf = tb.text_frame

    concl = [
        "Milestone Achieved: Successfully completed 30%+ workable modules for Review 1 strictly adhering to the WAD syllabus.",
        "Syllabus-Compliant Stack: Built using Node.js, Express.js, EJS templates, Bootstrap 5.3, and local MongoDB Compass without external React overhead.",
        "Continuous Navigation Solved: Overcame the traditional multi-page reset issue by coupling browser sessionStorage with automated redirection.",
        "Security & Integrity: Enforced role-based document authorization and strict campus boundary guardrails to protect institutional information.",
        "Next Steps: Ready to proceed into Week 5 for automated certificate approvals and administrative analytics dashboard."
    ]

    for c in concl:
        p = tf.add_paragraph()
        p.text = f"• {c}"
        p.font.name = 'Arial'
        p.font.size = Pt(14)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 14: THANKS & SUGGESTIONS SLIDE
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = C_NAVY
    bg14.line.color.rgb = C_NAVY

    card14 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    card14.fill.solid()
    card14.fill.fore_color.rgb = C_WHITE
    card14.line.color.rgb = C_GOLD
    card14.line.width = Pt(3)

    tb = s14.shapes.add_textbox(Inches(1.8), Inches(1.8), Inches(9.7), Inches(3.8))
    tf = tb.text_frame
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "THANK YOU!"
    p1.font.name = 'Arial'
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = C_BLUE

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Questions, Feedback & Faculty Suggestions Welcome"
    p2.font.name = 'Arial'
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_GOLD

    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "\nPSG NEXUS (CHAT-BOT) • TEAM 1\nLaxman B (26MX209) • Karthikeyan S (26MX110) • Mohamed Abdul Basith A A (26MX115)\nGuide: Ms. J. Gowri Thangam"
    p3.font.name = 'Arial'
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_GRAY

    p4 = tf.add_paragraph()
    p4.alignment = PP_ALIGN.CENTER
    p4.text = "\nProject Repository: https://github.com/Abdul-Basith-AA/psgNEXUS"
    p4.font.name = 'Arial'
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = C_BLUE

    output_path = "PSG_Nexus_WAD_Review1_Presentation.pptx"
    prs.save(output_path)
    print(f"[OK] Generated PPT successfully: {output_path}")

if __name__ == '__main__':
    create_presentation()
