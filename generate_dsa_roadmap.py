import os
import re
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, XPreformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to add running headers and footers with a dynamic page count.
    Suppress headers and footers on the cover page (Page 1).
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
        # Page 1: Cover Page
        if self._pageNumber == 1:
            self.saveState()
            # Top block background decoration (Dark Slate/Navy)
            self.setFillColor(colors.HexColor("#1A365D"))
            self.rect(0, 420, 612, 792 - 420, fill=True, stroke=False)
            
            # Gold Accent Strip
            self.setFillColor(colors.HexColor("#D69E2E"))
            self.rect(0, 400, 612, 20, fill=True, stroke=False)
            
            # Sub-accent Circle
            self.setFillColor(colors.HexColor("#2B6CB0"))
            self.circle(550, 700, 120, fill=True, stroke=False)
            
            self.restoreState()
            return

        # Subsequent Pages
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Running Header
        self.drawString(54, 750, "DSA & COMPETITIVE PROGRAMMING SPECIALIST ROADMAP")
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "Complete Career & Algorithmic Guide")
        
        # Header Line Separator
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Running Footer
        self.drawString(54, 40, "Confidential — Algorithmic Learning Curriculum")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 40, page_text)
        
        # Footer Line Separator
        self.line(54, 52, 612 - 54, 52)
        self.restoreState()

def escape_and_format(text):
    """
    Escapes raw XML entities (like ampersands) and parses inline markdown:
    - & to &amp; (only if not already an entity)
    - **bold** to <b>bold</b>
    - *italic* to <i>italic</i>
    - `code` to courier font
    """
    text = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(
        r'`(.*?)`', 
        r'<font face="Courier" color="#2B6CB0" size="8.5"><b>\1</b></font>', 
        text
    )
    return text

