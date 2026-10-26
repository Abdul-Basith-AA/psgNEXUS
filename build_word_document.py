import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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

    # Set Margins (0.8 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

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

    def add_section_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
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

    col_widths = [Inches(1.5), Inches(1.2), Inches(2.2), Inches(1.9)]
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
        ("Team 1\nPSG Nexus", "26MX209", "Laxman B", "Ms. J. Gowri Thangam\nAssistant Professor, CA"),
        ("Team 1\nPSG Nexus", "26MX110", "Karthikeyan S", "Ms. J. Gowri Thangam\nAssistant Professor, CA"),
        ("Team 1\nPSG Nexus", "26MX115", "Mohamed Abdul Basith A A", "Ms. J. Gowri Thangam\nAssistant Professor, CA")
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
    r = p.add_run("PSG Nexus (Chat-Bot)")
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
        "PSG Nexus is a helpful digital assistant created just for the PSG College website. Our main goal is to give quick and "
        "personalized support to students, teachers, parents, alumni, and visitors based on what they need. It acts as a single, "
        "easy-to-use guide where users can find reliable information about courses, academic departments, admissions, college events, "
        "fee details, syllabus copies, campus facilities, and other important institutional resources.\n\n"
        "This tool lets users easily move around the college website while the assistant stays active on the screen to help them at any time. "
        "Unlike conventional chatbots that reset upon opening another webpage, PSG Nexus maintains session continuity using browser session "
        "storage, meaning you get continuous support and clear directions without having to search for things manually or retype questions. "
        "The system also introduces intelligent page redirection—for instance, when a user asks to fill a bonafide or hostel leave form, "
        "the chatbot directs them straight to the Online Forms Portal while keeping the conversation open.\n\n"
        "Additionally, role-based access ensures that while students and visitors receive clear public guidance on academics and hostel rules, "
        "confidential staff circulars remain restricted. All queries and interactions are stored in a local MongoDB database to help the college "
        "understand student requirements. By providing fast and trustworthy answers, PSG Nexus makes using the website a much better experience "
        "and helps build a more connected and efficient digital campus for everyone."
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
        "It publishes college news, admission announcements, tenders, department details, and links to external portals. "
        "However, it is a static informational website with traditional dropdown navigation and does not have any chatbot or automated assistant. "
        "When first-year students or parents visit the portal, they have to navigate the site by themselves and find specific information "
        "(like hostel rules or fee procedures) manually by clicking through multiple sub-pages, which can be time-consuming.\n\n"
    )
    r2.font.size = Pt(10.5)

    r3 = p1.add_run("2. PSG Tech Studzone / Student Services Portal (Link: https://studzone.psgtech.ac.in/)\n")
    r3.bold = True
    r3.font.size = Pt(10.5)
    r4 = p1.add_run(
        "• Description: Studzone is the primary student portal used by PSG Tech students for viewing internal marks, attendance logs, and exam fee payments. "
        "While it serves transactional academic requirements, it lacks any conversational guidance or virtual helpdesk. If a student has questions regarding "
        "attendance condonation limits (65%-74%), CAT assessment weightage, or how to apply for bonafide certificates, they must either consult the academic "
        "handbook or visit the department office in person. There is no instant digital assistant to guide them directly to the appropriate form or procedure."
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
        "• To develop an intelligent, context-aware chatbot serving as a unified digital guide for the PSG College ecosystem.\n"
        "• To deliver instant, 24/7 access to crucial institutional information regarding academics, admissions, fees, and campus amenities.\n"
        "• To elevate the user experience (UX) by significantly reducing the time required to retrieve syllabus, circulars, and form details.\n"
        "• To implement tailored, role-based assistance addressing the varying intents of students, faculty, parents, alumni, and visitors.\n"
        "• To enable automated in-browser page redirection (e.g., navigating directly to the Online Forms Portal or Syllabus repository) "
        "while keeping the chatbot session continuously active and conversations preserved across page transitions.\n"
        "• To safeguard institutional confidentiality through role-based access control, ensuring students cannot access private staff files, "
        "and logging all conversation data to local MongoDB storage for administrative review."
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
        "The application is integrated as a persistent, floating interactive widget in the bottom-left corner of the PSG College website. "
        "It covers key institutional domains including departmental directories, syllabus repositories, admission guidelines, campus events, "
        "hostel rules, and online student form filling services.\n\n"
        "• Use Cases:\n"
        "1. Prospective Students & Parents: Navigating admission procedures, checking TNEA cutoff trends, understanding fee structures, and exploring hostel/campus facilities.\n"
        "2. Current Students: Clarifying attendance criteria (75%), Continuous Assessment marks (CAT), CGPA calculation, hostel in-times (8:30 PM), "
        "and submitting requests for Bonafide certificates or duplicate hall tickets.\n"
        "3. Faculty & Staff: Obtaining quick access to leave application procedures, academic council schedules, and syllabus revision memos.\n"
        "4. Visitors & Alumni: Accessing campus directions, alumni association updates (Laudea), and institutional NIRF / NAAC accreditation details.\n"
        "5. Campus Administration: Viewing stored conversation logs in MongoDB Compass to recognize frequently asked student queries and address bottlenecks."
    )
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(scope_text)
    r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # VIII. Technology to be used (ACCURATE WAD SYLLABUS STACK)
    # -------------------------------------------------------------
    add_section_heading("VIII. 	Technology to be used")

    table_tech = doc.add_table(rows=1, cols=1)
    table_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_tech)
    cell = table_tech.rows[0].cells[0]
    set_cell_margins(cell, top=140, bottom=140, left=160, right=160)

    tech_text = (
        "• Frontend Technologies:\n"
        "  - HTML5 & CSS3: Page structuring and responsive layout conforming to the official PSG Tech website design.\n"
        "  - Bootstrap 5.3: Responsive navigation bars, hero carousel, cards, and modal dialogs with PSG brand styling.\n"
        "  - JavaScript (ES6): Interactive client-side behavior, floating widget toggling, auto-redirection timers, and input validation.\n\n"
        "• Server-Side & Templating Engine:\n"
        "  - Node.js: Cross-platform, asynchronous JavaScript runtime environment for executing the backend script.\n"
        "  - Express.js: Web application framework for handling HTTP routing, static asset serving, and RESTful API endpoints (/api/chat).\n"
        "  - EJS (Embedded JavaScript): Template engine for server-side dynamic rendering with shared partials (header.ejs, footer.ejs, chatbot.ejs).\n\n"
        "• Client-Side Session & State Management:\n"
        "  - Browser sessionStorage: Preserves conversation history, user role, and widget visibility across page navigation without database reload overhead.\n\n"
        "• Database & Storage:\n"
        "  - MongoDB (Local Storage): Document-oriented database for logging chat sessions, roles, timestamps, and status into 'psgnexus_db'.\n"
        "  - MongoDB Compass: Official GUI client used to inspect and verify stored conversation collections.\n\n"
        "• AI / NLP Engine:\n"
        "  - Built-in Campus Knowledge Engine: Local keyword-scoring algorithm delivering fast, offline-ready answers to 50+ college topics.\n"
        "  - Google GenAI SDK (@google/genai): Integration with Gemini 1.5 Flash for answering open-ended campus queries."
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
        "1. Role Identification & Intent Recognition: The system defaults to the 'Student' role for immediate usability and accurately "
        "categorizes user queries, tailoring responses based on the user's role (Student, Faculty, Parent, Visitor).\n"
        "2. Continuous Session Management: The chatbot maintains conversational context and persists across different pages of the website "
        "using browser sessionStorage without resetting or losing previous chat messages.\n"
        "3. Automated Page Redirection: The system detects navigation requests (e.g., 'take me to form filling page' or 'show syllabus') "
        "and triggers automatic redirection with a countdown banner while keeping the chat open.\n"
        "4. Out-of-Scope Boundary Guardrail: Queries unrelated to PSG Tech (such as entertainment, general sports, or external coding) "
        "are filtered out and handled with a polite refusal prompting the user to ask college-related questions.\n"
        "5. Role-Based Document Access Control: Confidential faculty records (e.g., academic council meeting minutes or staff payroll) "
        "are restricted when queried under Student/Visitor roles and approved only for verified Faculty sessions.\n"
        "6. Local Database Logging: Every conversation exchange (user query, bot response, user role, status, and timestamp) is stored "
        "asynchronously in local MongoDB under the 'conversations' collection.\n"
        "7. Online Form Submission Services: Provides interactive student service forms for Bonafide certificates, hostel outing passes, "
        "and duplicate hall tickets with dynamic reference ID generation."
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
        "• Performance: Chatbot response time must be under 1.5 seconds (under 50ms for local knowledge base matching) to ensure a fluid conversational experience.\n"
        "• Availability & Offline Reliability: The system architecture guarantees high availability and includes complete offline operational capability "
        "during lab reviews and network downtimes.\n"
        "• Usability: The UI widget is non-intrusive, placed at the bottom-left with intuitive launcher icons, clear typography, and responsive layout across desktop, tablet, and mobile devices.\n"
        "• Visual Consistency: The web portal closely replicates (>90% match) the visual identity of the official PSG College of Technology website (Royal Blue #2B4BAB and Gold accents).\n"
        "• Security & Privacy: Role-based authorization prevents unauthorized access to internal staff records. All sensitive server keys are maintained securely in environment variables."
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
        "Figure 1 illustrates the complete operational flow of the PSG Nexus application, detailing the role selection, "
        "boundary guardrail check, authorization filter, navigation intent evaluation, dual-tier response generation, "
        "and asynchronous storage into MongoDB and browser session storage:"
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
        r_c1 = p_cap1.add_run("Figure 1: Complete System Flow Diagram of PSG Nexus Application")
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
        p_cap2.paragraph_format.space_after = Pt(8)
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
        p_cap3.paragraph_format.space_after = Pt(8)
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
    r_sl = p_sig_l.add_run("Signature of the students\n\n\n1. __________________________ (26MX209)\n\n2. __________________________ (26MX110)\n\n3. __________________________ (26MX115)")
    r_sl.bold = True
    r_sl.font.size = Pt(11)

    p_sig_r = sig_right.paragraphs[0]
    p_sig_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sr = p_sig_r.add_run("Signature of the Guide\n\n\n\n__________________________\n(Ms. J. Gowri Thangam)")
    r_sr.bold = True
    r_sr.font.size = Pt(11)

    output_filename = "WAD_Project_Design_Document_PSG_Nexus.docx"
    doc.save(output_filename)
    print(f"[OK] Generated Word Document successfully: {output_filename}")

if __name__ == '__main__':
    create_design_document()
