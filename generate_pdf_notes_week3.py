import os
import re
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, XPreformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to add running headers and footers with dynamic page count.
    Suppress header/footer on page 1 (cover page).
    Matches Week 2 template styles.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Draw beautiful top block background decoration for cover page (Week 1/2 Style)
            self.saveState()
            
            # Dark navy block at top
            self.setFillColor(colors.HexColor("#1A365D"))
            self.rect(0, 440, 612, 792 - 440, fill=True, stroke=False)
            
            # Light blue circle decoration in top right
            self.setFillColor(colors.HexColor("#2B6CB0"))
            self.circle(580, 750, 100, fill=True, stroke=False)
            
            # Bright blue horizontal strip separating top block from bottom block
            self.setFillColor(colors.HexColor("#3182CE"))
            self.rect(0, 420, 612, 20, fill=True, stroke=False)
            
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Draw running header left
        self.drawString(54, 750, "WEEK THREE: FILE HANDLING, DATA ANALYSIS & DATABASES")
        
        # Draw running header right
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "Python Learning Journey")
        
        # Header line separator
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612-54, 742)
        
        # Draw running footer left
        self.setFont("Helvetica", 8)
        self.drawString(54, 40, "Reference Study Guide")
        
        # Draw running footer right
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 40, page_text)
        
        # Footer line separator
        self.line(54, 52, 612-54, 52)
        
        self.restoreState()

# Emoji strip regex
emoji_pattern = re.compile(
    '['
    '\U0001f000-\U0001f9ff'  # Miscellaneous Symbols and Pictographs, etc.
    '\U0001fa00-\U0001faff'  # Symbols and Pictographs Extended-A
    '\u2600-\u27bf'          # Miscellaneous Symbols, Dingbats
    ']+', flags=re.UNICODE
)

def clean_heading(text):
    """
    Strips emojis from headings and reformats Day titles into clean topic numbers.
    """
    text = emoji_pattern.sub('', text)
    text = text.strip()
    
    # Map Day headings to clean continuous numbering
    HEADING_MAP = {
        "Day 12": "1. File Handling",
        "Day 13": "2. Introduction to Pandas & Data Analysis",
        "Day 14": "3. Data Cleaning & Feature Engineering",
        "Day 15": "4. Introduction to DBMS & PostgreSQL Basics",
        "Day 16": "5. SQLite3 & Authentication Simulation"
    }
    
    for key, val in HEADING_MAP.items():
        if key in text:
            return val
            
    return text

def escape_and_format(text):
    """
    Escape XML entities and parse markdown inline styles:
    - **bold** to <b>bold</b>
    - *italic* to <i>italic</i>
    - `code` to courier font with highlight color
    - [link](url) to <a> tags
    """
    # 1. Escape HTML special characters
    text = html.escape(text)
    
    # 2. Convert markdown bold **text** to <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # 3. Convert markdown italic *text* to <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # 4. Convert markdown inline code `code` to formatted text
    text = re.sub(
        r'`(.*?)`', 
        r'<font face="Courier" color="#C7254E" size="9.5"><b>\1</b></font>', 
        text
    )
    
    # 5. Convert markdown links [text](url) to <a> tags
    text = re.sub(
        r'\[(.*?)\]\((.*?)\)', 
        r'<a href="\2" color="#3182CE"><b>\1</b></a>', 
        text
    )
    
    return text

