import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), val)
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    tblPr.append(tblBorders)

def create_design_document():
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # HEADER SECTION (EXACT TEMPLATE)
    # -------------------------------------------------------------
    p_college = doc.add_paragraph()
    p_college.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_college.paragraph_format.space_before = Pt(0)
    p_college.paragraph_format.space_after = Pt(2)
    run_c = p_college.add_run("PSG COLLEGE OF TECHNOLOGY, COIMBATORE – 641 004")
    run_c.bold = True
    run_c.font.size = Pt(13)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(2)
    run_d = p_dept.add_run("DEPARTMENT OF COMPUTER APPLICATIONS")
    run_d.bold = True
    run_d.font.size = Pt(12)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(0)
    p_course.paragraph_format.space_after = Pt(4)
    run_cr = p_course.add_run("Academic Year 2026-2027         26MX17         WEB APPLICATION DEVELOPMENT")
    run_cr.bold = True
    run_cr.font.size = Pt(11)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(14)
    run_t = p_title.add_run("Design Document")
    run_t.bold = True
    run_t.underline = True
    run_t.font.size = Pt(13)

    # Helper function for Section Headings
    def add_section_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        return p

    # -------------------------------------------------------------
    # I. Team Detail
    # -------------------------------------------------------------
    add_section_heading("I.    Team Detail")

    table_team = doc.add_table(rows=4, cols=4)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_team)

    col_widths = [Inches(1.5), Inches(1.2), Inches(2.0), Inches(2.0)]
    headers = ["Team No. & Name", "Roll No.", "Name of the student", "Name of the Faculty Guide"]

    hdr_cells = table_team.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10.5)

    team_data = [
        ("Team 12\nPSG Nexus", "26MX101", "Abdul Basith A", "Ms. A. Kalyani\nAssistant Professor, CA"),
        ("Team 12\nPSG Nexus", "26MX102", "Karthikeyan S", "Ms. A. Kalyani\nAssistant Professor, CA"),
        ("Team 12\nPSG Nexus", "26MX103", "Laxman R", "Ms. A. Kalyani\nAssistant Professor, CA")
    ]

    for row_idx, data in enumerate(team_data, start=1):
        row_cells = table_team.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=120, right=120)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # II. Title of the Application
    # -------------------------------------------------------------
    add_section_heading("II.   Title of the Application")

    table_title = doc.add_table(rows=1, cols=1)
    table_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_title)
    cell = table_title.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("PSG NEXUS – Intelligent Role-Based Campus Digital Assistant and Navigation Portal for PSG College of Technology")
    r.bold = True
    r.font.size = Pt(11)

    # -------------------------------------------------------------
    # III. Overview of the Project ( minimum 100 words )
    # -------------------------------------------------------------
    add_section_heading("III. Overview of the Project ( minimum 100 words )")

    table_overview = doc.add_table(rows=1, cols=1)
    table_overview.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_overview)
    cell = table_overview.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
    
    overview_text = (
        "PSG College of Technology is a large autonomous institution with many departments, academic regulations, "
        "and student services. Currently, when students, parents, or visitors visit the college website, finding specific "
        "details like attendance rules, internal Continuous Assessment (CA) calculation, syllabus copies, hostel gate rules, "
        "or certificate application forms requires clicking through multiple nested menus and reading through long PDF circulars.\n\n"
        "PSG Nexus is developed to solve this issue by providing a single-point interactive digital assistant directly on the "
        "campus portal. We built a responsive replica of the official PSG Tech website matching the institutional identity, "
        "with an AI assistant floating at the bottom-left corner. The assistant is built using Node.js, Express, EJS templates, "
        "Bootstrap 5, and JavaScript. It provides immediate, human-friendly answers to frequent college questions and can automatically "
        "redirect users to dedicated pages—such as the Online Form Filling Portal or the Syllabus Repository—while keeping the chat window "
        "open and preserving conversation history through browser session storage.\n\n"
        "The application also implements role-based access control. While students can readily access academic guidelines, exam schedules, "
        "and certificate request forms, sensitive faculty documents such as academic council meeting minutes and staff payroll records "
        "are strictly restricted from student view. Furthermore, all student interactions are logged in real time to a local MongoDB "
        "database, allowing college administrators to identify common student issues and continuously improve campus support."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(overview_text)
    r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # IV. Existing System - Description with the link to the application. Minimum 2 should be mentioned.
    # -------------------------------------------------------------
    add_section_heading("IV. Existing System  -  Description with the link to the application. Minimum 2 should be mentioned.")

    table_existing = doc.add_table(rows=1, cols=1)
    table_existing.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_existing)
    cell = table_existing.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    p1 = cell.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p1.add_run("1. PSG College of Technology Official Website (Link: https://www.psgtech.edu/)\n")
    r1.bold = True
    r1.font.size = Pt(10.5)
    r2 = p1.add_run(
        "• Description: The official portal of PSG Tech acts as the central information repository for the college. "
        "It publishes college news, admission announcements, tenders, department details, and links to external portals like Studzone. "
        "However, it is purely a static informational website with traditional dropdown navigation. There is no automated help assistant "
        "or search chatbot. When first-year students or parents visit the portal, they often struggle to locate specific information such as "
        "hostel rules, condonation criteria, or fee payment procedures without manually searching across multiple sub-pages.\n\n"
    )
    r2.font.size = Pt(10.5)

    r3 = p1.add_run("2. Anna University Student COE Web Portal (Link: https://coe1.annauniv.edu/)\n")
    r3.bold = True
    r3.font.size = Pt(10.5)
    r4 = p1.add_run(
        "• Description: The Controller of Examinations portal of Anna University is used by affiliated and autonomous college students "
        "to check exam schedules, internal marks, and semester results. While it serves transactional examination needs, it lacks any interactive "
        "guidance mechanism. If a student has doubts regarding grade point formulas, revaluation timelines, or photocopy requests, there is no "
        "conversational support available to guide them to the correct procedure."
    )
    r4.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # VI. Objectives of the Proposed Application (Template jumps from IV to VI)
    # -------------------------------------------------------------
    add_section_heading("VI. Objectives of the Proposed Application")

    table_obj = doc.add_table(rows=1, cols=1)
    table_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_obj)
    cell = table_obj.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    obj_text = (
        "1. To develop a responsive web portal representing PSG College of Technology with an integrated, floating AI digital assistant.\n"
        "2. To provide quick, 100% accurate responses to routine college questions regarding minimum attendance (75%), CAT continuous "
        "assessment calculations (50 marks), autonomous grading scales, hostel rules, and placement statistics.\n"
        "3. To implement an automated page redirection feature that smoothly guides users to relevant pages (e.g., from Home to the Online "
        "Form Filling Portal) while preserving conversation state and keeping the chat window open using browser sessionStorage.\n"
        "4. To enforce role-based access control (RBAC) so that authenticated faculty members can view internal meeting records, while "
        "students and visitors are restricted from viewing confidential files.\n"
        "5. To include an out-of-scope guardrail filter that ensures the chatbot remains professional and answers only questions related "
        "to the college and campus life.\n"
        "6. To store all conversations, roles, queries, and server responses in a local MongoDB database so that campus administrators "
        "can view student queries directly using MongoDB Compass."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(obj_text)
    r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # VII. Scope / Use
    # -------------------------------------------------------------
    add_section_heading("VII. Scope / Use")

    table_scope = doc.add_table(rows=1, cols=1)
    table_scope.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_scope)
    cell = table_scope.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    scope_text = (
        "• Scope:\n"
        "The project is designed for the students, faculty members, parents, alumni, and prospective visitors of PSG College of Technology. "
        "It acts as a 24/7 digital campus guide and automated navigation hub across web browsers on desktops, laptops, and mobile devices.\n\n"
        "• Practical Use:\n"
        "1. For Students: Instantly clarify attendance rules, internal assessment weightage, library book limits, hostel in-times (8:30 PM), "
        "and navigate straight to the online form filling portal to request Bonafide certificates or hall tickets.\n"
        "2. For Parents: Quickly access tuition and hostel fee payment schedules, hostel warden phone numbers, and TNEA cutoff trends without confusion.\n"
        "3. For Faculty: Obtain quick access to leave application forms, syllabus revision guidelines, and department meeting notices.\n"
        "4. For Visitors & Applicants: Learn about autonomous degree programmes, NAAC A+ accreditation status, NIRF ranking, and campus directions.\n"
        "5. For College Administration: Monitor student queries via MongoDB Compass to understand common difficulties and post timely announcements."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(scope_text)
    r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # VIII. Technology to be used
    # -------------------------------------------------------------
    add_section_heading("VIII. 	Technology to be used")

    table_tech = doc.add_table(rows=1, cols=1)
    table_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_tech)
    cell = table_tech.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    tech_text = (
        "• Frontend Technologies:\n"
        "  - HTML5 & CSS3: Structuring web pages and applying custom PSG Tech brand styling (Navy Blue #2B4BAB and Gold #F4DE88).\n"
        "  - Bootstrap 5.3 Framework: Building responsive navigation bars, carousels, cards, grids, and dialog modals.\n"
        "  - Vanilla JavaScript (ES6): Handling DOM manipulation, client-side event listeners, typing animations, and redirection timers.\n\n"
        "• Templating & Server Architecture:\n"
        "  - EJS (Embedded JavaScript): Dynamic server-side rendering with reusable layout partials (header.ejs, footer.ejs, chatbot.ejs).\n"
        "  - Node.js & Express.js: Robust backend runtime and web server managing routing, static files, and the /api/chat endpoint.\n\n"
        "• Session & State Management:\n"
        "  - Browser sessionStorage: Preserving active chat logs, current user role, and open/closed widget state across multi-page navigation.\n\n"
        "• Database & Storage:\n"
        "  - MongoDB (Local Storage): Storing conversation documents, timestamps, and roles in 'psgnexus_db' via Mongoose ODM.\n"
        "  - MongoDB Compass: Desktop GUI tool used for inspecting live student query records.\n\n"
        "• AI & Natural Language Processing:\n"
        "  - Built-in Campus Knowledge Engine: Local keyword scoring and intent classification for instant offline answers during reviews.\n"
        "  - Google GenAI SDK (@google/genai): Free-tier integration with Gemini 1.5 Flash for answering open-ended campus questions."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(tech_text)
    r.font.size = Pt(10)

    # -------------------------------------------------------------
    # IX. Functional Requirements of the Application
    # -------------------------------------------------------------
    add_section_heading("IX. Functional Requirements of the Application")

    table_func = doc.add_table(rows=1, cols=1)
    table_func.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_func)
    cell = table_func.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    func_text = (
        "1. Institutional Role Management: The application defaults to the 'Student' role for immediate use, while allowing users "
        "to switch between Student, Faculty, Parent, and Visitor roles via an in-chat selector.\n"
        "2. Campus Question Answering: The chatbot processes user text and provides structured answers regarding attendance rules (75%), "
        "Continuous Assessment tests (CAT), autonomous GPA calculations, hostel timings (8:30 PM), library facilities, and placements.\n"
        "3. Out-of-Scope Query Guardrail: The backend scans incoming messages for non-college topics (e.g., movies, gaming, politics, external programming) "
        "and returns a polite refusal message reminding users to ask campus-related questions.\n"
        "4. Role-Based Document Access Control: If a student asks for confidential faculty files (e.g., academic council meeting minutes or staff payroll), "
        "the system rejects the request with an 'Access Restricted' warning, but approves it when queried under the Faculty role.\n"
        "5. Automated Multi-Page Redirection: When the user requests a specific section (e.g., 'take me to form filling page' or 'show syllabus'), "
        "the chatbot displays a confirmation with an animated progress bar and redirects the browser window to that page.\n"
        "6. Cross-Page Session Persistence: The conversation history, active role, and widget visibility are saved in sessionStorage, "
        "ensuring the chat stays open and continues seamlessly after redirecting to another page.\n"
        "7. Database Logging: Every user message, role, response, and timestamp are saved asynchronously into MongoDB under the 'conversations' collection.\n"
        "8. Online Form Filling Services: A functional forms portal where students can submit online requests for Bonafide certificates, hostel outing slips, "
        "and duplicate hall tickets with confirmation popups."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(func_text)
    r.font.size = Pt(10)

    # -------------------------------------------------------------
    # X. Non-Functional Requirements of the Application
    # -------------------------------------------------------------
    add_section_heading("X. Non-Functional Requirements of the Application")

    table_nonfunc = doc.add_table(rows=1, cols=1)
    table_nonfunc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_nonfunc)
    cell = table_nonfunc.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    nonfunc_text = (
        "1. Usability & User Experience: The portal faithfully replicates the official PSG Tech website design (>90% match) with clean typography, "
        "accessible navigation, and an intuitive bottom-left floating chatbot with animated pulse indicators.\n"
        "2. Performance & Speed: Local knowledge base matches respond within 50 milliseconds, providing an instant conversational experience "
        "without noticeable latency.\n"
        "3. Offline Reliability: The application runs completely offline during lab tests and viva evaluations using its local database and knowledge engine, "
        "ensuring zero dependency on live internet connectivity.\n"
        "4. Security & Privacy: Sensitive faculty information is protected through role-based access rules, and secret API keys are kept safely in server environment variables.\n"
        "5. Cross-Browser Compatibility: Compatible across major modern web browsers including Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari.\n"
        "6. Maintainability: Structured using standard Model-View-Controller (MVC) principles with clean separation between EJS views, static assets, and Express route controllers."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(nonfunc_text)
    r.font.size = Pt(10)

    # -------------------------------------------------------------
    # XI. Flow diagram of the Application
    # -------------------------------------------------------------
    add_section_heading("XI. Flow diagram of the Application")

    p_flow_desc = doc.add_paragraph()
    p_flow_desc.paragraph_format.space_before = Pt(2)
    p_flow_desc.paragraph_format.space_after = Pt(6)
    r_fd = p_flow_desc.add_run(
        "The following diagram illustrates the complete operational workflow of the PSG Nexus application, "
        "showing role selection, query evaluation, boundary filtering, document security checks, page redirection, "
        "and dual persistence to MongoDB Compass and browser session storage:"
    )
    r_fd.font.size = Pt(10.5)

    if os.path.exists('docs_assets/flow_diagram.png'):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_after = Pt(4)
        run_img1 = p_img1.add_run()
        run_img1.add_picture('docs_assets/flow_diagram.png', width=Inches(6.2))

        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(12)
        r_c1 = p_cap1.add_run("Figure 1: Complete System Flow Diagram of PSG Nexus")
        r_c1.bold = True
        r_c1.font.size = Pt(10)

    # -------------------------------------------------------------
    # XII. Interface/prototype of the proposed Application
    # -------------------------------------------------------------
    add_section_heading("XII. Interface/prototype of the proposed Application  - < use any wireframe tools or HTML &CSS coding >")

    p_proto_desc = doc.add_paragraph()
    p_proto_desc.paragraph_format.space_before = Pt(2)
    p_proto_desc.paragraph_format.space_after = Pt(6)
    r_pd = p_proto_desc.add_run(
        "The working prototype of PSG Nexus was developed using HTML5, CSS3, Bootstrap 5.3, and EJS templates, "
        "running locally on Node.js at http://localhost:3000. Below are the actual running interface screens:"
    )
    r_pd.font.size = Pt(10.5)

    # Screenshot 1
    if os.path.exists('docs_assets/screenshot1_portal.png'):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture('docs_assets/screenshot1_portal.png', width=Inches(6.0))

        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(10)
        r_c2 = p_cap2.add_run("Figure 2: Homepage Interface of PSG Nexus Portal with Bottom-Left Assistant Launcher")
        r_c2.bold = True
        r_c2.font.size = Pt(10)

        p_desc2 = doc.add_paragraph()
        p_desc2.paragraph_format.space_after = Pt(12)
        r_d2 = p_desc2.add_run(
            "• Description of Screen: Figure 2 displays the homepage replicating the official PSG College of Technology portal. "
            "It showcases the top announcement bar, royal blue navigation header, portal tiles (Online Forms, Curriculum, Admissions, Hostels, Library), "
            "recent circulars, and the floating PSG Nexus AI logo positioned at the bottom-left corner."
        )
        r_d2.font.size = Pt(10)

    # Screenshot 2
    if os.path.exists('docs_assets/screenshot2_assistant.png'):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_after = Pt(4)
        run_img3 = p_img3.add_run()
        run_img3.add_picture('docs_assets/screenshot2_assistant.png', width=Inches(4.5))

        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.paragraph_format.space_after = Pt(10)
        r_c3 = p_cap3.add_run("Figure 3: Interactive PSG Nexus Chatbot Interface (Student Role & Quick Prompts)")
        r_c3.bold = True
        r_c3.font.size = Pt(10)

        p_desc3 = doc.add_paragraph()
        p_desc3.paragraph_format.space_after = Pt(14)
        r_d3 = p_desc3.add_run(
            "• Description of Screen: Figure 3 displays the active PSG Nexus Assistant dialog window. "
            "It features the custom robot logo avatar, role indicator badge ('STUDENT'), quick clickable prompt chips "
            "(e.g., 'Take me to form filling page', 'What is the minimum attendance?'), and message input box connected to the Express backend and local MongoDB."
        )
        r_d3.font.size = Pt(10)

    # -------------------------------------------------------------
    # XIII. (Optional) BPMN diagram of the proposed application
    # -------------------------------------------------------------
    add_section_heading("XIII.  (Optional)   BPMN diagram of the proposed application")

    p_bpmn_desc = doc.add_paragraph()
    p_bpmn_desc.paragraph_format.space_before = Pt(2)
    p_bpmn_desc.paragraph_format.space_after = Pt(6)
    r_bd = p_bpmn_desc.add_run(
        "Figure 4 shows the Business Process Model and Notation (BPMN) diagram illustrating the sequence of interactions across "
        "three primary swimlanes: the Student/User, the Client UI & SessionStorage, and the Express Server & MongoDB Database:"
    )
    r_bd.font.size = Pt(10.5)

    if os.path.exists('docs_assets/bpmn_diagram.png'):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.paragraph_format.space_after = Pt(4)
        run_img4 = p_img4.add_run()
        run_img4.add_picture('docs_assets/bpmn_diagram.png', width=Inches(6.2))

        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.paragraph_format.space_after = Pt(20)
        r_c4 = p_cap4.add_run("Figure 4: BPMN Business Process Model of PSG Nexus")
        r_c4.bold = True
        r_c4.font.size = Pt(10)

    # -------------------------------------------------------------
    # SIGNATURE BLOCK (EXACT TEMPLATE)
    # -------------------------------------------------------------
    doc.add_paragraph().paragraph_format.space_after = Pt(15)

    table_sig = doc.add_table(rows=1, cols=2)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    # No visible borders for signature line
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'none')
        tblBorders.append(b)
    table_sig._tbl.tblPr.append(tblBorders)

    sig_left = table_sig.rows[0].cells[0]
    sig_right = table_sig.rows[0].cells[1]

    p_sig_l = sig_left.paragraphs[0]
    p_sig_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_sl = p_sig_l.add_run("Signature of the students\n\n\n1. __________________________\n\n2. __________________________\n\n3. __________________________")
    r_sl.bold = True
    r_sl.font.size = Pt(11)

    p_sig_r = sig_right.paragraphs[0]
    p_sig_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sr = p_sig_r.add_run("Signature of the Guide\n\n\n\n__________________________\n(Ms. A. Kalyani)")
    r_sr.bold = True
    r_sr.font.size = Pt(11)

    output_filename = "WAD_Project_Design_Document_PSG_Nexus.docx"
    doc.save(output_filename)
    print(f"[OK] Generated Word Document successfully: {output_filename}")

if __name__ == '__main__':
    create_design_document()
