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
        self.drawString(54, 750, "DATA SCIENCE SPECIALIST ROADMAP")
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "Complete Career & Analytical Guide")
        
        # Header Line Separator
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Running Footer
        self.drawString(54, 40, "Confidential — Data Science Learning Curriculum")
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
    Formats a python/sql code block with a light gray background.
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

def get_algorithm_blocks(styles):
    """
    Returns list of Flowables for each of the algorithms in Stage 6.
    """
    h2_style = styles['Heading2Style']
    body_style = styles['BodyStyle']
    
    # 1. Linear Regression
    lr = [
        Paragraph("1. Linear Regression (Regression)", h2_style),
        create_callout_box("Foundational algorithm for continuous target prediction.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Modeling a linear relationship between features and target by fitting a straight line that minimizes distance to the actual data points.", body_style),
        Paragraph("<b>2. Mathematics:</b> <i>y</i> = <i>w</i><sub>0</sub> + <i>w</i><sub>1</sub><i>x</i><sub>1</sub> + ... + <i>w</i><sub>n</sub><i>x</i><sub>n</sub> + <i>e</i>. Fits line by minimizing Mean Squared Error (MSE) via Ordinary Least Squares (OLS).", body_style),
        Paragraph("<b>3. Assumptions:</b> Linearity, Homoscedasticity (constant variance of residuals), Independence of errors, Normality of error distributions.", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `fit_intercept` (bool).", body_style),
        Paragraph("<b>5. Advantages:</b> Simple, highly interpretable, fast training, no tuning needed.", body_style),
        Paragraph("<b>6. Disadvantages:</b> Assumes linear relations, sensitive to outliers and multicollinearity.", body_style),
        Paragraph("<b>7. When to Use:</b> Continuous target variable with clear linear relationships; baseline regression modeling.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> Non-linear relationships or complex datasets with thousands of interacting features.", body_style),
        Spacer(1, 10)
    ]
    
    # 2. Logistic Regression
    logr = [
        Paragraph("2. Logistic Regression (Classification)", h2_style),
        create_callout_box("The foundational baseline for binary and multi-class classification.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Predicts probability of membership in a class using the Sigmoid (logistic) function, outputting a value between 0 and 1.", body_style),
        Paragraph("<b>2. Mathematics:</b> <i>p</i> = 1 / (1 + <i>e</i><sup>-(<b>w</b><sup>T</sup><b>x</b> + <i>b</i>)</sup>). Fits parameters via Maximum Likelihood Estimation.", body_style),
        Paragraph("<b>3. Assumptions:</b> Binary/Ordinal target, Independence of observations, Little or no multicollinearity among independent variables.", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `C` (inverse regularization strength), `penalty` ('l1', 'l2', 'elasticnet'), `solver` ('lbfgs', 'saga').", body_style),
        Paragraph("<b>5. Advantages:</b> Extremely fast, outputs calibrated probabilities, easy to regularize, interpretable weights.", body_style),
        Paragraph("<b>6. Disadvantages:</b> Assumes linear decision boundary, struggles with complex relationships.", body_style),
        Paragraph("<b>7. When to Use:</b> Binary classification baselines; when model interpretability and probability outputs are critical.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> Highly complex non-linear decision boundaries.", body_style),
        Spacer(1, 10)
    ]

    # 3. Decision Trees
    dt = [
        Paragraph("3. Decision Trees (Regression &amp; Classification)", h2_style),
        create_callout_box("Highly interpretable rule-based model.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Making decisions by splitting data recursively on features that maximize information gain (Gini or Entropy reduction).", body_style),
        Paragraph("<b>2. Mathematics:</b> Splitting criteria: Gini Impurity = 1 - Sum( <i>p<sub>i</sub></i><sup>2</sup> ); Entropy = -Sum( <i>p<sub>i</sub></i> * log<sub>2</sub>(<i>p<sub>i</sub></i>) ).", body_style),
        Paragraph("<b>3. Assumptions:</b> Non-parametric. No assumptions about data distribution.", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `max_depth`, `min_samples_split`, `min_samples_leaf`, `criterion`.", body_style),
        Paragraph("<b>5. Advantages:</b> No feature scaling required, highly interpretable rules, handles non-linearities and missing values.", body_style),
        Paragraph("<b>6. Disadvantages:</b> High variance, extremely prone to overfitting, unstable (small data changes change the tree entirely).", body_style),
        Paragraph("<b>7. When to Use:</b> Simple rules-based modeling where interpretability is the priority.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> When predicting smooth continuous variables, or when the decision boundary has diagonal elements.", body_style),
        Spacer(1, 10)
    ]

    # 4. Random Forest
    rf = [
        Paragraph("4. Random Forest (Regression &amp; Classification)", h2_style),
        create_callout_box("Robust ensemble model using bagging of independent decision trees.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Aggregates a large number of independent, deep decision trees trained on random bootstrap samples of data and random subsets of features.", body_style),
        Paragraph("<b>2. Mathematics:</b> Bootstrap Aggregating (Bagging) + Subspace Sampling. Combines independent trees by averaging (regression) or majority voting (classification) to reduce variance.", body_style),
        Paragraph("<b>3. Assumptions:</b> Non-parametric.", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `n_estimators`, `max_features`, `max_depth`, `min_samples_leaf`, `bootstrap`.", body_style),
        Paragraph("<b>5. Advantages:</b> Very robust, avoids overfitting, handles high dimensionality, provides feature importance.", body_style),
        Paragraph("<b>6. Disadvantages:</b> Slower inference, large memory footprint, acts as a 'black box' compared to a single tree.", body_style),
        Paragraph("<b>7. When to Use:</b> General purpose classification and regression on tabular data.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> Low latency real-time prediction environments, or when data is extremely sparse (e.g. text).", body_style),
        Spacer(1, 10)
    ]

    # 5. XGBoost
    xgb = [
        Paragraph("5. XGBoost (Regression &amp; Classification)", h2_style),
        create_callout_box("Highly optimized, industry-standard gradient boosting library.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Sequential boosting of weak decision trees, where each tree is trained to correct the residual errors of the prior ensemble, utilizing L1/L2 regularization on leaf weights.", body_style),
        Paragraph("<b>2. Mathematics:</b> Taylor series expansion of objective: <i>Loss</i><sup>(<i>t</i>)</sup> approx. Sum( <i>g<sub>i</sub></i>*<i>f<sub>t</sub></i>(<i>x<sub>i</sub></i>) + 0.5*<i>h<sub>i</sub></i>*<i>f<sub>t</sub></i><sup>2</sup>(<i>x<sub>i</sub></i>) ) + penalty.", body_style),
        Paragraph("<b>3. Assumptions:</b> Non-parametric.", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `eta` (learning_rate), `max_depth`, `lambda` (L2 reg), `alpha` (L1 reg), `subsample`, `colsample_bytree`.", body_style),
        Paragraph("<b>5. Advantages:</b> Native L1/L2 regularization, exceptional accuracy, handles missing values, parallel tree construction.", body_style),
        Paragraph("<b>6. Disadvantages:</b> Complex to tune, prone to overfitting if learning rate is too high, black box.", body_style),
        Paragraph("<b>7. When to Use:</b> Tabular datasets where maximum predictive accuracy is the main metric.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> When interpretability is required by regulators, or when dataset is extremely small (use simpler models).", body_style),
        Spacer(1, 10)
    ]

    # 6. PCA (Principal Component Analysis)
    pca = [
        Paragraph("6. Principal Component Analysis (Unsupervised)", h2_style),
        create_callout_box("Standard linear dimensionality reduction technique.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Projects high-dimensional data onto orthogonal axes (principal components) that maximize the variance of the data, reducing dimensions with minimal information loss.", body_style),
        Paragraph("<b>2. Mathematics:</b> Computes the covariance matrix, then calculates its eigenvalues and eigenvectors. Eigenvectors corresponding to the largest eigenvalues represent principal components.", body_style),
        Paragraph("<b>3. Assumptions:</b> Linearity (variables have linear relations), Scaled data (highly sensitive to scale difference).", body_style),
        Paragraph("<b>4. Hyperparameters:</b> `n_components` (number of components or percentage of variance to keep).", body_style),
        Paragraph("<b>5. Advantages:</b> Removes multicollinearity, reduces memory footprint, speeds up model training.", body_style),
        Paragraph("<b>6. Disadvantages:</b> Principal components are linear combinations of features and lose direct interpretability.", body_style),
        Paragraph("<b>7. When to Use:</b> High dimensional datasets where features are highly correlated, and for preprocessing before modeling.", body_style),
        Paragraph("<b>8. When NOT to Use:</b> When maintaining individual feature interpretability is required, or when the data manifold is highly non-linear.", body_style),
        Spacer(1, 10)
    ]
    
    return lr + logr + dt + rf + xgb + pca

def build_pdf(filename="Data_Science_Specialist_Roadmap.pdf"):
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
    story.append(Paragraph("Data Science Specialist", cover_title_style))
    story.append(Paragraph("Complete Learning &amp; Career Roadmap", cover_subtitle_style))
    
    story.append(Spacer(1, 230))
    story.append(Paragraph("Welcome to the Data Science Specialist Curriculum", welcome_title_style))
    story.append(Paragraph(
        "This curriculum is designed to take aspiring data professionals from the fundamentals of "
        "programming and database operations to production-level machine learning and experimentation. "
        "It emphasizes the ability to translate open-ended business problems into structured analytical tasks, "
        "covering: Business Problem &rarr; Data &rarr; EDA &rarr; Statistical Inference &rarr; Modeling "
        "&rarr; Metric Evaluation &rarr; Business Insights &rarr; Deployment &amp; Stakeholder Communication.",
        welcome_body_style
    ))
    
    story.append(Paragraph("<b>Table of Stages / Content Map:</b>", h3_style))
    stages = [
        "Stage 0 — Prerequisites (Python, NumPy, Pandas, SQL, Git)",
        "Stage 1 — Mathematics &amp; Statistics (Descriptive, Probability, Inference, Statistical Tests)",
        "Stage 2 — SQL Mastery (CTEs, Joins, Window Functions, Optimization)",
        "Stage 3 — Data Cleaning (MCAR/MAR/MNAR missingness, outlier clipping, quality checks)",
        "Stage 4 — Exploratory Data Analysis (EDA) (Univariate, Multivariate, Insights generation)",
        "Stage 5 — Feature Engineering (Log transforms, scaling, binning, selection, PCA)",
        "Stage 6 — Machine Learning (Supervised Regression &amp; Classification, Unsupervised)",
        "Stage 7 — Model Evaluation (Precision/Recall tradeoff, ROC/PR-AUC, calibration)",
        "Stage 8 — Experimentation &amp; A/B Testing (Sample sizing, power, multiple testing)",
        "Stage 9 — Business &amp; Product Analytics (KPIs, funnels, cohort analysis, CLV)",
        "Stage 10 — Time Series Forecasting (Stationarity, Autocorrelations, ARIMA/SARIMA)",
        "Stage 11 — Advanced Data Science (Causal inference, Survival analysis, Bayesian stats)",
        "Stage 12 — Data Science Engineering (ETL, APIs, FastAPI, Docker, MLflow, Monitoring)",
        "Stage 13 — 20 Progression Projects (5 Beginner, 5 Inter., 5 Adv., 5 Business/Product)",
        "Stage 14 — Data Science Interview Preparation &amp; Case Studies"
    ]
    for s in stages:
        story.append(Paragraph(f"&bull; {s}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 0 ------------------
    story.append(Paragraph("Stage 0 — Prerequisites", h1_style))
    story.append(Paragraph("Establish a strong base in tools, languages, and libraries before diving into statistical modelling.", body_style))
    story.append(Spacer(1, 4))
    
    prereqs = [
        ("Python", "MUST", "Core language used in modern data science. Focus on functions, loops, lists, dicts, and file operations."),
        ("NumPy", "MUST", "Numerical computing. Focus on array vectorization, slicing, array transformations, and dot products."),
        ("Pandas", "MUST", "Dataframes, cleaning operations, filtering rows, grouping, pivoting, merging, datetime conversions."),
        ("Matplotlib & Seaborn", "MUST", "Visualizing feature relationships, distributions, histograms, heatmaps, box plots."),
        ("SQL", "MUST", "Retrieving, aggregating, and joining data from relational database systems."),
        ("Git & GitHub", "SHOULD", "Version control, branching, commits, pulls, and pushing code to remote repositories."),
        ("Jupyter Notebooks", "MUST", "Interactive programming environment for coding, testing, and visualizing EDA code.")
    ]
    for name, level, why in prereqs:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(why, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 1 ------------------
    story.append(Paragraph("Stage 1 — Mathematics &amp; Statistics", h1_style))
    story.append(Paragraph("Statistical thinking is the core value driver of a data scientist. Master descriptive and inferential statistics.", body_style))
    
    # Descriptive Statistics
    story.append(Paragraph("Descriptive Statistics", h2_style))
    desc_stats = [
        ("Central Tendency (Mean, Median, Mode)", "MUST", "Mean: average (sensitive to outliers). Median: midpoint (outlier robust). Mode: most frequent."),
        ("Spread (Variance, Std Dev, Percentiles, IQR)", "MUST", "Variance &amp; Std Dev: measure dispersion. Percentiles: value below which a percentage of observations fall. IQR: Q3 - Q1 (outlier detection bounds)."),
        ("Shape (Skewness, Kurtosis)", "SHOULD", "Skewness: measures symmetry of distribution. Kurtosis: measures tailedness/peakedness (platykurtic vs. leptokurtic).")
    ]
    for name, level, desc in desc_stats:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    # Probability & Distributions
    story.append(Paragraph("Probability &amp; Distributions", h2_style))
    prob_dist = [
        ("Conditional Probability & Bayes Theorem", "MUST", "Bayes Theorem calculates post-event likelihood: P(A|B) = P(B|A)*P(A) / P(B). Core of Bayesian updates and diagnostic tests."),
        ("Common Distributions", "MUST", "Bernoulli/Binomial (binary events), Poisson (counts per time interval), Uniform (equal probabilities), Normal (Gaussian bells), Exponential (time between events)."),
        ("Central Limit Theorem (CLT)", "MUST", "Crucial theorem: The distribution of sample means approaches normal as sample size N grows, regardless of parent distribution shape.")
    ]
    for name, level, desc in prob_dist:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # Inferential Statistics
    story.append(Paragraph("Inferential Statistics &amp; Hypothesis Testing", h1_style))
    story.append(Paragraph("Drawing conclusions about populations from sample observations under probabilistic limits.", body_style))
    
    inferential_topics = [
        ("Confidence Intervals", "MUST", "Range estimating a population parameter with a confidence level (e.g. 95%). Width decays as sample size increases."),
        ("Hypothesis Testing & p-Values", "MUST", "Null Hypothesis (H0) vs. Alternative (H1). p-value: probability of observing sample statistics as extreme as collected, assuming H0 is true."),
        ("Errors & Power (Type I, Type II)", "MUST", "Type I error (&alpha;): rejecting H0 when true (false positive). Type II error (&beta;): retaining H0 when false (false negative). Statistical Power (1-&beta;): probability of correctly rejecting a false H0.")
    ]
    for name, level, desc in inferential_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Statistical Tests Guide", h2_style))
    
    # Statistical Tests Table
    test_table_data = [
        [Paragraph("<b>Test Name</b>", th_style), Paragraph("<b>When to Use</b>", th_style), Paragraph("<b>Assumptions</b>", th_style), Paragraph("<b>Common Pitfall</b>", th_style)],
        [Paragraph("t-test (1-sample, 2-sample, paired)", td_style), Paragraph("Compare means of 1 or 2 groups when population variance is unknown.", td_style), Paragraph("Normal distribution of groups, equal variances (independent t-test).", td_style), Paragraph("Using it on highly skewed, small datasets without non-parametric backups.", td_style)],
        [Paragraph("ANOVA (One-Way / Two-Way)", td_style), Paragraph("Compare means across 3 or more independent groups.", td_style), Paragraph("Normality, homogeneity of variances, independence.", td_style), Paragraph("Running multiple t-tests instead of ANOVA, inflating Type I error rate.", td_style)],
        [Paragraph("Chi-Square Test of Independence", td_style), Paragraph("Compare relationships between 2 categorical variables.", td_style), Paragraph("Expected counts in each cell &ge; 5, independent observations.", td_style), Paragraph("Applying to continuous variables or small sample sizes.", td_style)],
        [Paragraph("Mann-Whitney U Test", td_style), Paragraph("Compare distributions of 2 groups when normality fails (non-parametric t-test).", td_style), Paragraph("Ordinal or continuous data, independent samples.", td_style), Paragraph("Interpreting it as a direct comparison of means (it compares ranks).", td_style)],
        [Paragraph("Kruskal-Wallis Test", td_style), Paragraph("Compare distributions across 3+ groups when normality fails (non-parametric ANOVA).", td_style), Paragraph("Ordinal or continuous data, independent samples.", td_style), Paragraph("Failing to perform post-hoc Dunn's tests to locate which groups differ.", td_style)]
    ]
    t_tests = Table(test_table_data, colWidths=[100, 140, 134, 130])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tests)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 2 ------------------
    story.append(Paragraph("Stage 2 — SQL", h1_style))
    story.append(Paragraph("The language of database queries. Essential for extracting and processing structured datasets.", body_style))
    
    sql_roadmap = [
        ("Aggregations & Grouping", "MUST", "GROUP BY, HAVING, and aggregations (COUNT, SUM, AVG, MIN, MAX). Remember: HAVING filters aggregated groups; WHERE filters raw rows."),
        ("Subqueries & CTEs", "MUST", "Common Table Expressions (WITH queries) and nested subqueries. CTEs are preferred for readability and optimization structures."),
        ("Window Functions & Ranking", "MUST", "ROW_NUMBER(), RANK(), DENSE_RANK(), and partitions (`OVER(PARTITION BY ... ORDER BY ...)`). Crucial for filtering Top N entries per group."),
        ("LEAD & LAG operations", "MUST", "Retrieving values from preceding (LAG) or succeeding (LEAD) rows. Crucial for calculating session durations and step conversion differences."),
        ("Query Optimization", "SHOULD", "Reducing read times using index joins, avoiding SELECT *, avoiding Cartesian joins, and utilizing CTE boundaries effectively.")
    ]
    for name, level, desc in sql_roadmap:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Advanced SQL Interview Problem Example", h2_style))
    story.append(Paragraph(
        "<b>Problem:</b> Given a table of user log-ins `user_logins (user_id, login_time)`, find users who logged in 3 or more consecutive days.", body_style
    ))
    # Code block for consecutive days query
    consec_query = (
        "WITH unique_dates AS (\n"
        "    SELECT DISTINCT user_id, CAST(login_time AS DATE) AS login_date\n"
        "    FROM user_logins\n"
        "),\n"
        "ranked_dates AS (\n"
        "    SELECT user_id, login_date,\n"
        "           ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_date) AS rn\n"
        "    FROM unique_dates\n"
        "),\n"
        "grouped_dates AS (\n"
        "    SELECT user_id,\n"
        "           login_date - INTERVAL '1 day' * rn AS group_date\n"
        "    FROM ranked_dates\n"
        ")\n"
        "SELECT user_id\n"
        "FROM grouped_dates\n"
        "GROUP BY user_id, group_date\n"
        "HAVING COUNT(*) >= 3;"
    )
    story.append(make_code_block(consec_query, code_style))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 3 ------------------
    story.append(Paragraph("Stage 3 — Data Cleaning", h1_style))
    story.append(Paragraph("Garbage in, garbage out. Cleanse data to ensure modeling pipelines receive high-quality inputs.", body_style))
    
    stage3_topics = [
        ("Missing Data Types", "MUST", "1) MCAR (Missing Completely at Random): missingness independent of variables. Impute safely. 2) MAR (Missing at Random): missingness depends on observed features. Impute using conditional rules. 3) MNAR (Missing Not at Random): missingness depends on unobserved values. Requires structural additions or indicator columns."),
        ("Outlier Treatment", "MUST", "Detecting outliers via IQR (clipping to [Q1 - 1.5*IQR, Q3 + 1.5*IQR]) or Z-score boundaries. Avoid dropping outliers blindly; clip (winsorization) or apply transforms first."),
        ("Inconsistent Categories & Types", "MUST", "Resolving mixed classifications (e.g. 'US', 'USA', 'United States' to 'USA') and casting column types (e.g. object to float or datetime)."),
        ("Data Quality & Leakage validation", "MUST", "Spotting duplicates, verifying input ranges, and identifying target variables data leakage (dropping features containing future target information).")
    ]
    for name, level, desc in stage3_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 4 ------------------
    story.append(Paragraph("Stage 4 — Exploratory Data Analysis (EDA)", h1_style))
    story.append(Paragraph("Perform univariate, bivariate, and multivariate analysis to identify distribution shapes, target relationships, and anomalies.", body_style))
    
    stage4_topics = [
        ("Univariate Analysis", "MUST", "Analyzing single columns. Plot histograms to inspect skewness, box plots for outliers, and value counts for categories."),
        ("Bivariate & Multivariate Analysis", "MUST", "Analyzing two or more columns simultaneously. Use scatter plots to trace feature relationships, heatmaps for correlation coefficients, and pairplots for overall grids."),
        ("Systematic Dataset Approach", "MUST", "When given an unfamiliar dataset: 1) Check dimensions (.shape) and column data types, 2) Calculate descriptive summaries (.describe()), 3) Scan null counts (.isnull().sum()), 4) Plot target variable distribution, 5) Compute correlation heatmap with target.")
    ]
    for name, level, desc in stage4_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 5 ------------------
    story.append(Paragraph("Stage 5 — Feature Engineering", h1_style))
    story.append(Paragraph("Transforming features to improve model capacity and linear alignments.", body_style))
    
    stage5_topics = [
        ("Numerical Transformations", "MUST", "Log transformations (`np.log1p`) to reduce heavy right skewness. Power transforms (Box-Cox, Yeo-Johnson) to make distributions Gaussian."),
        ("Feature Scaling", "MUST", "StandardScaler (mean=0, std=1) for normal-behaving parameters. MinMaxScaler (scale to 0-1) for neural networks and distance algorithms. RobustScaler for outliers."),
        ("Categorical Encoding", "MUST", "One-hot encoding for low-cardinality unordered fields. Target/Mean encoding for high-cardinality fields (e.g. zip codes) to prevent dimension explosions."),
        ("Feature Selection", "SHOULD", "Reducing dimensionality via filter methods (correlations), wrapper methods (Recursive Feature Elimination), or tree-based feature importances.")
    ]
    for name, level, desc in stage5_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 6 ------------------
    story.append(Paragraph("Stage 6 — Machine Learning", h1_style))
    story.append(Paragraph("Core statistical algorithms. Focus on model assumptions, mathematical operations, and hyperparameters.", body_style))
    story.append(Spacer(1, 10))
    
    alg_story = get_algorithm_blocks(styles)
    story.extend(alg_story)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 7 ------------------
    story.append(Paragraph("Stage 7 — Model Evaluation", h1_style))
    story.append(Paragraph("Metrics selection determines model performance alignment with actual business KPIs.", body_style))
    
    stage7_topics = [
        ("Validation Strategy", "MUST", "Train/Validation/Test split. Use Stratified K-Fold cross-validation for target class imbalances. Maintain temporal splits for timeseries."),
        ("Classification Metrics", "MUST", "Accuracy (avoid on imbalanced sets), Precision (minimize false alarms), Recall (minimize missed detections), F1-Score (harmonic mean), ROC-AUC (overall ranking), PR-AUC (best for highly skewed classes)."),
        ("Probability Calibration", "SHOULD", "Ensuring predicted model probabilities match actual frequencies. Correct tree/SVM predictions via Platt Scaling or Isotonic Regression."),
        ("Bias-Variance Tradeoff", "MUST", "Bias: error from underfitting (simple model). Variance: error from overfitting (complex model, fits training noise). Solve variance via regularization or bagging.")
    ]
    for name, level, desc in stage7_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 8 ------------------
    story.append(Paragraph("Stage 8 — Experimentation &amp; A/B Testing", h1_style))
    story.append(Paragraph("Formulate experiment structures to validate feature changes and quantify business impact.", body_style))
    
    stage8_topics = [
        ("A/B Test Design", "MUST", "Control group (status quo) vs. Treatment group (feature variation). Establish randomization bounds to ensure users don't cross-contaminate."),
        ("Sample Sizing &amp; MDE", "MUST", "Determine sample size using: 1) Significance level (&alpha;, typically 0.05), 2) Statistical Power (1-&beta;, typically 0.80), 3) Minimum Detectable Effect (MDE)."),
        ("Hypothesis Validation &amp; Pitfalls", "MUST", "Calculate z-test or t-test significance on outcome KPIs. Pitfalls: Peeking (repeatedly checking p-values to stop test early, inflating Type I error), Multiple testing bias.")
    ]
    for name, level, desc in stage8_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("A/B Testing Business Scenario Example", h2_style))
    story.append(Paragraph(
        "<b>Scenario:</b> Product manager wants to test a new checkout button color. "
        "Conversion rate baseline is 5%. Target is to detect a 5% relative increase (MDE = 0.25 percentage points). "
        "With &alpha; = 0.05 and Power = 0.80, sample sizing calculation dictates approximately 250,000 users per group. "
        "Split traffic evenly. After 2 weeks, check p-value: if p &lt; 0.05, reject the null hypothesis and roll out the checkout button.", body_style
    ))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 9 ------------------
    story.append(Paragraph("Stage 9 — Business &amp; Product Analytics", h1_style))
    story.append(Paragraph("Translating qualitative business operations questions into metrics, funnels, and structured analysis.", body_style))
    
    stage9_topics = [
        ("Business Metrics &amp; KPIs", "MUST", "LTV (Customer Lifetime Value), CAC (Customer Acquisition Cost), Churn Rate (user attrition), Retention Rate, ARPU (Average Revenue Per User)."),
        ("Funnel &amp; Cohort Analysis", "MUST", "Funnel: tracking step-by-step drop-offs (e.g. Land page &rarr; Cart &rarr; Purchase). Cohort: tracking behaviors of groups sharing characteristics over time."),
        ("Translating Business to Analytics", "MUST", "When asked 'Why did revenue drop?', translate to: 1) Decompose revenue = Active Users * Conversion Rate * Average Order Value. 2) Trace which component dropped. 3) Segment by traffic source or device.")
    ]
    for name, level, desc in stage9_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 10 ------------------
    story.append(Paragraph("Stage 10 — Time Series &amp; Forecasting", h1_style))
    story.append(Paragraph("Modelling data variables indexed chronologically.", body_style))
    
    stage10_topics = [
        ("Time Series Components", "MUST", "Trend (long-term direction), Seasonality (repetitive cyclic patterns), and Noise (random variations)."),
        ("Stationarity &amp; Autocorrelation", "MUST", "Stationary: constant mean/variance over time. Test using Augmented Dickey-Fuller (ADF) test. Autocorrelation (ACF) tracks correlation with past lags."),
        ("Forecasting Models", "SHOULD", "ARIMA (p, d, q) and SARIMA (adds seasonal variables). Exponential Smoothing (Holt-Winters) models trend and seasonality exponentially.")
    ]
    for name, level, desc in stage10_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 11 ------------------
    story.append(Paragraph("Stage 11 — Advanced Data Science", h1_style))
    story.append(Paragraph("Advanced modeling techniques for causal tracking, survivorship, and text analytics.", body_style))
    
    stage11_topics = [
        ("Causal Inference", "ADVANCED", "Moving from correlation to causation. Focus on randomized controlled trials, matching methods, and difference-in-differences (DiD) designs."),
        ("Survival Analysis", "ADVANCED", "Analyzing time-to-event data (e.g. time until customer churns). Focus on Kaplan-Meier curves and Cox Proportional Hazards models."),
        ("Recommendation Systems", "SHOULD", "Collaborative Filtering (Matrix Factorization/SVD), content-based recommenders, and evaluation metrics (Precision@K, NDCG)."),
        ("Natural Language Processing (NLP)", "SHOULD", "Processing text data. Focus on TF-IDF word vectors, sentiment parsing, and transformer embeddings for textual feature columns.")
    ]
    for name, level, desc in stage11_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 12 ------------------
    story.append(Paragraph("Stage 12 — Data Science Engineering", h1_style))
    story.append(Paragraph("ETL pipeline construction, Docker containers, API serving, and performance monitoring.", body_style))
    
    stage12_topics = [
        ("ETL/ELT Pipelines", "MUST", "Extract-Transform-Load. Structuring automated pipelines to ingest database records, clean observations, and save model ready tables."),
        ("APIs &amp; Containerization", "MUST", "FastAPI/Flask to build endpoints exposing models. Docker containers to package dependencies and guarantee scaling stability."),
        ("Tracking &amp; Monitoring", "SHOULD", "Using MLflow or Weights &amp; Biases for experiment tracking. Monitoring deployments for concept drift and performance decay.")
    ]
    for name, level, desc in stage12_topics:
        story.append(Paragraph(f"<b>{escape_and_format(name)}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 13 ------------------
    story.append(Paragraph("Stage 13 — 20 Progression Projects", h1_style))
    story.append(Paragraph("Building portfolio impact by resolving business-oriented and model accuracy problems.", body_style))
    story.append(Spacer(1, 6))
    
    # 5 Beginner Projects
    story.append(Paragraph("Level 1 — Beginner Projects (5 Projects)", h2_style))
    beg_projects = [
        "1. House Price Regressor (Boston/Ames dataset - Linear/Ridge, baseline MSE)",
        "2. Iris Species Classifier (Iris dataset - Logistic Regression/KNN, multi-class metrics)",
        "3. Titanic Survival Classifier (Titanic dataset - Decision Trees, categorical imputations)",
        "4. Customer segmentation (K-Means, silhouette plotting on store user transactions)",
        "5. Wine Quality Classifier (Wine dataset - Random Forest classifier, scaling comparison)"
    ]
    for p in beg_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))
    
    # 5 Intermediate Projects
    story.append(Paragraph("Level 2 — Intermediate Projects (5 Projects)", h2_style))
    int_projects = [
        "1. Credit Card Default Predictor (Kaggle - XGBoost/GBDT, class weight adjustments, PR-AUC)",
        "2. E-Commerce Customer Cohort Analytics (Retail logs - Pandas cohort matrices, retention visualization)",
        "3. Store Sales Time Series Forecaster (Store sales - ARIMA/SARIMA, lag feature engineering)",
        "4. Movie Recommendation Engine (MovieLens - Matrix Factorization SVD, NDCG metrics)",
        "5. Email Spam Classifier (Text emails - Naive Bayes + TF-IDF vectorizers)"
    ]
    for p in int_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))

    # 5 Advanced Projects
    story.append(Paragraph("Level 3 — Advanced Projects (5 Projects)", h2_style))
    adv_projects = [
        "1. Real-Time Transaction Fraud Detector (FastAPI + Docker + LightGBM + Drift Monitoring)",
        "2. Clinical Patient Survival Predictor (Cox Proportional Hazard, Kaplan-Meier curves)",
        "3. Search Query Auto-Complete Engine (Trie trees index, prefix search lookups)",
        "4. Dynamic Pricing Engine (Bayesian optimization, demand-based pricing)",
        "5. Document Semantic Search Engine (BERT embeddings + Cosine similarity indexes)"
    ]
    for p in adv_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
    story.append(Spacer(1, 8))

    # 5 Business/Product Oriented Projects
    story.append(Paragraph("Level 4 — Business &amp; Product Projects (5 Projects)", h2_style))
    bus_projects = [
        "1. A/B Testing Button Redesign Pipeline (MDE sizing, p-value calculations, power checks)",
        "2. Customer Churn Economic Impact Modeller (Classifier + Revenue savings optimization matrices)",
        "3. Marketing Attribution Modeller (Markov chains, attribution path conversions)",
        "4. SaaS Product Funnel Optimization (Drop-off tracking, conversion optimization rates)",
        "5. Store Inventory Allocation Optimization (Linear Programming, cost-demand modeling)"
    ]
    for p in bus_projects:
        story.append(Paragraph(f"&bull; {p}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 14 ------------------
    story.append(Paragraph("Stage 14 — Interview Preparation", h1_style))
    story.append(Paragraph("Practicing case studies and data interpretation questions to demonstrate analytical strength.", body_style))
    story.append(Spacer(1, 10))
    
    questions = [
        ("Python & SQL: Find User Retention", "Write an SQL query to retrieve the percentage of users who logged in during Month 1 and returned in Month 2."),
        ("Statistics: When does Central Limit Theorem fail?", "CLT assumes independent and identically distributed (i.i.d.) variables with finite variance. It fails on heavy-tailed distributions (like Cauchy) with infinite variance."),
        ("Probability: Describe Bayes Theorem diagnostic checks.", "Used to calculate posterior probability of a disease given positive test: P(D|+) = P(+|D)*P(D) / [P(+|D)*P(D) + P(+|no D)*P(no D)]. Shows how base rates matter."),
        ("ML Case Study: Design a ride-sharing ETA model.", "Decompose into: 1) Business Problem (customer cancellation from inaccurate ETAs). 2) Features (hour of day, driver location, historical route speed). 3) Model (XGBoost Regressor). 4) Metrics (RMSE, MAPE)."),
        ("A/B Testing: How do you handle a flat A/B test?", "If button conversion change is not significant (p &ge; 0.05): 1) Accept Null Hypothesis. 2) Check segmentation (e.g. mobile vs. web, maybe it worked for a sub-demographic). 3) Conduct post-mortem check on sample size.")
    ]
    for q, ans in questions:
        story.append(Paragraph(f"<b>Q: {q}</b>", h3_style))
        story.append(Paragraph(ans, body_style))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ TIMELINES ------------------
    story.append(Paragraph("Recommended Timeline Plans &amp; Checklists", h1_style))
    story.append(Paragraph("Structured timetables designed for data science career progression.", body_style))
    story.append(Spacer(1, 10))
    
    # Table of Roadmaps
    timeline_data = [
        [Paragraph("<b>Duration</b>", th_style), Paragraph("<b>Target Focus</b>", th_style), Paragraph("<b>Weekly Milestones</b>", th_style)],
        [Paragraph("3-Month Plan", td_style), Paragraph("Core Analytics &amp; SQL", td_style), Paragraph("Month 1: Python, SQL aggregations, Pandas joins. Month 2: Descriptive stats, probability, t-tests, ANOVA. Month 3: EDA visualizations and 5 Beginner projects.", td_style)],
        [Paragraph("6-Month Plan", td_style), Paragraph("ML &amp; Evaluation", td_style), Paragraph("Months 1-3: Core analytics foundations. Month 4: Supervised ML (Linear/Logistic, XGBoost), PCA. Month 5: Model evaluations (ROC/PR-AUC), calibration. Month 6: 5 Intermediate projects.", td_style)],
        [Paragraph("12-Month Plan", td_style), Paragraph("Production &amp; A/B Testing", td_style), Paragraph("Months 1-6: ML and analytics foundations. Month 7-8: A/B testing design, statistical power, MDE calculations. Month 9-10: Causal inference, survival, FastAPI pipelines. Month 11: 5 Advanced + 5 Business projects. Month 12: Case study preparation.", td_style)]
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
    
    story.append(Paragraph("Final Data Science Specialist Checklist", h2_style))
    checklist_items = [
        "Can explain the difference between t-test, ANOVA, and Chi-Square tests.",
        "Can write SQL queries utilizing window ranking functions and consecutive session offsets.",
        "Knows when to prioritize PR-AUC over ROC-AUC for imbalanced datasets.",
        "Can design an A/B test, calculate sample size requirements, and check significance.",
        "Understand the difference between MCAR, MAR, and MNAR missing data types.",
        "Can decompose business metrics (e.g. churn) into clear features and analytical target columns.",
        "Has implemented and documented at least one production-grade, API-deployed machine learning model."
    ]
    for item in checklist_items:
        story.append(Paragraph(f"[  ] {item}", bullet_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Data Science career roadmap PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
