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
            # Top block background decoration (Dark Navy)
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
        self.drawString(54, 750, "AI SPECIALIST ROADMAP")
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "Complete Career & Engineering Guide")
        
        # Header Line Separator
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Running Footer
        self.drawString(54, 40, "Confidential — Artificial Intelligence Learning Curriculum")
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
    Formats a python/system code block with a light gray background.
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

def build_pdf(filename="AI_Specialist_Roadmap.pdf"):
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
    
    # Register styles
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
    story.append(Paragraph("AI Specialist", cover_title_style))
    story.append(Paragraph("Complete Learning &amp; Career Roadmap", cover_subtitle_style))
    
    story.append(Spacer(1, 230))
    story.append(Paragraph("Welcome to the AI Specialist Curriculum", welcome_title_style))
    story.append(Paragraph(
        "This roadmap is designed to build a deep theoretical understanding and high-performance engineering "
        "skills in Artificial Intelligence. The curriculum covers classic state-space searches, deep learning, "
        "computer vision architectures, advanced Natural Language Processing, Large Language Models (LLMs), "
        "Retrieval-Augmented Generation (RAG), AI Agent architectures, containerized model serving, "
        "and critical AI Safety guardrails.",
        welcome_body_style
    ))
    
    story.append(Paragraph("<b>Table of Stages / Content Map:</b>", h3_style))
    stages = [
        "Stage 0 — Prerequisites (Python, NumPy, SQL, Linux, Basic Math)",
        "Stage 1 — Artificial Intelligence Fundamentals (PEAS, DFS/BFS, UCS, A*, Minimax, Logic)",
        "Stage 2 — Mathematics for AI (Linear Algebra, Calculus, Convex Optimization, Loss Functions)",
        "Stage 3 — Neural Networks &amp; Deep Learning (Backpropagation, Optimizers, Regularization)",
        "Stage 4 — Computer Vision (CNNs, ResNet, Object Detection YOLO, Segmentations, ViTs)",
        "Stage 5 — Natural Language Processing (Embeddings, LSTM, Self-Attention, Transformers)",
        "Stage 6 — Large Language Models (LLMs) (Pretraining, Fine-tuning, RLHF, Quantization, LoRA)",
        "Stage 7 — Generative AI (VAEs, GANs, Diffusion models, Multimodal Vision-Language models)",
        "Stage 8 — Retrieval-Augmented Generation (RAG) (Chunking, Vector Databases, Reranking, Evaluation)",
        "Stage 9 — AI Agents (Tool calling, planning, reflection, ReAct, multi-agent systems)",
        "Stage 10 — AI Engineering (APIs, Model serving, FastAPI, Docker, GPU fundamentals, Caching)",
        "Stage 11 — AI Safety &amp; Responsible AI (Hallucinations, Jailbreaks, Guardrails, Governance)",
        "Stage 12 — 20 Progression Projects (5 Beginner, 5 Inter., 5 Adv., 5 Production-grade)",
        "Stage 13 — AI Specialist Interview Preparation &amp; System Design Case Studies"
    ]
    for s in stages:
        story.append(Paragraph(f"&bull; {s}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 0 ------------------
    story.append(Paragraph("Stage 0 — Prerequisites", h1_style))
    story.append(Paragraph("Minimum competencies required before attempting neural network layers and state search spaces.", body_style))
    
    prereqs = [
        ("Python & Core Math", "MUST", "Comfortable implementing classes, decorators, OOP. Linear Algebra: matrix multiplication, transposes, dimensions. Calculus: derivatives and partial derivatives."),
        ("Collections & NumPy", "MUST", "Vectorized calculations, array broadcasts, dot products, matrix slicing without using loops."),
        ("SQL & Git", "MUST", "Retrieving datasets from databases, merging tables, and committing/pushing production code splits."),
        ("Linux & Command Line", "SHOULD", "Navigating paths, configuring environment variables, running python scripts via shell, and basic pip packages management.")
    ]
    for name, level, desc in prereqs:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 1 ------------------
    story.append(Paragraph("Stage 1 — Artificial Intelligence Fundamentals", h1_style))
    story.append(Paragraph("Classic algorithmic search and representation paradigms.", body_style))
    
    stage1_topics = [
        ("Intelligent Agents & PEAS", "MUST", "Agent: perceives environment through sensors, acts via actuators. PEAS: Performance measure, Environment, Actuators, Sensors. Defines task environments."),
        ("Uninformed Search (BFS, DFS, UCS)", "MUST", "BFS: level order, optimal for unweighted. DFS: depth first, low memory. UCS (Uniform Cost Search): expands node with lowest path cost, optimal for weighted edges."),
        ("Heuristic Search (A*, Greedy Best First)", "MUST", "Greedy: expands node with lowest h(n). A* Search: minimizes f(n) = g(n) + h(n). Optimal if heuristic h(n) is admissible (never overestimates actual cost) and consistent."),
        ("Adversarial Search (Minimax, Alpha-Beta)", "MUST", "Minimax: decision rule for multi-player games. Alpha-Beta Pruning: decreases nodes evaluated by pruning branches that cannot impact final decisions (bounds alpha/beta)."),
        ("Knowledge Representation & Logic", "SHOULD", "Propositional Logic (evaluates absolute True/False variables) and First-Order Logic (incorporates predicates, objects, and quantifiers like 'for all' and 'exists').")
    ]
    for name, level, desc in stage1_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Key Search Algorithms Comparison", h2_style))
    
    search_table = [
        [Paragraph("<b>Algorithm</b>", th_style), Paragraph("<b>Time Complexity</b>", th_style), Paragraph("<b>Space Complexity</b>", th_style), Paragraph("<b>Optimality</b>", th_style)],
        [Paragraph("BFS", td_style), Paragraph("O(b<sup>d</sup>)", td_style), Paragraph("O(b<sup>d</sup>) (high memory)", td_style), Paragraph("Yes (if edge costs are 1)", td_style)],
        [Paragraph("DFS", td_style), Paragraph("O(b<sup>m</sup>)", td_style), Paragraph("O(b * m) (low memory)", td_style), Paragraph("No", td_style)],
        [Paragraph("UCS", td_style), Paragraph("O(b<sup>1 + floor(C*/e)</sup>)", td_style), Paragraph("O(b<sup>1 + floor(C*/e)</sup>)", td_style), Paragraph("Yes (if edge costs &ge; e &gt; 0)", td_style)],
        [Paragraph("A*", td_style), Paragraph("O(b<sup>d</sup>) (exponential)", td_style), Paragraph("O(b<sup>d</sup>) (keeps all in memory)", td_style), Paragraph("Yes (if heuristic is admissible)", td_style)]
    ]
    t_search = Table(search_table, colWidths=[100, 140, 134, 130])
    t_search.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_search)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 2 ------------------
    story.append(Paragraph("Stage 2 — Mathematics for AI", h1_style))
    story.append(Paragraph("The mathematical engine powering optimization and representation.", body_style))
    
    math_topics = [
        ("Linear Algebra & Derivatives", "MUST", "Matrix dimensions, dot products, projections, eigenvalues/eigenvectors, partial derivatives, Jacobian matrices, chain rule."),
        ("Convexity & Optimization", "SHOULD", "Convex functions (local minimum is global minimum), Gradient Descent (optimizing weights sequentially in direction of steepest descent)."),
        ("Loss Functions", "MUST", "Mean Squared Error (regression), Binary Cross-Entropy (binary classification), Categorical Cross-Entropy (multi-class predictions).")
    ]
    for name, level, desc in math_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 3 ------------------
    story.append(Paragraph("Stage 3 — Neural Networks &amp; Deep Learning", h1_style))
    story.append(Paragraph("Deep representations constructed via chain rule backpropagation.", body_style))
    
    stage3_topics = [
        ("Perceptron & Activation Functions", "MUST", "Perceptron: output = activation(w*x + b). Activation functions: Sigmoid (0 to 1), Tanh (-1 to 1), ReLU (max(0, x), avoids gradients vanishing), LeakyReLU (prevents dead neurons)."),
        ("Forward & Backpropagation", "MUST", "Forward: compute layer-by-layer activations. Backpropagation: calculates gradients of loss function with respect to weights using chain rule, propagating error backward."),
        ("Optimizers (Momentum, Adam)", "MUST", "SGD with Momentum: adds velocity vector to smooth out oscillations. Adam (Adaptive Moment Estimation): maintains adaptive learning rates using first and second moments of gradients."),
        ("Regularizations (Dropout, Batch Norm)", "MUST", "Dropout: randomly deactivates neurons during training to prevent co-adaptation. Batch Normalization: standardizes layer inputs per batch to accelerate convergence.")
    ]
    for name, level, desc in stage3_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 4 ------------------
    story.append(Paragraph("Stage 4 — Computer Vision", h1_style))
    story.append(Paragraph("Architectures designed to extract spatial features from image pixels.", body_style))
    
    stage4_topics = [
        ("CNN Layers (Convolutions, Pooling)", "MUST", "Convolution: kernel sliding over pixels to create feature maps. Padding: keeping dimensions constant. Stride: step size. Pooling (Max/Average): spatial downsampling."),
        ("ResNet & Transfer Learning", "MUST", "ResNet: skip connections (identity shortcuts) allowing gradients to flow directly, resolving vanishing gradients in very deep networks. Transfer learning: using pre-trained weights (e.g. ImageNet)."),
        ("Object Detection (YOLO, Faster R-CNN)", "SHOULD", "YOLO (You Only Look Once): single-stage detector, predicts boxes and probabilities in one forward pass (high speed). Faster R-CNN: two-stage detector using Region Proposal Networks (high accuracy)."),
        ("Vision Transformers (ViT)", "ADVANCED", "Applying self-attention to patches of images. Split image into grid patches, flatten them, add positional encoding, and feed into a standard transformer encoder.")
    ]
    for name, level, desc in stage4_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 5 ------------------
    story.append(Paragraph("Stage 5 — Natural Language Processing (NLP)", h1_style))
    story.append(Paragraph("Representing and sequence modelling textual parameters.", body_style))
    
    stage5_topics = [
        ("Classical NLP & Embeddings", "MUST", "Tokenization, lemmatization, Bag of Words, TF-IDF. Word2Vec/GloVe: dense low-dimensional vector representations capturing semantic similarities."),
        ("Recurrent Networks (LSTM, GRU)", "MUST", "RNN: sequential tokens scan. LSTM (Long Short-Term Memory): maintains cell state, controlled via Input, Forget, and Output gates, resolving short-term memory decays. GRU: simplified gates (Reset/Update)."),
        ("Self-Attention & Multi-Head Attention", "MUST", "Self-Attention: calculates token relationships by computing Query (Q), Key (K), and Value (V) dot products: Attention(Q,K,V) = softmax(Q*K^T / sqrt(d_k)) * V. Multi-Head: performs projections in parallel.")
    ]
    for name, level, desc in stage5_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 6 ------------------
    story.append(Paragraph("Stage 6 — Large Language Models (LLMs)", h1_style))
    story.append(Paragraph("Billions of parameters models optimized via next-token predictions.", body_style))
    
    stage6_topics = [
        ("Pretraining & Next-Token Prediction", "MUST", "Generative pretraining on massive web-scale corpora using causal language modeling (predicting the next token given context)."),
        ("Fine-Tuning (Instruction & RLHF)", "MUST", "Instruction Tuning: training model on prompt-response pairs. RLHF (Reinforcement Learning from Human Feedback): aligning models using a reward predictor and PPO or DPO."),
        ("PEFT & Parameter Efficiency (LoRA)", "MUST", "LoRA (Low-Rank Adaptation): freezes model weights and inserts low-rank decomposition matrices (A and B) into attention layers, reducing trainable parameters by 99%."),
        ("Quantization (QLoRA)", "SHOULD", "Reducing precision (e.g. from FP16 to INT4/INT8) using double quantization and Pageable Optimizers, enabling LLM fine-tuning on consumer-grade GPUs.")
    ]
    for name, level, desc in stage6_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 7 ------------------
    story.append(Paragraph("Stage 7 — Generative AI", h1_style))
    story.append(Paragraph("Generative models synthesizing structured pixel, audio, or text parameters.", body_style))
    
    stage7_topics = [
        ("Variational Autoencoders (VAEs)", "SHOULD", "Compresses images into a latent space (mean and log-variance) and reconstructs them, regularized via Kullback-Leibler (KL) divergence."),
        ("Generative Adversarial Networks (GANs)", "SHOULD", "Two-player minimax game: Generator synthesizes fake samples; Discriminator attempts to classify real vs. fake. Trained in parallel."),
        ("Diffusion Models", "MUST", "Generates high-fidelity images by reversing a forward noise process. Slowly adds noise to image, then trains a U-Net model to predict and subtract noise step-by-step.")
    ]
    for name, level, desc in stage7_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 8 ------------------
    story.append(Paragraph("Stage 8 — Retrieval-Augmented Generation (RAG)", h1_style))
    story.append(Paragraph("Injecting external verified knowledge documents into LLM prompts without retraining weights.", body_style))
    
    stage8_topics = [
        ("Vector Databases & Embeddings", "MUST", "Converting chunks of documents into floating-point vectors. Storing in databases (Chroma, FAISS, Pinecone) for similarity searches."),
        ("Chunking Strategies & Retrieval", "MUST", "Split documents logically (e.g. recursive character splits with 500-token size, 50-token overlap). Retrieve top-K chunks using cosine similarity."),
        ("Reranking & Hybrid Search", "SHOULD", "Hybrid: combine keyword BM25 search with dense vector search. Reranking: using Cross-Encoder models to re-evaluate semantic matches, filtering top chunks to fit context windows."),
        ("RAG Evaluation & Failure Modes", "MUST", "Evaluation metrics (faithfulness, answer relevance, context recall) using frameworks like Ragas. Failure modes: out-of-context chunks, LLM hallucination despite retrieve.")
    ]
    for name, level, desc in stage8_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 9 ------------------
    story.append(Paragraph("Stage 9 — AI Agents", h1_style))
    story.append(Paragraph("Autonomous entities combining reasoning, tool use, memory, and multi-agent structures.", body_style))
    
    stage9_topics = [
        ("Agent Reasoning & ReAct", "MUST", "ReAct (Reason + Action) loop: Thought (reason about state), Action (call tool), Observation (read tool output), Repeat. Prevents flat prompt actions."),
        ("Tool Calling & State Memory", "MUST", "LLMs outputting JSON matching tool schemas. Memory: maintaining conversational state, summarizations, or key-value memory banks."),
        ("Multi-Agent Orchestration", "ADVANCED", "Splitting complex workflows into dedicated agents (e.g. Planner, Researcher, Writer) communicating via message buses (LangGraph).")
    ]
    for name, level, desc in stage9_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 10 ------------------
    story.append(Paragraph("Stage 10 — AI Engineering &amp; Serving", h1_style))
    story.append(Paragraph("Deploying, hosting, and optimizing large neural architectures.", body_style))
    
    stage10_topics = [
        ("API Serving & FastAPI", "MUST", "Exposing models via REST endpoints. Creating input-validation schemas using Pydantic inside FastAPI."),
        ("Containerization (Docker)", "MUST", "Packaging environment variables, CUDA requirements, and python scripts inside a lightweight Docker container for cloud scaling."),
        ("GPU Optimization & Inference", "SHOULD", "Optimizing memory: batching queries, setting up prompt caching, and using vLLM (PagedAttention) to scale concurrent serving throughput.")
    ]
    for name, level, desc in stage10_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 11 ------------------
    story.append(Paragraph("Stage 11 — AI Safety &amp; Responsible AI", h1_style))
    story.append(Paragraph("Securing deployments against adversarial prompt injections and jailbreaks.", body_style))
    
    stage11_topics = [
        ("Hallucination & Bias Mitigation", "MUST", "Evaluating output alignments, checking truthfulness benchmarks, and implementing system prompts to bound response structures."),
        ("Prompt Injection & Jailbreaking", "MUST", "Adversarial prompts attempting to override system instructions. Secure via input guardrails (Llama Guard) and token validation filters."),
        ("AI Governance & Guardrails", "SHOULD", "Ensuring data privacy compliance (GDPR, HIPAA) and running post-generation toxic content analysis.")
    ]
    for name, level, desc in stage11_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 12 ------------------
    story.append(Paragraph("Stage 12 — 20 Progression Projects", h1_style))
    story.append(Paragraph("Practical portfolios designed to validate production-level AI engineering capabilities.", body_style))
    story.append(Spacer(1, 6))
    
    # 5 Beginner Projects
    story.append(Paragraph("Level 1 — Beginner Projects (5 Projects)", h2_style))
    beg_projects = [
        "1. Image Classifier (PyTorch + CIFAR-10 - training CNN from scratch, calculating validation loss)",
        "2. Custom A* Path Finder (Python - search space visualization, grid-obstacle coordinate heuristic maps)",
        "3. Text Sentiment Classifier (PyTorch + LSTM on movie reviews, embedding layer setups)",
        "4. Perceptron logic gate simulator (Scratch code - plotting linear decision boundaries for AND/OR gates)",
        "5. TF-IDF document search engine (Python - sparse representation and cosine similarity retrieval)"
    ]
    for p in beg_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))
    
    # 5 Intermediate Projects
    story.append(Paragraph("Level 2 — Intermediate Projects (5 Projects)", h2_style))
    int_projects = [
        "1. Transfer Learning ResNet Image Classifier (PyTorch - freezing backbone weights, custom output heads)",
        "2. YOLO Object Detector Pipeline (YOLOv8 + OpenCV - local video stream bbox drawing)",
        "3. Next-Character GRU Text Generator (PyTorch - character-level tokenization, temperature scaling)",
        "4. Fine-Tune Llama-3-8B using LoRA (Unsloth/HuggingFace - dataset formatting, save adapters)",
        "5. Basic RAG document Q&A (ChromaDB + OpenAI API + LangChain - basic chunk-and-retrieval pipeline)"
    ]
    for p in int_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))

    # 5 Advanced Projects
    story.append(Paragraph("Level 3 — Advanced Projects (5 Projects)", h2_style))
    adv_projects = [
        "1. Vision Transformer from scratch (PyTorch - grid patching, patch embeddings, multi-head self-attention)",
        "2. VAE Image Synthesizer (PyTorch - latent space reparameterization trick, reconstruction loss plotting)",
        "3. Advanced RAG with Reranking & Hybrid search (Qdrant + Cohere Rerank + BM25 + Weaviate)",
        "4. Autonomous ReAct Agent with Tool calling (LangGraph - state transitions, SQL tools access)",
        "5. Containerized GPU model server (FastAPI + Docker + vLLM - hosting Llama-3, benchmark latency)"
    ]
    for p in adv_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))

    # 5 Portfolio / Production Projects
    story.append(Paragraph("Level 4 — Portfolio/Production Projects (5 Projects)", h2_style))
    prod_projects = [
        "1. Enterprise RAG Pipeline (Document ingestion pipeline, chunking evaluation, semantic search + LLM Guardrails)",
        "2. Multi-Agent Software Development Team (Coder agent, tester agent, manager agent orchestrating code fixes)",
        "3. Fine-Tuned Domain-Specific LLM (Instruction tuning via QLoRA, alignment with DPO, deployed to production)",
        "4. Real-time Video Segmentation Stream (U-Net segmentation serving on edge GPUs, low latency optimizing)",
        "5. Secure AI Assistant Gateway (FastAPI proxy with prompt-injection scanners and cost/token caches)"
    ]
    for p in prod_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 13 ------------------
    story.append(Paragraph("Stage 13 — AI Specialist Interview Preparation", h1_style))
    story.append(Paragraph("Common technical evaluation cases and target responses.", body_style))
    story.append(Spacer(1, 10))
    
    questions = [
        ("Deep Learning: Explaining Vanishing Gradients", "Vanishing gradients occur when backpropagated gradients shrink exponentially as they flow backward through deep layers, halting weight updates in early layers. Fixes: 1) ReLU activation, 2) ResNet skip connections, 3) Batch Normalization, 4) Xavier/He weight initializations."),
        ("LLMs: Intuition of self-attention scaling factor", "Scaling query-key dot products by 1/sqrt(d_k) prevents the values from growing extremely large in magnitude, which would push the softmax function into regions with extremely small gradients (causing vanishing gradient issues during backprop)."),
        ("RAG System Design: How to design a legal document search engine?", "Architecture: 1) Extract PDFs using OCR, 2) Split using recursive layout-aware chunking, 3) Embed chunks using a domain-specific model (e.g. legal-BERT), 4) Save to vector database (Qdrant), 5) Use hybrid search + Cohere reranker to fetch top-5 chunks, 6) Feed to LLM with system prompt limiting context answers, 7) Evaluate correctness via Ragas."),
        ("AI Safety: Describe prompt injection mitigation strategies.", "Mitigate by: 1) Separating system commands from user text using XML tags, 2) Passing user text through a classifier (Llama Guard) before LLM generation, 3) Using strict JSON outputs schema via outlines/Pydantic to constrain model output spaces.")
    ]
    for q, ans in questions:
        story.append(Paragraph(f"<b>Q: {q}</b>", h3_style))
        story.append(Paragraph(ans, body_style))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ TIMELINES ------------------
    story.append(Paragraph("Recommended Timeline Plans &amp; Checklists", h1_style))
    story.append(Paragraph("Structured timetables designed for AI Specialist career paths.", body_style))
    story.append(Spacer(1, 10))
    
    # Table of Roadmaps
    timeline_data = [
        [Paragraph("<b>Duration</b>", th_style), Paragraph("<b>Target Focus</b>", th_style), Paragraph("<b>Weekly Milestones</b>", th_style)],
        [Paragraph("3-Month Plan", td_style), Paragraph("Core Math &amp; Deep Learning", td_style), Paragraph("Week 1-4: Linear algebra, calculus, search algorithms. Week 5-8: PyTorch, backpropagation, MLP models. Week 9-12: CNN basics, classical NLP, and Level 1 projects.", td_style)],
        [Paragraph("6-Month Plan", td_style), Paragraph("NLP, Vision &amp; LLMs", td_style), Paragraph("Months 1-3: Math &amp; PyTorch. Month 4: Object detection (YOLO), transfer learning. Month 5: Transformers self-attention, tokenization, fine-tuning. Month 6: Level 2 projects.", td_style)],
        [Paragraph("12-Month Plan", td_style), Paragraph("Generative AI &amp; Engineering", td_style), Paragraph("Months 1-6: Deep learning and NLP foundations. Month 7-8: Diffusion models, Generative AI. Month 9-10: Vector databases, Advanced RAG, AI Agents, LangGraph. Month 11: FastAPI serving, Docker, GPU optimization, Level 3/4 projects. Month 12: Interview preparation.", td_style)]
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
    
    story.append(Paragraph("Final AI Specialist Competency Checklist", h2_style))
    checklist_items = [
        "Can write backpropagation formulas using multi-variable chain rule derivatives.",
        "Understand the mechanics of skip connections in ResNet and self-attention in Transformers.",
        "Can fine-tune an LLM on custom datasets using LoRA/QLoRA in Hugging Face.",
        "Can design and deploy a production RAG pipeline using vector DBs and rerankers.",
        "Can build state-managed multi-agent workflows using LangGraph.",
        "Can serve models inside a FastAPI endpoint packaged inside a Docker container.",
        "Understand how to evaluate and mitigate prompt injections and hallucinations."
    ]
    for item in checklist_items:
        story.append(Paragraph(f"[  ] {item}", bullet_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated AI Specialist career roadmap PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