def highlight_code(escaped_code):
    """
    Applies custom syntax highlighting to python and sql code blocks.
    - Blue for keywords
    - Teal for builtins / SQL commands
    - Orange for strings / True / False
    - Grey-green for comments
    """
    lines = escaped_code.split('\n')
    highlighted_lines = []
    
    keywords = {
        'def', 'class', 'return', 'if', 'else', 'elif', 'for', 'while',
        'in', 'not', 'and', 'or', 'import', 'from', 'global', 'nonlocal',
        'try', 'except', 'pass', 'break', 'continue', 'lambda', 'with', 'as'
    }
    builtins = {
        'print', 'int', 'str', 'float', 'bool', 'list', 'dict', 'len', 'sum', 'range', 'input',
        'connect', 'cursor', 'execute', 'commit', 'fetchone', 'fetchall'
    }
    
    sql_keywords = {
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'CREATE', 'TABLE', 'IF', 'NOT', 'EXISTS',
        'VARCHAR', 'INTEGER', 'DATE', 'DEFAULT', 'SERIAL', 'PRIMARY', 'KEY', 'NULL', 'AND', 'OR'
    }
    
    for line in lines:
        # Detect comment index that is outside string quotes
        comment_start = -1
        in_single_quote = False
        in_double_quote = False
        
        # SQL comments start with --
        sql_comment_start = line.find('--')
        if sql_comment_start != -1:
            comment_start = sql_comment_start
        else:
            for idx, char in enumerate(line):
                if char == "'" and (idx == 0 or line[idx-1] != '\\'):
                    in_single_quote = not in_single_quote
                elif char == '"' and (idx == 0 or line[idx-1] != '\\'):
                    in_double_quote = not in_double_quote
                elif char == '#' and not in_single_quote and not in_double_quote:
                    comment_start = idx
                    break
        
        if comment_start != -1:
            code_part = line[:comment_start]
            comment_part = line[comment_start:]
        else:
            code_part = line
            comment_part = ""
        
        # Replace keywords and builtins in code part
        def replace_keyword(match):
            word = match.group(0)
            if word in keywords:
                return f'<font color="#2B6CB0"><b>{word}</b></font>'
            elif word in builtins:
                return f'<font color="#319795"><b>{word}</b></font>'
            elif word in sql_keywords or word.upper() in sql_keywords:
                return f'<font color="#2B6CB0"><b>{word}</b></font>'
            elif word in {'True', 'False', 'None'}:
                return f'<font color="#DD6B20"><b>{word}</b></font>'
            return word
        
        code_part = re.sub(r'\b\w+\b', replace_keyword, code_part)
        
        if comment_part:
            comment_part = f'<font color="#718096"><i>{comment_part}</i></font>'
            
        highlighted_lines.append(code_part + comment_part)
        
    return '\n'.join(highlighted_lines)