def create_callout_box(text, level, styles):
    """
    Creates a styled callout box table with a thick left border.
    level can be 'MUST', 'SHOULD', or 'ADVANCED'
    """
    body_style = styles['BodyStyle']
    
    if level == 'MUST':
        border_color = colors.HexColor("#E53E3E")
        bg_color = colors.HexColor("#FFF5F5")
        label = "<b><font color=\"#E53E3E\">[MUST KNOW]</font></b> "
    elif level == 'SHOULD':
        border_color = colors.HexColor("#DD6B20")
        bg_color = colors.HexColor("#FFFAF0")
        label = "<b><font color=\"#DD6B20\">[SHOULD KNOW]</font></b> "
    else:
        border_color = colors.HexColor("#319795")
        bg_color = colors.HexColor("#E6FFFA")
        label = "<b><font color=\"#319795\">[ADVANCED]</font></b> "

    p = Paragraph(label + escape_and_format(text), body_style)
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('LINELEFT', (0,0), (0,-1), 4, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def make_code_block(code_text, code_style):
    """
    Formats a python/code block with a light gray background.
    """
    escaped = html.escape(code_text)
    p = XPreformatted(escaped, code_style)
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def build_pdf(filename="DSA_Competitive_Programming_Roadmap.pdf"):
    # Setup document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles definitions
    cover_label_style = ParagraphStyle(
        'CoverLabel',
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=colors.white,
        spaceAfter=10
    )
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white,
        spaceAfter=8
    )
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#D69E2E"),
        spaceAfter=25
    )
    welcome_title_style = ParagraphStyle(
        'WelcomeTitle',
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=20,
        spaceAfter=12
    )
    welcome_body_style = ParagraphStyle(
        'WelcomeBody',
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'Heading1Style',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2Style',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15.5,
        textColor=colors.HexColor("#319795"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3Style',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=3,
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceBefore=2,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeBlockStyle',
        fontName='Courier',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )
    th_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2D3748")
    )
    
    # Register styles in default stylesheet to resolve references in callouts
    styles.add(cover_label_style)
    styles.add(cover_title_style)
    styles.add(cover_subtitle_style)
    styles.add(welcome_title_style)
    styles.add(welcome_body_style)
    styles.add(h1_style)
    styles.add(h2_style)
    styles.add(h3_style)
    styles.add(body_style)
    styles.add(bullet_style)
    styles.add(code_style)
    styles.add(th_style)
    styles.add(td_style)
    
    story = []
    
    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("TECHNICAL EDUCATION CURRICULUM", cover_label_style))
    story.append(Paragraph("DSA &amp; Competitive Programming Specialist", cover_title_style))
    story.append(Paragraph("Complete Learning &amp; Career Roadmap", cover_subtitle_style))
    
    story.append(Spacer(1, 230))
    story.append(Paragraph("Welcome to the Algorithmic &amp; DSA Curriculum", welcome_title_style))
    story.append(Paragraph(
        "This roadmap is designed to take software engineers and competitive programmers from "
        "basic coding language syntax to advanced algorithmic problem solving. The content is structured "
        "hierarchically to guarantee step-by-step progress. It covers programming fundamentals, "
        "classic data structures, complex optimization strategies (Dynamic Programming, Greedy), "
        "advanced range-query trees, and competitive programming invariants. It is suitable "
        "for preparing for product companies, LeetCode, Codeforces, and Google/Meta style interviews.",
        welcome_body_style
    ))
    
    story.append(Paragraph("<b>Table of Stages / Content Map:</b>", h3_style))
    stages = [
        "Stage 0 — Programming Fundamentals &amp; Complexity Analysis",
        "Stage 1 — Arrays &amp; Strings (Traversals, Two Pointers, Sliding Window)",
        "Stage 2 — Linked Lists (Singly, Doubly, Circular, Cycles)",
        "Stage 3 — Stack &amp; Queue (Deques, Monotonic structures, Range Maximums)",
        "Stage 4 — Hashing &amp; Sets (Frequency maps, Collisions)",
        "Stage 5 — Recursion &amp; Backtracking (Permutations, N-Queens, Sudoku)",
        "Stage 6 — Binary Trees (Traversals, BFS, DFS, Ancestors, Serializers)",
        "Stage 7 — Binary Search Trees (Properties, Operations, Balancing)",
        "Stage 8 — Heaps &amp; Priority Queues (Median of Stream, Top K)",
        "Stage 9 — Graphs (BFS, DFS, Cycles, Topological Sorts)",
        "Stage 10 — Shortest Paths (Dijkstra, Bellman-Ford, Floyd-Warshall)",
        "Stage 11 — Minimum Spanning Trees &amp; Disjoint Set Union (DSU)",
        "Stage 12 — Dynamic Programming (Memoization, Tabulation, 18 Patterns)",
        "Stage 13 — Greedy Algorithms (Scheduling, Exchange arguments)",
        "Stage 14 — Advanced Data Structures &amp; Algorithms (Segment Trees, Trie, KMP)",
        "Stage 15 — Bit Manipulation (AND/OR/XOR operations, Masks)",
        "Stage 16 — Mathematical Algorithms (Modular inverse, Sieve, Exponentiation)",
        "Stage 17 — Competitive Programming Techniques (Coordinate compression, Sweep-line)",
        "Stage 18 — 18 Problem-Solving Pattern Templates",
        "Stage 19 — Practice Roadmap (Level 1 to Level 5 Problem Sheets)",
        "Stage 20 — Dedicated Interview Preparation Tracks"
    ]
    for s in stages:
        story.append(Paragraph(f"&bull; {s}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 0 ------------------
    story.append(Paragraph("Stage 0 — Programming Fundamentals &amp; Complexity", h1_style))
    story.append(Paragraph(
        "Master the fundamentals of your chosen language (Python for implementation templates) "
        "and learn the asymptotic notation needed to evaluate algorithm efficiency.", body_style
    ))
    
    stage0_topics = [
        ("Language Syntax Basics", "MUST", "Variables, basic data types (integers, floats, strings, booleans), standard input/output, conditional logic (if-elif-else), loops (for, while), and functions."),
        ("Recursion Fundamentals", "MUST", "A function calling itself to break down problems. Focus on base cases, state transitions, recursion stack frames, and preventing stack overflows."),
        ("Object-Oriented Programming (OOP)", "SHOULD", "Classes, object instantiations, attribute state, and constructor methods. Crucial for custom tree/graph node designs."),
        ("Python Built-Ins & Collections", "MUST", "Operations on lists, sets, and dictionaries. Master methods like list appending/slicing, set hashing/lookups, and dictionary get/default values."),
        ("Iterators & Lambdas", "SHOULD", "Generating ranges, traversing custom collections using iterators, and using anonymous functions (lambdas) for custom sorting keys."),
        ("Basic Exception Handling", "MUST", "Using try-except blocks to catch division errors, key errors, and index out of bounds to write resilient code."),
        ("Sorting", "MUST", "Standard sorting operations, custom key sorting, comparator functions, and understanding Python's Timsort complexity (O(N log N)).")
    ]
    for name, level, desc in stage0_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Asymptotic Complexity Analysis", h2_style))
    story.append(Paragraph(
        "Evaluate algorithm runtime and memory usage using asymptotic bounds. "
        "Avoid raw operations counting; focus on bounding scaling limits.", body_style
    ))
    
    complexity_bounds = [
        ("Big-O Notation (O)", "MUST", "Represents the asymptotic upper bound of growth. Used to analyze worst-case behavior."),
        ("Big-Theta (Theta)", "SHOULD", "Represents the tight asymptotic bound. Growth is bounded both above and below."),
        ("Big-Omega (Omega)", "SHOULD", "Represents the asymptotic lower bound. Used to analyze best-case execution bounds.")
    ]
    for name, level, desc in complexity_bounds:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Common Complexity Patterns Reference Table", h2_style))
    
    complexity_table_data = [
        [Paragraph("<b>Time Complexity</b>", th_style), Paragraph("<b>Operation Scaling Type</b>", th_style), Paragraph("<b>Common Algorithmic Pattern Examples</b>", th_style)],
        [Paragraph("O(1)", td_style), Paragraph("Constant", td_style), Paragraph("Hash table lookups, array indexing, mathematical formulas, push/pop in stack.", td_style)],
        [Paragraph("O(log N)", td_style), Paragraph("Logarithmic", td_style), Paragraph("Binary search, heap operations, modular exponentiation.", td_style)],
        [Paragraph("O(N)", td_style), Paragraph("Linear", td_style), Paragraph("Single loop traversals, linear search, prefix sums, queue operations.", td_style)],
        [Paragraph("O(N log N)", td_style), Paragraph("Linearithmic", td_style), Paragraph("Merge sort, quicksort, heap sort, coordinate compression.", td_style)],
        [Paragraph("O(N²)", td_style), Paragraph("Quadratic", td_style), Paragraph("Nested loops, bubble sort, brute force pairs search, 2D grid DP.", td_style)],
        [Paragraph("O(2^N)", td_style), Paragraph("Exponential", td_style), Paragraph("Generating all subsets of size N, recursive Fibonacci, backtracking combinations.", td_style)],
        [Paragraph("O(N!)", td_style), Paragraph("Factorial", td_style), Paragraph("Generating all permutations of an array, traveling salesperson TSP brute force.", td_style)]
    ]
    t_comp = Table(complexity_table_data, colWidths=[100, 140, 264])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_comp)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 1 ------------------
    story.append(Paragraph("Stage 1 — Arrays &amp; Strings", h1_style))
    story.append(Paragraph("Linear structures stored contiguously. Master traversal patterns and sliding window limits.", body_style))
    
    stage1_topics = [
        ("Contiguous Traversals", "MUST", "Traversing arrays from left-to-right, right-to-left, or outer-to-inner. Core for basic indexing."),
        ("Two Pointers Technique", "MUST", "Iterating using two index variables moving toward each other or moving at different speeds. Reduces O(N^2) scans to O(N)."),
        ("Sliding Window (Fixed/Variable)", "MUST", "Maintaining a subarray window that expands or contracts based on constraints. Focus on window resizing triggers."),
        ("Prefix Sums & Difference Arrays", "MUST", "Prefix Sum: precomputes cumulative sum for O(1) range queries. Difference Array: stores step differences to perform O(1) range updates."),
        ("Frequency counting & Hashing", "MUST", "Storing character/element occurrence counts inside a hash map or array to solve anagrams or duplicate check queries."),
        ("Sorting-Based Techniques", "MUST", "Sorting inputs first to allow binary search, target pairs scanning, or interval merging."),
        ("Subarrays vs. Subsequences", "MUST", "Subarray: contiguous slice of an array. Subsequence: elements in their original relative order but not necessarily contiguous.")
    ]
    for name, level, desc in stage1_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Representative Problems", h2_style))
    rep_problems_s1 = [
        "Two Pointers: Target Sum (LeetCode 167 - Two Sum II - Input Array Is Sorted)",
        "Sliding Window: Longest Substring Without Repeating Characters (LeetCode 3)",
        "Prefix Sum: Range Sum Query (LeetCode 303 - Range Sum Query - Immutable)",
        "Difference Array: Range Addition (LeetCode 370)",
        "Frequency Map: Valid Anagram (LeetCode 242)"
    ]
    for prob in rep_problems_s1:
        story.append(Paragraph(f"&bull; {prob}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 2 ------------------
    story.append(Paragraph("Stage 2 — Linked Lists", h1_style))
    story.append(Paragraph("Dynamic node chains linked via memory pointers. Master pointer manipulations and node linkages.", body_style))
    
    stage2_topics = [
        ("Singly Linked Lists", "MUST", "Nodes containing data and a 'next' pointer. Master basic node insertion and deletion."),
        ("Doubly Linked Lists", "MUST", "Nodes containing 'next' and 'prev' pointers, allowing bidirectional traversals. Crucial for LRU cache implementations."),
        ("Circular Linked Lists", "SHOULD", "Tail node points back to the head node. Used in round-robin scheduling algorithms."),
        ("Fast & Slow Pointers", "MUST", "Two pointers traversal at rates of 2x and 1x. Used to find list midpoints and detect cycles."),
        ("Linked List Reversal", "MUST", "Reversing link directions iteratively or recursively using pointer swapping."),
        ("Cycle Detection & Floyd's Algorithm", "MUST", "Fast and slow pointers collide in a cycle loop. Locate the loop starting node using Floyd's Tortoise and Hare."),
        ("Merging & Intersecting lists", "MUST", "Merging two sorted lists (O(N)); identifying list intersection nodes using length diffs or dual pointers.")
    ]
    for name, level, desc in stage2_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 3 ------------------
    story.append(Paragraph("Stage 3 — Stack &amp; Queue", h1_style))
    story.append(Paragraph("Linear containers following strict insertion and retrieval access bounds.", body_style))
    
    stage3_topics = [
        ("Stack (LIFO)", "MUST", "Last In, First Out. Standard operations (push, pop, peek). Master recursion simulation and undo operations."),
        ("Queue (FIFO) & Deque", "MUST", "First In, First Out. Deque (Double Ended Queue): supports push/pop at both ends. Essential for BFS tree/graph traversals."),
        ("Monotonic Stack", "MUST", "Stack that maintains elements in strict increasing/decreasing order. Used for O(N) next-greater-element checks."),
        ("Monotonic Queue", "MUST", "Queue maintaining elements in sorted order. Used to track range maximums inside sliding windows."),
        ("Expression Evaluation", "SHOULD", "Evaluating infix, prefix, and postfix notations. Master the Shunting-Yard algorithm for parsing operators.")
    ]
    for name, level, desc in stage3_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Representative Problems", h2_style))
    rep_problems_s3 = [
        "Monotonic Stack: Next Greater Element (LeetCode 496), Largest Rectangle in Histogram (LeetCode 84)",
        "Monotonic Queue: Sliding Window Maximum (LeetCode 239)",
        "Parentheses parsing: Valid Parentheses (LeetCode 20), Min Add to Make Valid (LeetCode 921)"
    ]
    for prob in rep_problems_s3:
        story.append(Paragraph(f"&bull; {prob}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 4 ------------------
    story.append(Paragraph("Stage 4 — Hashing", h1_style))
    story.append(Paragraph("Using hash functions to map arbitrary-sized data inputs to fixed-size buckets for fast lookups.", body_style))
    
    stage4_topics = [
        ("Hash Table & Set", "MUST", "Containers providing O(1) average lookup, insert, and delete. Sets store keys; maps store key-value pairs."),
        ("Collision Intuition", "SHOULD", "Understanding how keys map to the same bucket. Master Chaining (linked list buckets) and Open Addressing (linear/quadratic probing)."),
        ("Frequency Maps", "MUST", "Tracking element counts to locate duplicates, find majority elements, and scan target occurrences.")
    ]
    for name, level, desc in stage4_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Classic Hashing Problems", h2_style))
    rep_problems_s4 = [
        "Two Sum (LeetCode 1) - standard frequency map lookup",
        "Subarray Sum Equals K (LeetCode 560) - prefix sum + frequency map pattern",
        "Longest Consecutive Sequence (LeetCode 128) - hash set lookup"
    ]
    for prob in rep_problems_s4:
        story.append(Paragraph(f"&bull; {prob}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 5 ------------------
    story.append(Paragraph("Stage 5 — Recursion &amp; Backtracking", h1_style))
    story.append(Paragraph("Systematic search of space options by constructing path states and backtracking on dead-ends.", body_style))
    
    stage5_topics = [
        ("Recursion Trees", "MUST", "Visualizing execution branches. Each tree node represents a recursive call; tree depth determines space complexity."),
        ("Backtracking Paradigm", "MUST", "Constructing search paths step-by-step. If a path violates problem constraints, back up and try the next branch."),
        ("Permutations & Combinations", "MUST", "Generating permutations (ordering matters, size N!) and combinations/subsets (order ignores, size 2^N)."),
        ("Constraint Satisfaction Search", "SHOULD", "Placing elements on boards under strict limits. Classic problems: N-Queens, Sudoku solver.")
    ]
    for name, level, desc in stage5_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("How to Identify Backtracking Problems", h2_style))
    story.append(Paragraph(
        "A problem requires backtracking when: "
        "1) The output demands listing ALL possible combinations, permutations, or configurations. "
        "2) The solution bounds scale exponentially (e.g., N &le; 15, indicating O(2^N) or O(N!) is expected). "
        "3) Decisions must be validated step-by-step with rollback capabilities.", body_style
    ))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 6 ------------------
    story.append(Paragraph("Stage 6 — Binary Trees", h1_style))
    story.append(Paragraph("Hierarchical structures where each node has at most two child pointers. Master tree traversals.", body_style))
    
    stage6_topics = [
        ("Tree traversals (DFS)", "MUST", "Depth-First Search. Traversing trees recursively: Preorder (Root-L-R), Inorder (L-Root-R), and Postorder (L-R-Root)."),
        ("Tree traversals (BFS)", "MUST", "Breadth-First Search. Traversal level-by-level using a Queue. Standard pattern for level-order printing."),
        ("Height & Depth", "MUST", "Height: max path length from node to leaf. Depth: path length from root to node. Calculated recursively."),
        ("Diameter of Binary Tree", "MUST", "Longest path between any two leaf nodes in the tree. May or may not pass through the root node."),
        ("Lowest Common Ancestor (LCA)", "MUST", "The deepest node that is an ancestor to two target nodes. Essential recursive traversal check."),
        ("Tree Serialization", "SHOULD", "Converting binary tree structure to a flat string representation (e.g., string list with '#' for nulls) and rebuilding it.")
    ]
    for name, level, desc in stage6_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 7 ------------------
    story.append(Paragraph("Stage 7 — Binary Search Trees (BST)", h1_style))
    story.append(Paragraph("A binary tree where left child values are less than root, and right child values are greater.", body_style))
    
    stage7_topics = [
        ("BST Properties", "MUST", "Left subtree values &lt; node value &lt; right subtree values. Crucial point: Inorder traversal outputs sorted values."),
        ("BST Operations", "MUST", "Search, Insert, and Delete. Delete requires handling three cases: leaf node, one-child node, and two-children node."),
        ("BST Validation", "MUST", "Validating if a binary tree is a valid BST. Do not check local parent-child relations only; maintain range limits [min, max] recursively."),
        ("Kth Smallest/Largest", "MUST", "Locating the Kth sorted element. Perform Inorder traversal to count items, or track subtree sizes if dynamic.")
    ]
    for name, level, desc in stage7_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 8 ------------------
    story.append(Paragraph("Stage 8 — Heaps &amp; Priority Queues", h1_style))
    story.append(Paragraph("Complete binary trees that satisfy the heap property, providing fast access to maximum/minimum elements.", body_style))
    
    stage8_topics = [
        ("Heap Structure & Heapify", "MUST", "Min Heap (parent &le; children) and Max Heap (parent &ge; children). Heapify: O(N) array-to-heap conversion. Push/Pop run in O(log N)."),
        ("Priority Queues", "MUST", "Abstract data structure providing fast min/max retrievals. Implemented natively in Python via `heapq`."),
        ("Top K Elements Problems", "MUST", "Extracting K largest/smallest elements. Use a size-K min heap to track top values in O(N log K) time."),
        ("Median of Stream", "SHOULD", "Tracking median dynamically in a continuous stream of numbers. Implement using two heaps: a max-heap for the lower half and a min-heap for the upper half.")
    ]
    for name, level, desc in stage8_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 9 ------------------
    story.append(Paragraph("Stage 9 — Graphs", h1_style))
    story.append(Paragraph("Sets of vertices connected by edges. Master graph representations and traversals.", body_style))
    
    stage9_topics = [
        ("Graph Representation", "MUST", "Adjacency Matrix: O(V^2) grid (good for dense graphs). Adjacency List: list of edge arrays (best for sparse graphs, uses O(V+E) memory)."),
        ("Graph DFS & BFS", "MUST", "BFS: level-order scan using Queue. DFS: recursive depth exploration using Call Stack. Must track visited vertices to prevent infinite loops."),
        ("Cycle Detection", "MUST", "Undirected: check if visited neighbor is not parent. Directed: track recursion stack state (detect back edges)."),
        ("Topological Sorting", "MUST", "Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for edge u-v, u comes before v. Use Kahn's BFS (indegree counting) or DFS."),
        ("Bipartite Graphs", "SHOULD", "Check if graph vertices can be colored using two colors such that no adjacent vertices share a color. Test using BFS/DFS coloring.")
    ]
    for name, level, desc in stage9_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 10 ------------------
    story.append(Paragraph("Stage 10 — Shortest Path Algorithms", h1_style))
    story.append(Paragraph("Algorithmic frameworks designed to locate paths of minimal weights between vertices.", body_style))
    story.append(Spacer(1, 10))
    
    # Dijkstra
    story.append(Paragraph("1. Dijkstra's Algorithm", h2_style))
    dij_desc = (
        "<b>Intuition:</b> Greedy search that expands the shortest known paths from a source node.<br/>"
        "<b>Algorithm:</b> Maintains distances array. Uses Min-Priority Queue to extract unvisited node with minimum distance, relaxes neighbors, and repeats.<br/>"
        "<b>Time Complexity:</b> O((V + E) log V).<br/>"
        "<b>Space Complexity:</b> O(V + E) (to store graph and priority queue).<br/>"
        "<b>When to use:</b> Single-source shortest paths on graphs with non-negative edge weights.<br/>"
        "<b>When NOT to use:</b> Graphs containing negative edge weights (fails to converge)."
    )
    story.append(create_callout_box(dij_desc, "MUST", styles))
    story.append(Spacer(1, 8))
    
    # Bellman-Ford
    story.append(Paragraph("2. Bellman-Ford Algorithm", h2_style))
    bf_desc = (
        "<b>Intuition:</b> Dynamic programming approach that relaxes all edges V-1 times.<br/>"
        "<b>Algorithm:</b> Loops V-1 times; in each iteration, loops over all edges to update min distance. A V-th iteration detects negative cycles.<br/>"
        "<b>Time Complexity:</b> O(V * E).<br/>"
        "<b>Space Complexity:</b> O(V).<br/>"
        "<b>When to use:</b> Single-source shortest paths with negative weights, or when negative cycle detection is required.<br/>"
        "<b>When NOT to use:</b> Large graphs where O(V * E) is computationally prohibitive."
    )
    story.append(create_callout_box(bf_desc, "SHOULD", styles))
    story.append(Spacer(1, 8))
    
    # Floyd-Warshall
    story.append(Paragraph("3. Floyd-Warshall Algorithm", h2_style))
    fw_desc = (
        "<b>Intuition:</b> Compares path transitions via an intermediate vertex k.<br/>"
        "<b>Algorithm:</b> 3-nested loops: for each intermediate k, check if path u-v can be shortened via k: grid[i][j] = min(grid[i][j], grid[i][k] + grid[k][j]).<br/>"
        "<b>Time Complexity:</b> O(V³).<br/>"
        "<b>Space Complexity:</b> O(V²).<br/>"
        "<b>When to use:</b> All-pairs shortest paths on small graphs (V &le; 400).<br/>"
        "<b>When NOT to use:</b> Large graphs where cubic time is too slow."
    )
    story.append(create_callout_box(fw_desc, "SHOULD", styles))
    story.append(Spacer(1, 8))
    
    # 0-1 BFS
    story.append(Paragraph("4. 0-1 BFS Algorithm", h2_style))
    bfs_desc = (
        "<b>Intuition:</b> Shortest path on graphs with edge weights restricted to 0 and 1.<br/>"
        "<b>Algorithm:</b> Deque traversal. If weight is 0, append to front; if 1, append to back. Always extracts minimum distance first.<br/>"
        "<b>Time Complexity:</b> O(V + E).<br/>"
        "<b>Space Complexity:</b> O(V).<br/>"
        "<b>When to use:</b> Shortest paths where edge transitions have binary cost (0 or 1).<br/>"
        "<b>When NOT to use:</b> Graphs with fractional or arbitrary edge weights."
    )
    story.append(create_callout_box(bfs_desc, "MUST", styles))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 11 ------------------
    story.append(Paragraph("Stage 11 — Minimum Spanning Tree (MST) &amp; DSU", h1_style))
    story.append(Paragraph("Connecting all vertices in a graph with the minimum possible total edge weight without cycles.", body_style))
    
    stage11_topics = [
        ("Prim's Algorithm", "MUST", "Greedy node-centric algorithm. Starts with a node and repeatedly appends the cheapest edge that connects a node in the tree to a node outside it. Uses Min Heap."),
        ("Kruskal's Algorithm", "MUST", "Greedy edge-centric algorithm. Sorts all edges by weight, and repeatedly adds the cheapest edge if it doesn't create a cycle. Cycles are checked using DSU."),
        ("Disjoint Set Union (DSU)", "MUST", "Data structure representing partition elements. Standard operations: Find (returns root) and Union (joins sets)."),
        ("Union-Find Optimizations", "MUST", "Path Compression (flattens tree structure to O(1) during find operations) and Union by Rank/Size (attaches smaller trees to larger ones, keeping depth low).")
    ]
    for name, level, desc in stage11_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 12 ------------------
    story.append(Paragraph("Stage 12 — Dynamic Programming (DP) Roadmap", h1_style))
    story.append(Paragraph(
        "DP optimizes recursion by saving solutions to overlapping subproblems "
        "rather than recalculating them.", body_style
    ))
    
    dp_basics = [
        ("DP Core Concept", "MUST", "Applicable when a problem displays: 1) Overlapping Subproblems (subproblems recalculate repeatedly), 2) Optimal Substructure (global optimal uses local subproblem optimals)."),
        ("Memoization vs. Tabulation", "MUST", "Memoization: Top-down recursion caching. Tabulation: Bottom-up iterative table resolution. Tabulation is generally faster but memoization is easier to write."),
        ("State & Transition", "MUST", "State: Variables describing subproblem inputs. Transition: Formula connecting the current state to sub-states (e.g., dp[i] = dp[i-1] + dp[i-2])."),
        ("Space Optimization", "SHOULD", "Reducing storage from O(N) or O(N^2) to O(1) or O(W) by keeping only the last few rows/elements needed for transitions.")
    ]
    for name, level, desc in dp_basics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("18 Key DP Patterns &amp; Recognition Strategies", h2_style))
    
    dp_patterns = [
        ("1D DP (Linear State)", "MUST", "State is a single parameter representing array index. Transition uses previous indices (e.g., Climbing Stairs)."),
        ("2D DP / Grid DP", "MUST", "State is index coordinates (i, j) on a grid. Transitions allow moving down/right (e.g., Unique Paths)."),
        ("0/1 Knapsack", "MUST", "State represents choice of item i and remaining weight w. Transition: include item vs. exclude item."),
        ("Unbounded Knapsack", "MUST", "Same as 0/1, but items can be selected infinitely. Transition updates weight but keeps index constant."),
        ("Subsequence DP / LIS", "MUST", "Longest Increasing Subsequence. State tracks indices i and j. Transition: dp[i] = max(dp[j] + 1) for all j &lt; i where arr[j] &lt; arr[i]."),
        ("String DP / LCS", "MUST", "Longest Common Subsequence. State tracks string lengths (i, j). Transition: match (1 + dp[i-1][j-1]) vs. mismatch (max(dp[i-1][j], dp[i][j-1]))."),
        ("Interval DP", "SHOULD", "State represents range boundaries [left, right]. Solve sub-intervals first (e.g., Matrix Chain Multiplication)."),
        ("Partition DP", "SHOULD", "Partitioning array into K subsegments to minimize/maximize costs. Transition loops over possible partition cuts."),
        ("Tree DP", "ADVANCED", "Performing DP on tree nodes. State represents node selection (e.g., selected vs. not selected in House Robber III)."),
        ("Bitmask DP", "ADVANCED", "State uses an integer mask (binary representation) to track visited sub-states (e.g., Traveling Salesperson TSP)."),
        ("Digit DP", "ADVANCED", "Counting count digits satisfying a property in a range [L, R]. State tracks index, digit limit, and condition constraints.")
    ]
    for name, level, desc in dp_patterns:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 13 ------------------
    story.append(Paragraph("Stage 13 — Greedy Algorithms", h1_style))
    story.append(Paragraph("Making locally optimal choices at each step, hoping it leads to a global optimum.", body_style))
    
    stage13_topics = [
        ("Greedy Intuition", "MUST", "Choose the best local choice without looking back. Works only if local choices never rule out global optimals."),
        ("Exchange Argument", "SHOULD", "Mathematical proof strategy to prove greedy correctness: assume another optimal ordering exists, swap elements, and show target cost doesn't decay."),
        ("Activity Selection / Interval Scheduling", "MUST", "Given tasks with start/end times, select maximum tasks. Greedy strategy: sort by finish times, pick earliest finishing tasks first."),
        ("Fractional Knapsack", "MUST", "Items can be split. Greedy strategy: sort by value/weight ratio, select highest ratios first."),
        ("Huffman Coding", "SHOULD", "Greedy data compression. Build a tree by repeatedly combining the two least-frequent character nodes.")
    ]
    for name, level, desc in stage13_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 14 ------------------
    story.append(Paragraph("Stage 14 — Advanced Algorithms", h1_style))
    story.append(Paragraph("Advanced data structures for range queries, prefix matching, and string patterns.", body_style))
    
    stage14_topics = [
        ("Trie (Prefix Tree)", "MUST", "Node tree storing characters. Used to lookup word prefixes and perform search auto-completes in O(Length) time."),
        ("Segment Tree", "ADVANCED", "Balanced binary tree representing range intervals. Perform range queries (Sum/Min/Max) and point updates in O(log N) time."),
        ("Fenwick Tree (BIT)", "ADVANCED", "Binary Indexed Tree. Much faster and easier to code than Segment Trees; supports range sum queries and updates in O(log N)."),
        ("Lazy Propagation", "ADVANCED", "Deferring updates inside Segment Trees by buffering additions at parent nodes, reducing range update complexity from O(N) to O(log N)."),
        ("String Matching: KMP Algorithm", "ADVANCED", "Knuth-Morris-Pratt. Avoids resetting scanning pointers using a prefix table (LPS array), finding string matches in O(N+M) time."),
        ("String Hashing & Rabin-Karp", "SHOULD", "Calculates sliding hash values (Rolling Hash) to find pattern matches in linear time.")
    ]
    for name, level, desc in stage14_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 15 ------------------
    story.append(Paragraph("Stage 15 — Bit Manipulation", h1_style))
    story.append(Paragraph("Bitwise operations on integers, maximizing execution speed.", body_style))
    
    stage15_topics = [
        ("Bitwise Operators", "MUST", "AND (&amp;), OR (|), XOR (^), NOT (~), and shifts (&lt;&lt;, &gt;&gt;)."),
        ("Basic Bit Operations", "MUST", "Set bit: `x | (1 &lt;&lt; i)`. Unset bit: `x &amp; ~(1 &lt;&lt; i)`. Toggle bit: `x ^ (1 &lt;&lt; i)`. Check bit: `(x &gt;&gt; i) &amp; 1`."),
        ("Power of Two & Count Bits", "MUST", "Power of Two: `x &amp; (x - 1) == 0`. Kernighan's algorithm count set bits: repeatedly clear lowest set bit `x &amp;= x-1`."),
        ("XOR Tricks", "MUST", "Properties: `x ^ x = 0`, `x ^ 0 = x`. Used to find non-duplicate elements in pairs arrays (LeetCode 136).")
    ]
    for name, level, desc in stage15_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 16 ------------------
    story.append(Paragraph("Stage 16 — Mathematical Algorithms", h1_style))
    story.append(Paragraph("Number theory and combinatorics necessary for competitive programming limits.", body_style))
    
    stage16_topics = [
        ("Greatest Common Divisor (GCD)", "MUST", "Euclidean algorithm: `gcd(a, b) = gcd(b, a % b)`. Runs in O(log(min(a, b))) time."),
        ("Prime Numbers & Sieve", "MUST", "Sieve of Eratosthenes: precomputes prime flags up to N in O(N log(log N)) time. Prime checks up to sqrt(N)."),
        ("Modular Arithmetic & Exponentiation", "MUST", "Modular addition, subtraction, multiplication. Binary Exponentiation: calculates `a^b % mod` in O(log b) time."),
        ("Modular Multiplicative Inverse", "SHOULD", "Finding `x` such that `(a * x) % mod == 1`. Uses Fermat's Little Theorem if mod is prime: `a^(mod-2) % mod`."),
        ("Combinatorics (nCr)", "SHOULD", "Calculating combinations. Precompute factorials and modular inverses to query `nCr % mod` in O(1) time.")
    ]
    for name, level, desc in stage16_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 17 ------------------
    story.append(Paragraph("Stage 17 — Competitive Programming Techniques", h1_style))
    story.append(Paragraph("Optimization patterns focused on beating testing limits and handling massive queries.", body_style))
    
    stage17_topics = [
        ("Coordinate Compression", "SHOULD", "Mapping large, sparse coordinates values (e.g. up to 10^9) to index values from 0 to N-1 while preserving relative order."),
        ("Sweep Line Paradigm", "SHOULD", "Iterating over events sorted by coordinates (e.g. interval merges, intersection queries). Tracks active state dynamically."),
        ("Meet in the Middle", "ADVANCED", "Split dataset of size N into two halves of size N/2, search both halves independently, and merge outputs (reduces O(2^N) to O(2^(N/2)))."),
        ("Binary Search on Answer", "MUST", "Applying binary search on the output value space [min_val, max_val] instead of array indices, using a greedy helper to test validity.")
    ]
    for name, level, desc in stage17_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 18 ------------------
    story.append(Paragraph("Stage 18 — Problem-Solving Templates", h1_style))
    story.append(Paragraph("Reusable algorithmic templates for the 18 core design patterns.", body_style))
    story.append(Spacer(1, 10))
    
    # 1. Two Pointers
    story.append(Paragraph("1. Two Pointers", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Input is a sorted array/list, and we need to find pairs matching a target sum or condition.", body_style))
    story.append(make_code_block(
"def two_pointers(arr, target):\n"
"    left, right = 0, len(arr) - 1\n"
"    while left < right:\n"
"        val = arr[left] + arr[right]\n"
"        if val == target: return left, right\n"
"        elif val < target: left += 1\n"
"        else: right -= 1\n"
"    return -1", code_style
    ))
    story.append(Spacer(1, 8))
    
    # 2. Sliding Window
    story.append(Paragraph("2. Sliding Window (Variable Size)", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Find the contiguous subarray (longest/shortest) matching a sum or distinct characters constraint.", body_style))
    story.append(make_code_block(
"def sliding_window(arr, constraint):\n"
"    left, max_len = 0, 0\n"
"    state = {}\n"
"    for right in range(len(arr)):\n"
"        # update state with arr[right]\n"
"        while not valid(state):\n"
"            # remove arr[left] from state\n"
"            left += 1\n"
"        max_len = max(max_len, right - left + 1)\n"
"    return max_len", code_style
    ))
    story.append(Spacer(1, 8))
    
    # 3. Binary Search
    story.append(Paragraph("3. Binary Search Template", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Target query on a sorted lookup space, or finding minimum/maximum matching values.", body_style))
    story.append(make_code_block(
"def binary_search(arr, target):\n"
"    low, high = 0, len(arr) - 1\n"
"    ans = -1\n"
"    while low <= high:\n"
"        mid = (low + high) // 2\n"
"        if condition(arr[mid], target):\n"
"            ans = mid\n"
"            high = mid - 1 # search left\n"
"        else:\n"
"            low = mid + 1  # search right\n"
"    return ans", code_style
    ))
    story.append(Spacer(1, 8))
    
    # 4. BFS Graph
    story.append(Paragraph("4. Breadth-First Search (BFS) Graph", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Shortest path on unweighted graphs, or level-order tree expansions.", body_style))
    story.append(make_code_block(
"from collections import deque\n"
"def bfs(graph, start):\n"
"    visited = {start}\n"
"    queue = deque([start])\n"
"    while queue:\n"
"        node = queue.popleft()\n"
"        for neighbor in graph[node]:\n"
"            if neighbor not in visited:\n"
"                visited.add(neighbor)\n"
"                queue.append(neighbor)", code_style
    ))
    story.append(Spacer(1, 8))
    
    # 5. Backtracking
    story.append(Paragraph("5. Backtracking Template", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Generate all subsets, combinations, permutations, or validate N-Queens puzzle configurations.", body_style))
    story.append(make_code_block(
"def backtrack(state, options, path, result):\n"
"    if is_solution(state):\n"
"        result.append(list(path))\n"
"        return\n"
"    for option in options:\n"
"        if valid(option, state):\n"
"            path.append(option)\n"
"            update(state, option)\n"
"            backtrack(state, options, path, result)\n"
"            path.pop() # rollback\n"
"            rollback(state, option)", code_style
    ))
    story.append(Spacer(1, 8))
    
    # 6. Topological Sort (Kahn's)
    story.append(Paragraph("6. Topological Sort (BFS Indegree)", h2_style))
    story.append(Paragraph("<b>How to Recognize:</b> Schedule tasks under dependencies (e.g. Course Schedule), finding scheduling sequence.", body_style))
    story.append(make_code_block(
"from collections import deque\n"
"def topo_sort(num_nodes, graph):\n"
"    indegree = {i: 0 for i in range(num_nodes)}\n"
"    for u in graph: \n"
"        for v in graph[u]: indegree[v] += 1\n"
"    queue = deque([n for n in indegree if indegree[n] == 0])\n"
"    order = []\n"
"    while queue:\n"
"        u = queue.popleft()\n"
"        order.append(u)\n"
"        for v in graph[u]:\n"
"            indegree[v] -= 1\n"
"            if indegree[v] == 0: queue.append(v)\n"
"    return order if len(order) == num_nodes else []", code_style
    ))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 19 ------------------
    story.append(Paragraph("Stage 19 — Practice Roadmap", h1_style))
    story.append(Paragraph("A progressive, structured problem sheets to gauge validation competency.", body_style))
    story.append(Spacer(1, 10))
    
    practice_levels = [
        ("Level 1 — Fundamentals", "50 Problems", "LeetCode Easy, AtCoder ABC (A-B). Focus on array loops, basic stacks, string processing, and O(N) traversals. Expected Skills: basic syntax, recursion trees."),
        ("Level 2 — Intermediate", "100 Problems", "LeetCode Medium, Codeforces Div2 (A-B). Focus on two pointers, sliding windows, hashing maps, linked lists, and recursion. Expected Skills: O(N) optimizations, DFS/BFS."),
        ("Level 3 — Advanced Patterns", "150 Problems", "LeetCode Medium/Hard, Codeforces Div2 (C). Focus on backtracking subsets, heaps, basic BSTs, standard graphs (BFS/DFS, Topological Sort), and basic DP. Expected Skills: recursion path tracking."),
        ("Level 4 — Optimization", "200 Problems", "LeetCode Hard, Codeforces Div2 (D-E). Focus on complex 2D DP, shortest path graphs (Dijkstra), MST trees, Trie matching, and Fenwick trees. Expected Skills: DP transitions."),
        ("Level 5 — Competitive Programming", "Continuous Practice", "Codeforces Div1 (A-C), AtCoder AGC. Focus on Range queries (Segment Trees), mathematical inversions, modular inverses, bitmask DP, and off-line queries. Expected Skills: CP optimizations.")
    ]
    
    for lvl_name, count, desc in practice_levels:
        story.append(Paragraph(f"<b>{lvl_name} ({count})</b>", h2_style))
        story.append(create_callout_box(desc, "SHOULD", styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 20 ------------------
    story.append(Paragraph("Stage 20 — Dedicated Interview Tracks", h1_style))
    story.append(Paragraph("Tailored tracks depending on target career aspirations and interview environments.", body_style))
    story.append(Spacer(1, 10))
    
    # Product Track
    story.append(Paragraph("Product Companies (Meta/Google/Amazon)", h2_style))
    track1 = (
        "<b>Focus Areas:</b> Medium/Hard LeetCode problems (80% Medium, 20% Hard). Master Two Pointers, Trees, Graphs, BFS/DFS, and dynamic programming patterns.<br/>"
        "<b>Key Competency:</b> Ability to identify the underlying pattern (e.g. Monotonic Stack) quickly and explain time/space complexities clearly under pressure."
    )
    story.append(create_callout_box(track1, "MUST", styles))
    story.append(Spacer(1, 8))
    
    # CP Track
    story.append(Paragraph("Competitive Programming Track (Codeforces/AtCoder)", h2_style))
    track2 = (
        "<b>Focus Areas:</b> Mathematical number theory, range trees, sweep line coordinates, segment trees, and offline queries.<br/>"
        "<b>Key Competency:</b> Absolute speed, optimization under tight time limit constraints (e.g. O(N log N) limit for N=2*10^5), and handling complex invariants."
    )
    story.append(create_callout_box(track2, "ADVANCED", styles))
    story.append(Spacer(1, 8))
    
    # General Track
    story.append(Paragraph("General Software Engineering Interviews", h2_style))
    track3 = (
        "<b>Focus Areas:</b> LeetCode Easy to Medium. Solid implementation of classic stacks, queues, hash sets, binary trees, and basic recursion.<br/>"
        "<b>Key Competency:</b> Readable code, clean variable names, explaining code flow, dry-running inputs, and handling basic edge cases."
    )
    story.append(create_callout_box(track3, "SHOULD", styles))
    
    story.append(PageBreak())
    
    # ------------------ TIMELINES ------------------
    story.append(Paragraph("Recommended Timeline Plans &amp; Checklists", h1_style))
    story.append(Paragraph("Structured timetables designed for algorithmic progression.", body_style))
    story.append(Spacer(1, 10))
    
    # Table of Roadmaps
    timeline_data = [
        [Paragraph("<b>Duration</b>", th_style), Paragraph("<b>Target Focus</b>", th_style), Paragraph("<b>Weekly Milestones</b>", th_style)],
        [Paragraph("30-Day Plan", td_style), Paragraph("Core Syntax &amp; Lin. structures", td_style), Paragraph("Week 1-2: Complexity, Arrays, Two Pointers, Strings. Week 3: Stacks, Queues, Hash Maps. Week 4: Singly Lists, recursion basics, and Level 1 problems.", td_style)],
        [Paragraph("3-Month Plan", td_style), Paragraph("Non-Linear &amp; Basic Graphs", td_style), Paragraph("Month 1: Arrays, Lists, Stacks. Month 2: Binary Trees, BST validations, Heaps. Month 3: Graph BFS/DFS, basic backtracking combinations, and Level 2 problems.", td_style)],
        [Paragraph("6-Month Plan", td_style), Paragraph("Optimization &amp; Algorithms", td_style), Paragraph("Months 1-3: Non-Linear trees &amp; Graphs. Month 4: Shortest paths, Prim's, DSU. Month 5: Dynamic Programming, Greedy selections. Month 6: Trie, bitwise algorithms, and Level 3 problems.", td_style)],
        [Paragraph("12-Month Plan", td_style), Paragraph("CP Specialist &amp; Advanced structures", td_style), Paragraph("Months 1-6: Advanced DSA patterns. Months 7-9: Segment Trees, Fenwick, string KMP, math sieve. Months 10-11: Coordinate sweeps, offline queries, mock contests. Month 12: System case studies, interview revision.", td_style)]
    ]
    t_time = Table(timeline_data, colWidths=[80, 150, 274])
    t_time.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_time)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Do Not Learn Everything at Once", h2_style))
    story.append(Paragraph(
        "To prevent cognitive overload, postpone these advanced topics until your core data structures "
        "(arrays, lists, trees, graphs) and optimization paradigms (basic DP, recursion, sorting) are solid: "
        "lazy propagation segment trees, string KMP, digit DP, bitmask DP, coordinate sweeps, and number theory "
        "modular multiplicative inverses.",
        body_style
    ))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Final DSA Competency Checklist", h2_style))
    checklist_items = [
        "Can analyze any recursive function's time and space complexity using a recursion tree.",
        "Knows when to use Two Pointers vs. Sliding Window vs. Prefix Sums.",
        "Can implement Singly and Doubly Linked List node deletions and reversals without syntax errors.",
        "Understand next-greater-element monotonic stack algorithms.",
        "Can validly check cycle detections in directed and undirected graphs.",
        "Can define DP states and establish transitions for Knapsack and Subsequence problems.",
        "Can package a graph topological sort using Kahn's BFS or DFS."
    ]
    for item in checklist_items:
        story.append(Paragraph(f"[  ] {item}", bullet_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated DSA career roadmap PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
