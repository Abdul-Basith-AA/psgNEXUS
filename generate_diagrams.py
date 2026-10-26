import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('docs_assets', exist_ok=True)

# Helper function to get a good font
def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{fn}", size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_flow_diagram():
    # Width 1200, Height 900
    img = Image.new('RGB', (1200, 920), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(26, bold=True)
    box_font = get_font(18, bold=True)
    text_font = get_font(15, bold=False)
    small_font = get_font(13, bold=False)

    # Title
    draw.text((600, 35), "PSG NEXUS - SYSTEM FLOW DIAGRAM", fill='#1B294B', font=title_font, anchor='mm')
    draw.line([(250, 55), (950, 55)], fill='#2B4BAB', width=3)

    def draw_box(x, y, w, h, text_title, text_sub="", bg='#F0F4FA', border='#2B4BAB', radius=10):
        # Draw rounded rectangle
        draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg, outline=border, width=2)
        if text_sub:
            draw.text((x + w/2, y + h/2 - 12), text_title, fill='#1B294B', font=box_font, anchor='mm')
            draw.text((x + w/2, y + h/2 + 14), text_sub, fill='#555555', font=text_font, anchor='mm')
        else:
            draw.text((x + w/2, y + h/2), text_title, fill='#1B294B', font=box_font, anchor='mm')

    def draw_decision(cx, cy, rx, ry, text_title, bg='#FFF8E6', border='#D4AF37'):
        pts = [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
        draw.polygon(pts, fill=bg, outline=border)
        # Re-draw outline with width
        for i in range(4):
            draw.line([pts[i], pts[(i+1)%4]], fill=border, width=2)
        draw.text((cx, cy), text_title, fill='#1B294B', font=box_font, anchor='mm')

    def draw_arrow(x1, y1, x2, y2, label="", color='#2B4BAB', width=2):
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
        # Arrowhead
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arr_len = 10
        p1 = (x2 - arr_len * math.cos(angle - math.pi/6), y2 - arr_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arr_len * math.cos(angle + math.pi/6), y2 - arr_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=color)
        if label:
            # offset label
            draw.text(((x1 + x2)/2 + 10, (y1 + y2)/2 - 10), label, fill='#1B294B', font=small_font)

    # 1. Start Box
    draw_box(460, 80, 280, 50, "User Opens PSG Tech Portal", "Loads Homepage with Chatbot", bg='#E8F0FE', border='#2B4BAB', radius=25)

    # Arrow down
    draw_arrow(600, 130, 600, 160)

    # 2. Role Selection Box
    draw_box(440, 160, 320, 55, "Select / Confirm Role", "Default: Student (Switchable to Faculty/Parent/Visitor)")

    # Arrow down
    draw_arrow(600, 215, 600, 245)

    # 3. Enter Query Box
    draw_box(450, 245, 300, 50, "User Enters Query in Chatbot", "e.g., 'Take me to form filling page'")

    # Arrow down
    draw_arrow(600, 295, 600, 335)

    # 4. Decision: Out of Scope?
    draw_decision(600, 380, 140, 45, "Is Query College Related?", bg='#FFF8E6', border='#D4AF37')

    # No -> Out of scope
    draw_arrow(740, 380, 930, 380, "No (Off-Topic)")
    draw_box(930, 355, 230, 50, "Polite Guardrail Refusal", "Prompt user to ask campus topics", bg='#FFF1F0', border='#CF1322')

    # Yes -> Down to Permission check
    draw_arrow(600, 425, 600, 470, "Yes")

    # 5. Decision: Document Allowed for Role?
    draw_decision(600, 515, 140, 45, "Authorized for User Role?", bg='#FFF8E6', border='#D4AF37')

    # No -> Restricted
    draw_arrow(740, 515, 930, 515, "No (Restricted)")
    draw_box(930, 490, 230, 50, "Show Access Denied Alert", "Staff-only document restriction", bg='#FFF1F0', border='#CF1322')

    # Yes -> Down to Navigation check
    draw_arrow(600, 560, 600, 600, "Yes")

    # 6. Decision: Navigation request?
    draw_decision(600, 645, 140, 45, "Page Redirection Request?", bg='#E8F5E9', border='#2E7D32')

    # Yes -> Navigation
    draw_arrow(460, 645, 280, 645, "Yes (e.g. /forms)")
    draw_box(50, 620, 230, 50, "Prepare Redirect Payload", "Attach Target URL + Countdown", bg='#E8F5E9', border='#2E7D32')

    # Down from 600, 690 to Response generation
    draw_arrow(600, 690, 600, 725, "No / Informational")

    # 7. Knowledge Base / AI Matching
    draw_box(380, 725, 440, 55, "Query Engine & Response Generation", "Matched against Campus Knowledge Base / Gemini AI", bg='#F3E8FF', border='#7E22CE')

    # Link from Prepare Redirect Payload to Query Engine
    draw_arrow(165, 670, 165, 750)
    draw_line_pts = [(165, 750), (380, 750)]
    draw.line(draw_line_pts, fill='#2B4BAB', width=2)
    # arrow head at 380, 750
    draw.polygon([(380, 750), (370, 745), (370, 755)], fill='#2B4BAB')

    # Arrow from 7 to Storage & Response
    draw_arrow(600, 780, 600, 815)

    # 8. Dual Action: MongoDB + SessionStorage
    draw_box(180, 815, 380, 60, "1. Save Record in Local MongoDB", "Persisted in 'psgnexus_db.conversations'", bg='#E6FFFA', border='#0D9488')
    draw_box(640, 815, 380, 60, "2. Update Browser sessionStorage", "Retains chat history & keeps window open", bg='#EFF6FF', border='#3B82F6')

    # Branch arrow to both
    draw_line_pts2 = [(600, 815), (370, 815)]
    draw.line(draw_line_pts2, fill='#2B4BAB', width=2)
    draw_line_pts3 = [(600, 815), (830, 815)]
    draw.line(draw_line_pts3, fill='#2B4BAB', width=2)

    img.save('docs_assets/flow_diagram.png', 'PNG')
    print("[OK] Created docs_assets/flow_diagram.png")

def create_bpmn_diagram():
    img = Image.new('RGB', (1200, 650), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    lane_font = get_font(18, bold=True)
    box_font = get_font(15, bold=True)
    text_font = get_font(13, bold=False)
    small_font = get_font(12, bold=False)

    # Title
    draw.text((600, 30), "PSG NEXUS - BPMN BUSINESS PROCESS MODEL", fill='#1B294B', font=title_font, anchor='mm')
    draw.line([(250, 48), (950, 48)], fill='#2B4BAB', width=2)

    # 3 Swimlanes
    # Lane 1: User / Student (Y: 60 to 220)
    # Lane 2: Web Client & SessionStorage (Y: 220 to 420)
    # Lane 3: Express Backend & MongoDB (Y: 420 to 620)

    lanes = [
        ("STUDENT / USER", 60, 220, '#F8FAFC'),
        ("CLIENT UI & SESSION STORAGE", 220, 420, '#FFFFFF'),
        ("EXPRESS SERVER & MONGODB", 420, 620, '#F8FAFC')
    ]

    for label, y1, y2, bg in lanes:
        draw.rectangle([50, y1, 1150, y2], fill=bg, outline='#94A3B8', width=1)
        # Header banner on left
        draw.rectangle([50, y1, 120, y2], fill='#1E293B', outline='#0F172A', width=1)
        # Vertical text or rotated: draw horizontal short text
        draw.text((85, (y1 + y2)/2), label.split()[0], fill='#FFFFFF', font=box_font, anchor='mm')

    def draw_task(x, y, w, h, t1, t2="", bg='#E0E7FF', border='#4338CA'):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=2)
        if t2:
            draw.text((x + w/2, y + h/2 - 10), t1, fill='#1E1B4B', font=box_font, anchor='mm')
            draw.text((x + w/2, y + h/2 + 10), t2, fill='#475569', font=text_font, anchor='mm')
        else:
            draw.text((x + w/2, y + h/2), t1, fill='#1E1B4B', font=box_font, anchor='mm')

    def draw_event(cx, cy, r, label, is_end=False, fill='#22C55E'):
        if is_end:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill='#FEE2E2', outline='#EF4444', width=3)
            draw.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], fill='#EF4444')
        else:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill='#DCFCE7', outline='#16A34A', width=2)
        draw.text((cx, cy + r + 14), label, fill='#1E293B', font=small_font, anchor='mm')

    def draw_arrow(x1, y1, x2, y2, label="", color='#4338CA'):
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arr_len = 8
        p1 = (x2 - arr_len * math.cos(angle - math.pi/6), y2 - arr_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arr_len * math.cos(angle + math.pi/6), y2 - arr_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=color)
        if label:
            draw.text(((x1 + x2)/2 + 8, (y1 + y2)/2 - 8), label, fill='#1E293B', font=small_font)

    # Events and Tasks
    # Start Event in Lane 1
    draw_event(160, 140, 16, "Visit Portal")

    # Arrow to Task 1
    draw_arrow(176, 140, 230, 140)
    draw_task(230, 110, 160, 60, "Click Assistant", "Choose Role", bg='#FEF3C7', border='#D97706')

    # Arrow to Task 2
    draw_arrow(390, 140, 440, 140)
    draw_task(440, 110, 160, 60, "Type Question", "or Click Prompt", bg='#FEF3C7', border='#D97706')

    # Arrow down to Lane 2: UI Send Request
    draw_arrow(520, 170, 520, 260)
    draw_task(430, 260, 180, 60, "Serialize Message", "POST /api/chat", bg='#E0E7FF', border='#3730A3')

    # Arrow down to Lane 3: Backend Processing
    draw_arrow(520, 320, 520, 460)
    draw_task(420, 460, 200, 60, "Evaluate Guardrails", "& Intent Engine", bg='#F3E8FF', border='#6B21A8')

    # Arrow right to Save Mongo
    draw_arrow(620, 490, 680, 490)
    draw_task(680, 460, 190, 60, "Save Document", "in MongoDB Compass", bg='#CCFBF1', border='#0F766E')

    # Arrow up back to Lane 2: Client response & sessionStorage
    draw_arrow(775, 460, 775, 330)
    draw_task(680, 270, 190, 60, "Update SessionStorage", "& Render Bot Bubble", bg='#E0E7FF', border='#3730A3')

    # Arrow to Redirect Check in Lane 2
    draw_arrow(870, 300, 930, 300)
    draw_task(930, 270, 170, 60, "Handle Redirection", "window.location", bg='#DCFCE7', border='#15803D')

    # Arrow back to Lane 1: User views destination page with chat open
    draw_arrow(1015, 270, 1015, 170)
    draw_task(930, 110, 170, 60, "Browse Destination", "Chatbot stays active", bg='#FEF3C7', border='#D97706')

    # End Event
    draw_arrow(1015, 110, 1015, 80)
    draw_event(1015, 60, 14, "Finished", is_end=True)

    img.save('docs_assets/bpmn_diagram.png', 'PNG')
    print("[OK] Created docs_assets/bpmn_diagram.png")

if __name__ == '__main__':
    create_flow_diagram()
    create_bpmn_diagram()