def make_code_block(code_text, code_style):
    """
    Format code block inside a multi-row table with light gray background and border.
    This allows code blocks to split gracefully across pages.
    """
    escaped = html.escape(code_text)
    highlighted = highlight_code(escaped)
    lines = highlighted.split('\n')
    
    # Construct rows containing XPreformatted for each line
    table_data = []
    for line in lines:
        # If the line is empty, put a non-breaking space or space to keep height
        line_content = line if line.strip() else " "
        p = XPreformatted(line_content, code_style)
        table_data.append([p])
        
    t = Table(table_data, colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def append_practice_questions(story, h1_style, h2_style, h3_style, body_style, code_style, bullet_style):
    """
    Appends the user requested practice questions to the PDF story for Week 3.
    """
    story.append(PageBreak())
    story.append(Paragraph("Practice Questions", h1_style))
    story.append(Spacer(1, 10))
    
    # --- PART A ---
    story.append(Paragraph("Part A: File Handling & Pandas", h2_style))
    story.append(Spacer(1, 6))
    
    # Q1
    story.append(Paragraph("Question 1: Word Counter", h3_style))
    story.append(Paragraph("Write a function <b>count_words(filename)</b> that takes a text file's name as input and returns the total number of words in that file.", body_style))
    story.append(make_code_block("Example\nInput:\nfile.txt (containing 'Hello World from Python')\n\nOutput:\n4", code_style))
    story.append(Spacer(1, 10))
    
    # Q2
    story.append(Paragraph("Question 2: Filter Orders by Price", h3_style))
    story.append(Paragraph("Write a python function using Pandas that reads a CSV file <b>orders.csv</b>, fills missing <b>Quantity</b> values with a default value of 1, and filters the rows to keep only orders where the <b>Price</b> is greater than 100. Return the clean, filtered DataFrame.", body_style))
    story.append(make_code_block("Example\nInput:\norders.csv\n\nOutput:\nFiltered DataFrame with non-null quantities and prices > 100", code_style))
    story.append(Spacer(1, 10))
    
    # Q3
    story.append(Paragraph("Question 3: Feature Engineering & De-duplication", h3_style))
    story.append(Paragraph("Write a function that accepts a Pandas DataFrame, creates a new feature column <b>Total_Cost</b> calculated as <b>Quantity * Price</b>, removes any duplicate rows from the DataFrame, and returns the modified DataFrame.", body_style))
    story.append(Spacer(1, 10))
    
    # --- PART B ---
    story.append(Paragraph("Part B: Relational Databases (PostgreSQL & SQLite)", h2_style))
    story.append(Spacer(1, 6))
    
    # Q4
    story.append(Paragraph("Question 4: SQL Table Definition", h3_style))
    story.append(Paragraph("Write a SQL query to create a table named <b>inventory</b>. The table must have: <b>product_id</b> (SERIAL, PRIMARY KEY), <b>name</b> (VARCHAR, NOT NULL), <b>price</b> (NUMERIC, greater than 0), and <b>stock</b> (INTEGER, default 0).", body_style))
    story.append(Spacer(1, 10))
    
    # Q5
    story.append(Paragraph("Question 5: Fetch Users from SQLite Database", h3_style))
    story.append(Paragraph("Write a python function <b>fetch_all_users()</b> that connects to an SQLite database named <b>facebook.db</b>, executes a SELECT statement to retrieve all usernames and email addresses from the <b>users</b> table, and prints each user.", body_style))
    story.append(make_code_block("Example Output:\nAjay ajay@mail.com\nVijay vijay@mail.com", code_style))
    story.append(Spacer(1, 15))
    
    # --- SIMULATION ---
    story.append(Paragraph("Simulation Question", h2_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Problem Statement</b>", h3_style))
    story.append(Paragraph("Design a Python program using SQLite3 to manage a simple Bookstore Inventory.", body_style))
    story.append(Paragraph("Write a function named <b>bookstore()</b> that acts as the main program. Inside <b>bookstore()</b>, define the following nested helper functions:", body_style))
    
    nested_list_style = ParagraphStyle(
        'NestedListStyle',
        parent=bullet_style,
        leftIndent=25,
        bulletIndent=15
    )
    story.append(Paragraph("&bull; <b>add_book(title, author, price)</b> &ndash; Inserts a new book record into a table named <b>books</b>.", nested_list_style))
    story.append(Paragraph("&bull; <b>view_books()</b> &ndash; Fetches and displays all books in the inventory.", nested_list_style))
    story.append(Paragraph("&bull; <b>search_book(title)</b> &ndash; Searches and displays details of a book based on its title.", nested_list_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Database Schema</b>", h3_style))
    story.append(Paragraph("The table <b>books</b> should contain the following fields: <b>title</b> (VARCHAR), <b>author</b> (VARCHAR), and <b>price</b> (FLOAT). Ensure the table is created automatically using a <b>CREATE TABLE IF NOT EXISTS</b> query at startup.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Sample Run</b>", h3_style))
    sample_text = (
        "Input / Operations:\n\n"
        "Welcome to the Bookstore Inventory System\n\n"
        "Select Choice:\n"
        "1) Add Book  2) View Books  3) Search Book  4) Exit\n"
        "Make your choice: 1\n\n"
        "Enter title: Python Basics\n"
        "Enter author: Guido van Rossum\n"
        "Enter price: 450.0\n\n"
        "Book added successfully.\n\n"
        "Make your choice: 2\n\n"
        "--------- BOOKS IN INVENTORY ---------\n"
        "Python Basics - Guido van Rossum - Rs. 450.0\n"
        "--------------------------------------\n"
    )
    story.append(make_code_block(sample_text, code_style))

def generate_pdf(readme_path, output_pdf_path):
    # Setup document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles Setup
    styles = getSampleStyleSheet()
    
    # Styles for Cover Page
    cover_label_style = ParagraphStyle(
        'CoverLabel',
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.white,
        spaceAfter=8
    )
    
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=25,
        leading=30,
        textColor=colors.white
    )
    
    welcome_title_style = ParagraphStyle(
        'WelcomeTitle',
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=12
    )
    
    welcome_body_style = ParagraphStyle(
        'WelcomeBody',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=20
    )
    
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=10
    )
    
    # Styles for Document Content
    h1_style = ParagraphStyle(
        'Heading1Style',
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=22,
        spaceAfter=12,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2Style',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#319795"),
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True
    )
    
    h3_style = ParagraphStyle(
        'Heading3Style',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h4_style = ParagraphStyle(
        'Heading4Style',
        fontName='Helvetica-BoldOblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=3,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=2,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'CodeBlockStyle',
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1A202C")
    )
    
    story = []
    
    # --- 1. COVER PAGE STORY ---
    story.append(Spacer(1, 35))
    story.append(Paragraph("Week Three", cover_label_style))
    story.append(Paragraph("Python Course: File Handling, Data Analysis &amp; Databases Reference Guide", cover_title_style))
    
    # Spacer to push next content down to the white region (below y=420)
    story.append(Spacer(1, 195))
    
    # Content in the white section
    story.append(Paragraph("Welcome to the Python Course!", welcome_title_style))
    story.append(Paragraph(
        "This document compiles the advanced topics learned during the third week. It serves as a "
        "comprehensive study guide, detailing key concepts, syntax, and basic practical examples. All "
        "explanations and code blocks are derived directly from the weekly log repository.",
        welcome_body_style
    ))
    
    story.append(Paragraph("Table of Contents / Topics Covered:", toc_title_style))
    
    # TOC bullet points
    toc_items = [
        "1. File Handling in Python",
        "2. Introduction to Pandas &amp; Data Analysis",
        "3. Data Cleaning &amp; Feature Engineering",
        "4. Introduction to DBMS &amp; PostgreSQL Basics",
        "5. SQLite3 &amp; Authentication Simulation",
        "Practice Questions"
    ]
    for item in toc_items:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
        
    story.append(PageBreak())
    
    # --- 2. PARSE README AND BUILD STORY ---
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    
    i = 0
    level_2_count = 0
    parse_active = False
    
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
            
        # Code block
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            force_closed = False
            while i < len(lines):
                next_line = lines[i]
                # Heuristic: force close if we see a Day heading or horizontal rule
                if next_line.strip().startswith("##") or next_line.strip() == "---":
                    force_closed = True
                    break
                if next_line.strip().startswith("```"):
                    break
                code_lines.append(next_line)
                i += 1
                
            if i < len(lines) and not force_closed:
                i += 1
                
            if parse_active and code_lines:
                code_text = '\n'.join(code_lines)
                story.append(make_code_block(code_text, code_style))
                story.append(Spacer(1, 6))
            continue
            
        # Horizontal Rule
        if line.strip() == "---":
            if parse_active:
                story.append(HRFlowable(
                    width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), 
                    spaceAfter=10, spaceBefore=10
                ))
            i += 1
            continue
            
        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line.strip())
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            
            # Clean emojis and format Day headings
            cleaned_text = clean_heading(text)
            formatted_text = escape_and_format(cleaned_text)
            
            # Skip main README title since we have cover page
            if level == 1 and "Python Course" in text:
                i += 1
                continue
                
            if level == 2:
                # Check if the Day is in Week 3 (Day 12, Day 13, Day 14, Day 15, Day 16)
                if any(f"Day {day}" in text for day in [12, 13, 14, 15, 16]):
                    parse_active = True
                else:
                    parse_active = False
                    
                if parse_active:
                    if level_2_count > 0:
                        story.append(PageBreak())
                    level_2_count += 1
                    story.append(Paragraph(formatted_text, h1_style))
            else:
                if parse_active:
                    if level == 3:
                        story.append(Paragraph(formatted_text, h2_style))
                    elif level == 4:
                        story.append(Paragraph(formatted_text, h3_style))
                    else:
                        story.append(Paragraph(formatted_text, h4_style))
                
            i += 1
            continue
            
        # Bullet lists and ordered lists
        bullet_match = re.match(r'^(\s*)([-\*]|\d+\.)\s+(.*)$', line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            marker = bullet_match.group(2)
            text = bullet_match.group(3)
            
            left_indent = 15
            if indent > 0:
                left_indent = 30 # sub-bullet
                
            # Collect multiline bullet item if any
            while i + 1 < len(lines) and lines[i+1].strip() and \
                  not re.match(r'^(\s*)([-\*]|\d+\.)\s+(.*)$', lines[i+1]) and \
                  not lines[i+1].strip().startswith("```") and \
                  not re.match(r'^(#{1,6})\s+(.*)$', lines[i+1].strip()) and \
                  lines[i+1].strip() != "---":
                text += " " + lines[i+1].strip()
                i += 1
                
            if parse_active:
                formatted_text = escape_and_format(text)
                
                item_style = ParagraphStyle(
                    f'BulletItem_{left_indent}',
                    parent=bullet_style,
                    leftIndent=left_indent,
                    bulletIndent=left_indent - 10
                )
                
                bullet_char = "&bull;" if marker in ['-', '*'] else marker
                story.append(Paragraph(f"{bullet_char} {formatted_text}", item_style))
            i += 1
            continue
            
        # Regular text paragraph
        paragraph_text = line.strip()
        i += 1
        # Group consecutive non-empty lines that aren't other elements
        while i < len(lines) and lines[i].strip() and \
              not re.match(r'^(#{1,6})\s+(.*)$', lines[i].strip()) and \
              not lines[i].strip().startswith("```") and \
              not re.match(r'^(\s*)([-\*]|\d+\.)\s+(.*)$', lines[i]) and \
              lines[i].strip() != "---":
            paragraph_text += " " + lines[i].strip()
            i += 1
            
        if parse_active:
            formatted_text = escape_and_format(paragraph_text)
            story.append(Paragraph(formatted_text, body_style))
            story.append(Spacer(1, 4))

    # --- 3. APPEND PRACTICE QUESTIONS ---
    append_practice_questions(story, h1_style, h2_style, h3_style, body_style, code_style, bullet_style)
        
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_pdf_path}")

if __name__ == "__main__":
    readme = "README.md"
    output_pdf = os.path.join("week_03", "Week_three.pdf")
    generate_pdf(readme, output_pdf)
