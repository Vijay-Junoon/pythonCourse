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
        self.drawString(54, 750, "MACHINE LEARNING SPECIALIST ROADMAP")
        self.setFont("Helvetica", 8)
        self.drawRightString(612 - 54, 750, "Complete Learning & Career Guide")
        
        # Header Line Separator
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Running Footer
        self.drawString(54, 40, "Confidential — Personal Study & Career Guide")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 40, page_text)
        
        # Footer Line Separator
        self.line(54, 52, 612 - 54, 52)
        self.restoreState()

def escape_and_format(text):
    """
    Escapes HTML entities and parses inline markdown:
    - **bold** to <b>bold</b>
    - *italic* to <i>italic</i>
    - `code` to courier font
    """
    text = html.escape(text)
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
        label = "<b><font color=\"#319795\">[ADVANCED / OPTIONAL]</font></b> "

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
    Formats a python code block with a light gray background.
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
    Returns list of Flowables for each of the 12 algorithms in Stage 3.
    """
    h2_style = styles['Heading2Style']
    body_style = styles['BodyStyle']
    code_style = styles['CodeBlockStyle']
    
    # 1. Linear Regression
    lr = [
        Paragraph("1. Linear Regression", h2_style),
        create_callout_box("Foundational algorithm for continuous target prediction.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Modeling a linear relationship between features and target by fitting a straight line that minimizes distance to the actual data points.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> $y = \\mathbf{w}^T\\mathbf{x} + b$, where $\\mathbf{w}$ represents weights and $b$ represents bias.", body_style),
        Paragraph("<b>3. Objective Function:</b> Mean Squared Error (MSE): $\\text{MSE} = \\frac{1}{N} \\sum_{i=1}^N (y_i - (\\mathbf{w}^T\\mathbf{x}_i + b))^2$.", body_style),
        Paragraph("<b>4. Training Process:</b> Optimization via Gradient Descent (iterative updates) or Ordinary Least Squares (OLS) closed-form solver: $\\mathbf{w} = (X^T X)^{-1} X^T y$.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `fit_intercept` (bool), L1/L2 regularization parameters if using Ridge/Lasso.", body_style),
        Paragraph("<b>6. Advantages:</b> Simple, highly interpretable, fast training, no tuning needed.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Assumes linear relations, sensitive to outliers and multicollinearity.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Underfits severely on non-linear or highly complex data.", body_style),
        Paragraph("<b>9. When to Use:</b> For simple regression baselines with linear relationships.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>What are the core assumptions of OLS Linear Regression?</i> (Linearity, Homoscedasticity, Independence, Normality of residuals).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)", code_style),
        Spacer(1, 12)
    ]
    
    # 2. Polynomial Regression
    pr = [
        Paragraph("2. Polynomial Regression", h2_style),
        create_callout_box("Extends linear models to fit curves.", "SHOULD", styles),
        Paragraph("<b>1. Intuition:</b> Fits a non-linear curve by transforming linear features into polynomial combinations (e.g., squaring or cubing inputs) and applying a linear model.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> $y = w_0 + w_1 x + w_2 x^2 + ... + w_d x^d$.", body_style),
        Paragraph("<b>3. Objective Function:</b> Mean Squared Error (MSE).", body_style),
        Paragraph("<b>4. Training Process:</b> Transforms features using `PolynomialFeatures` followed by training standard Linear Regression (OLS or Gradient Descent).", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `degree` (degree of polynomial expansion), `interaction_only`.", body_style),
        Paragraph("<b>6. Advantages:</b> Models curved relationships without discarding simple linear framework.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Prone to severe overfitting at high degrees, poor extrapolation behavior.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Extrapolating beyond training data ranges leads to erratic predictions.", body_style),
        Paragraph("<b>9. When to Use:</b> When a curved relationship is visible but dataset dimensions are low.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>Why is Polynomial Regression still considered a 'linear' model?</i> (Because the parameters/weights $\\mathbf{w}$ enter the equation linearly).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.linear_model import LinearRegression\npoly = PolynomialFeatures(degree=2)\nX_poly = poly.fit_transform(X)\nmodel = LinearRegression().fit(X_poly, y)", code_style),
        Spacer(1, 12)
    ]

    # 3. Logistic Regression
    logr = [
        Paragraph("3. Logistic Regression", h2_style),
        create_callout_box("The foundational baseline for binary and multi-class classification.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Predicts probability of membership in a class using the Sigmoid (logistic) function, outputting a value between 0 and 1.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> $p = \\sigma(\\mathbf{w}^T\\mathbf{x} + b) = \\frac{1}{1 + e^{-(\\mathbf{w}^T\\mathbf{x} + b)}}$.", body_style),
        Paragraph("<b>3. Objective Function:</b> Binary Cross-Entropy (Log Loss): $L = -\\frac{1}{N} \\sum [y_i \\log(p_i) + (1 - y_i)\\log(1 - p_i)]$.", body_style),
        Paragraph("<b>4. Training Process:</b> Maximum Likelihood Estimation optimized using gradient descent or coordinate descent.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `C` (inverse regularization strength), `penalty` ('l1', 'l2', 'elasticnet'), `solver` ('lbfgs', 'saga').", body_style),
        Paragraph("<b>6. Advantages:</b> Extremely fast, outputs calibrated probabilities, easy to regularize, interpretable weights.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Assumes linear decision boundary, struggles with complex relationships.", body_style),
        Paragraph("<b>8. Failure Cases:</b> High-dimensional non-linear boundaries cause low accuracy.", body_style),
        Paragraph("<b>9. When to Use:</b> As a first baseline model for classification tasks.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>Why is MSE not used as a loss function in Logistic Regression?</i> (It makes the optimization problem non-convex, leading to many local minima).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression(C=1.0, penalty='l2')\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 4. K-Nearest Neighbors (KNN)
    knn = [
        Paragraph("4. K-Nearest Neighbors (KNN)", h2_style),
        create_callout_box("Instance-based non-parametric classifier.", "SHOULD", styles),
        Paragraph("<b>1. Intuition:</b> Classifies a data point based on the majority vote of its $k$ closest neighbors in feature space.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Euclidean distance: $d(\\mathbf{p}, \\mathbf{q}) = \\sqrt{\\sum (p_i - q_i)^2}$. Other metrics include Manhattan and Cosine distance.", body_style),
        Paragraph("<b>3. Objective Function:</b> No explicit global objective function to minimize; it is a lazy learner.", body_style),
        Paragraph("<b>4. Training Process:</b> Lazy training; it simply stores the training dataset. All computations occur at inference time.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `n_neighbors` ($k$), `weights` ('uniform', 'distance'), `metric` ('euclidean', 'manhattan').", body_style),
        Paragraph("<b>6. Advantages:</b> Simple, adaptive to new data, non-parametric (no assumptions about data distribution).", body_style),
        Paragraph("<b>7. Disadvantages:</b> Very slow inference on large data, memory-intensive, highly sensitive to feature scaling and noise.", body_style),
        Paragraph("<b>8. Failure Cases:</b> High dimensional datasets (due to the curse of dimensionality, distances collapse).", body_style),
        Paragraph("<b>9. When to Use:</b> For small, low-dimensional datasets where local boundaries are highly irregular.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>How does $k$ affect the bias-variance tradeoff?</i> (A small $k$ leads to low bias but high variance; a large $k$ leads to high bias but low variance).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.neighbors import KNeighborsClassifier\nmodel = KNeighborsClassifier(n_neighbors=5)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 5. Naive Bayes
    nb = [
        Paragraph("5. Naive Bayes", h2_style),
        create_callout_box("Extremely fast classifier based on conditional independence.", "SHOULD", styles),
        Paragraph("<b>1. Intuition:</b> Classifies text or categorical vectors using Bayes' Theorem, making the 'naive' assumption that all features are independent given the class.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> $P(y|\\mathbf{x}) \\propto P(y) \\prod_{i=1}^d P(x_i|y)$.", body_style),
        Paragraph("<b>3. Objective Function:</b> Maximum a Posteriori (MAP) decision rule.", body_style),
        Paragraph("<b>4. Training Process:</b> Simply counting feature frequencies under each class to compute prior and likelihood probabilities.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `alpha` (additive Laplace smoothing parameter).", body_style),
        Paragraph("<b>6. Advantages:</b> Extremely fast, performs well with small datasets and high dimensions (e.g., text document categorization).", body_style),
        Paragraph("<b>7. Disadvantages:</b> Feature independence assumption is almost never true in real data.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Highly correlated features degrade performance significantly.", body_style),
        Paragraph("<b>9. When to Use:</b> Text classification baselines (e.g., spam detection, sentiment analysis).", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>What is Laplace smoothing and why is it needed?</i> (It avoids the 'zero probability' problem by adding a small value $\\alpha$ to count frequencies).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.naive_bayes import MultinomialNB\nmodel = MultinomialNB(alpha=1.0)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 6. Decision Trees
    dt = [
        Paragraph("6. Decision Trees", h2_style),
        create_callout_box("Highly interpretable rule-based model.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Splitting data recursively using simple decision rules (e.g., if age > 30) that maximize separation between classes.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Splitting criteria: Gini Impurity: $1 - \\sum p_i^2$, or Entropy: $-\\sum p_i \\log_2 p_i$.", body_style),
        Paragraph("<b>3. Objective Function:</b> Maximizing Information Gain (reduction in Gini/Entropy) at each split.", body_style),
        Paragraph("<b>4. Training Process:</b> Greedy search to find the feature and split threshold that maximizes information gain, recursively partitioning data until stopping criteria are met.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `max_depth`, `min_samples_split`, `min_samples_leaf`, `criterion` ('gini', 'entropy').", body_style),
        Paragraph("<b>6. Advantages:</b> Highly interpretable, no feature scaling needed, handles missing values and non-linearities.", body_style),
        Paragraph("<b>7. Disadvantages:</b> High variance, extremely prone to overfitting, unstable (small data changes change the tree entirely).", body_style),
        Paragraph("<b>8. Failure Cases:</b> Diagonal decision boundaries (trees only make axis-aligned splits).", body_style),
        Paragraph("<b>9. When to Use:</b> When model interpretability is paramount or as base estimators in ensembles.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>How does pruning prevent overfitting in decision trees?</i> (It cuts back branches that provide little predictive power, reducing tree complexity and variance).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=5)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 7. Random Forest
    rf = [
        Paragraph("7. Random Forest", h2_style),
        create_callout_box("Robust ensemble model using bagging of independent decision trees.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Aggregates a large number of independent, deep decision trees trained on random bootstrap samples of data and random subsets of features.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Bootstrap Aggregating (Bagging) + Subspace Sampling. Variance reduces by a factor of $M$ if models are uncorrelated.", body_style),
        Paragraph("<b>3. Objective Function:</b> Minimizing overall variance without increasing bias.", body_style),
        Paragraph("<b>4. Training Process:</b> Generates $M$ bootstrap samples of the training set, trains a deep decision tree on each (choosing from a random subset of features at each split node), and averages their predictions.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `n_estimators`, `max_features`, `max_depth`, `min_samples_leaf`, `bootstrap` (bool).", body_style),
        Paragraph("<b>6. Advantages:</b> Very robust, avoids overfitting, handles high dimensionality, provides feature importance.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Slower inference, large memory footprint, acts as a 'black box' compared to a single tree.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Extrapolation (cannot predict values outside the range of training targets).", body_style),
        Paragraph("<b>9. When to Use:</b> General purpose classification and regression on tabular data.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>Why does Random Forest select a random subset of features at each split?</i> (It decorrelates the trees, making their average much more effective at reducing variance).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 8. Gradient Boosting (GBDT)
    gbdt = [
        Paragraph("8. Gradient Boosting (GBDT)", h2_style),
        create_callout_box("Sequential boosting of decision trees.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Trains weak decision trees sequentially, where each new tree is trained to predict the residual errors (gradients) of the ensemble up to that point.", body_style),
        Paragraph(r"<b>2. Mathematical Idea:</b> $F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$, performing gradient descent in function space.", body_style),
        Paragraph("<b>3. Objective Function:</b> Any differentiable loss function (e.g., MSE for regression, log-loss for classification).", body_style),
        Paragraph("<b>4. Training Process:</b> Computes pseudo-residuals, fits a shallow tree to these residuals, computes optimal step size, updates ensemble, and repeats.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `learning_rate` (shrinkage), `n_estimators`, `max_depth`, `subsample`.", body_style),
        Paragraph("<b>6. Advantages:</b> Top-tier predictive accuracy on tabular data, handles various loss functions.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Slow training (sequential), prone to overfitting if hyperparameters are not tuned properly.", body_style),
        Paragraph("<b>8. Failure Cases:</b> High levels of noise in the target variable can lead to rapid overfitting.", body_style),
        Paragraph("<b>9. When to Use:</b> High-stakes regression or classification on tabular datasets.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>What is the relationship between learning rate and n_estimators in GBDT?</i> (They are inversely related: a lower learning rate requires a higher number of estimators for the same capacity).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.ensemble import GradientBoostingClassifier\nmodel = GradientBoostingClassifier(learning_rate=0.1, n_estimators=100)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 9. XGBoost
    xgb = [
        Paragraph("9. XGBoost (eXtreme Gradient Boosting)", h2_style),
        create_callout_box("Highly optimized, industry-standard GBDT library.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> A highly optimized GBDT version featuring parallel tree building, regularized objective functions, and hardware-accelerated processing.", body_style),
        Paragraph(r"<b>2. Mathematical Idea:</b> Taylor series expansion of objective: $L^{(t)} \approx \sum [g_i f_t(x_i) + \frac{1}{2}h_i f_t^2(x_i)] + \gamma T + \frac{1}{2}\lambda \sum w_j^2$.", body_style),
        Paragraph("<b>3. Objective Function:</b> Loss function plus L1/L2 regularization terms on leaf weights and number of leaves.", body_style),
        Paragraph("<b>4. Training Process:</b> Grows trees level-wise, utilizing a fast histogram-based split finder and weighted quantile sketches.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `eta` (learning_rate), `max_depth`, `lambda` (L2 regularization), `alpha` (L1 regularization), `subsample`, `colsample_bytree`.", body_style),
        Paragraph("<b>6. Advantages:</b> Parallel processing, built-in missing value handling, native L1/L2 regularization, exceptional performance.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Many hyperparameters to tune, complex black-box model, memory intensive.", body_style),
        Paragraph("<b>8. Failure Cases:</b> High-dimensional sparse text data (where Naive Bayes or sparse linear models are faster).", body_style),
        Paragraph("<b>9. When to Use:</b> Standard choice for competitive machine learning and production systems on tabular data.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>How does XGBoost handle missing values during training?</i> (It automatically assigns a default direction for missing values at each split node based on which path minimizes loss).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("import xgboost as xgb\nmodel = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 10. LightGBM
    lgb = [
        Paragraph("10. LightGBM (Light Gradient Boosting Machine)", h2_style),
        create_callout_box("Ultrafast boosting framework optimized for large datasets.", "MUST", styles),
        Paragraph("<b>1. Intuition:</b> Employs histogram-based algorithms, leaf-wise growth, and sampling techniques to train orders of magnitude faster with less memory.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB) to reduce data volume and feature size.", body_style),
        Paragraph("<b>3. Objective Function:</b> Regularized loss function (similar to XGBoost).", body_style),
        Paragraph("<b>4. Training Process:</b> Grows trees leaf-wise (splitting on leaves with maximum loss reduction) instead of depth/level-wise.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `num_leaves`, `max_depth`, `learning_rate`, `min_data_in_leaf`, `feature_fraction`.", body_style),
        Paragraph("<b>6. Advantages:</b> Extremely fast training, highly memory efficient, natively handles massive datasets.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Leaf-wise growth can cause severe overfitting on small datasets ($<10,000$ samples) if parameters aren't tuned.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Very small datasets where high capacity causes rapid overfitting.", body_style),
        Paragraph("<b>9. When to Use:</b> Large-scale tabular datasets (millions of rows) where training speed is a major bottleneck.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>Compare leaf-wise and level-wise tree growth.</i> (Level-wise grows the entire tree level by level; leaf-wise splits only the single leaf with the highest loss reduction, resulting in deeper, asymmetrical trees).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("import lightgbm as lgb\nmodel = lgb.LGBMClassifier(num_leaves=31, learning_rate=0.05)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]

    # 11. CatBoost
    cat = [
        Paragraph("11. CatBoost (Categorical Boosting)", h2_style),
        create_callout_box("Handles categorical variables out-of-the-box without manual preprocessing.", "SHOULD", styles),
        Paragraph("<b>1. Intuition:</b> Solves target leakage and prediction shift using Ordered Boosting and uses Symmetric Trees for fast, stable prediction.", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Ordered Target Statistics (calculating categorical target values using random permutations to prevent leakage).", body_style),
        Paragraph("<b>3. Objective Function:</b> Regularized loss function (cross-entropy or custom).", body_style),
        Paragraph("<b>4. Training Process:</b> Randomly permutes data to encode categorical columns, and builds symmetric trees (where split criteria are identical across each level).", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `iterations`, `learning_rate`, `depth`, `l2_leaf_reg`, `cat_features` (list of indices).", body_style),
        Paragraph("<b>6. Advantages:</b> Outstanding out-of-the-box performance, native categorical column handling, extremely fast inference.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Slower training speeds compared to LightGBM on purely numerical datasets.", body_style),
        Paragraph("<b>8. Failure Cases:</b> High dimensional text sparse datasets.", body_style),
        Paragraph("<b>9. When to Use:</b> Tabular datasets with many categorical columns (e.g., user profiles, zip codes).", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>What is prediction shift in boosting and how does CatBoost solve it?</i> (Traditional boosting uses the same data to calculate gradients and fit trees, causing bias. CatBoost uses ordered permutations so the gradient estimate of a sample uses only historical data).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("import catboost as cb\nmodel = cb.CatBoostClassifier(iterations=100, depth=6)\nmodel.fit(X_train, y_train, cat_features=[0, 3])", code_style),
        Spacer(1, 12)
    ]

    # 12. Support Vector Machines (SVM)
    svm = [
        Paragraph("12. Support Vector Machines (SVM)", h2_style),
        create_callout_box("Finds the optimal separating hyperplane that maximizes the class margin.", "SHOULD", styles),
        Paragraph("<b>1. Intuition:</b> Fits a decision boundary that maximizes the distance (margin) between the boundary and the closest data points of each class (support vectors).", body_style),
        Paragraph("<b>2. Mathematical Idea:</b> Kernel Trick: $K(x, z) = \\phi(x)^T\\phi(z)$ computes dot products in high-dimensional spaces implicitly.", body_style),
        Paragraph("<b>3. Objective Function:</b> Margin maximization with soft-margin hinge loss: $\\min \\frac{1}{2}||\\mathbf{w}||^2 + C \\sum \\xi_i$.", body_style),
        Paragraph("<b>4. Training Process:</b> Solving a quadratic programming optimization problem to identify support vectors.", body_style),
        Paragraph("<b>5. Hyperparameters:</b> `C` (trade-off between margin width and classification errors), `kernel` ('linear', 'rbf', 'poly'), `gamma` (kernel coefficient).", body_style),
        Paragraph("<b>6. Advantages:</b> High accuracy on complex datasets, memory efficient (only stores support vectors), performs well in high dimensions.", body_style),
        Paragraph("<b>7. Disadvantages:</b> Computationally expensive on large datasets ($O(N^3)$ complexity), no native probability outputs.", body_style),
        Paragraph("<b>8. Failure Cases:</b> Massive datasets where training time becomes prohibitive.", body_style),
        Paragraph("<b>9. When to Use:</b> Small-to-medium sized datasets with non-linear boundaries.", body_style),
        Paragraph("<b>10. Interview Question:</b> <i>What is the Kernel Trick and why is it useful?</i> (It projects data into a higher-dimensional space where classes are linearly separable, without ever computing coordinates in that high-dimensional space).", body_style),
        Paragraph("<b>11. Implementation:</b>", body_style),
        make_code_block("from sklearn.svm import SVC\nmodel = SVC(kernel='rbf', C=1.0, probability=True)\nmodel.fit(X_train, y_train)", code_style),
        Spacer(1, 12)
    ]
    
    return lr + pr + logr + knn + nb + dt + rf + gbdt + xgb + lgb + cat + svm

def build_pdf(filename="Machine_Learning_Specialist_Roadmap.pdf"):
    # Target file creation
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
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
        fontSize=20,
        leading=24,
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
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2Style',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#319795"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3Style',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=8,
        spaceAfter=4,
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
    story.append(Paragraph("Machine Learning Specialist", cover_title_style))
    story.append(Paragraph("Complete Learning &amp; Career Roadmap", cover_subtitle_style))
    
    story.append(Spacer(1, 230))
    story.append(Paragraph("Welcome to the Machine Learning Specialist Curriculum", welcome_title_style))
    story.append(Paragraph(
        "This curriculum is designed to transform individuals with basic Python proficiency "
        "into production-ready Machine Learning Specialists. It covers absolute fundamentals, "
        "core math, advanced tabular algorithms, deep evaluation frameworks, time series forecasting, "
        "and MLOps best practices. By completing this roadmap, you will gain the expertise to "
        "engineer models, build production-grade APIs, and design end-to-end ML architectures.",
        welcome_body_style
    ))
    
    story.append(Paragraph("<b>Table of Contents / Curriculum Stages:</b>", h3_style))
    stages = [
        "Stage 0 — Prerequisites (Python, NumPy, Pandas, SQL, Git)",
        "Stage 1 — Mathematics &amp; Statistics (Linear Algebra, Calculus, Probability)",
        "Stage 2 — Data Preprocessing &amp; Exploratory Data Analysis (EDA)",
        "Stage 3 — Supervised Learning (12 Essential Algorithms)",
        "Stage 4 — Unsupervised Learning (Clustering &amp; Dimensionality Reduction)",
        "Stage 5 — Model Evaluation &amp; Metrics Selection",
        "Stage 6 — Ensemble Learning (Bagging, Boosting, Stacking)",
        "Stage 7 — Advanced ML (Regularization, Calibration, Explainability)",
        "Stage 8 — Time Series Forecasting",
        "Stage 9 — ML Engineering (Pipelines, Containers, FastAPI)",
        "Stage 10 — MLOps (Deployment, Monitoring, Drift)",
        "Stage 11 — Progression Projects (Beginner to Production)",
        "Stage 12 — Interview Preparation &amp; Case Studies",
        "Recommended Timelines &amp; Specialist Checklists"
    ]
    for s in stages:
        story.append(Paragraph(f"&bull; {s}", bullet_style))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 0 ------------------
    story.append(Paragraph("Stage 0 — Prerequisites", h1_style))
    story.append(Paragraph("Establish a strong base in tools, languages, and libraries before diving into statistical modelling.", body_style))
    story.append(Spacer(1, 4))
    
    prereqs = [
        ("Python for ML", "MUST", "Core language used in modern AI. Focus on functions, OOP, and script execution.", "Comfortable writing clean scripts, implementing OOP classes, and debugging code."),
        ("NumPy", "MUST", "Underpins numerical computing. Provides optimized multi-dimensional array operations.", "Array creation, slicing, vectorization, dot products, broadcasting."),
        ("Pandas", "MUST", "The core data manipulation library. Essential for loading, cleaning, and transforming tabular data.", "Dataframe filtering, aggregations, merging/joining, pivot tables, handling datetimes."),
        ("Matplotlib & Seaborn", "MUST", "Visualization. Crucial for plotting distributions, finding correlations, and inspecting outliers.", "Scatter plots, line charts, histograms, heatmaps, box plots."),
        ("Basic SQL", "MUST", "Standard database query language. Most enterprise data starts in relational databases.", "SELECT statements, WHERE filters, GROUP BY aggregations, and inner/left JOINs."),
        ("Basic Git & GitHub", "SHOULD", "Version control is mandatory in team environments to track changes and collaborate.", "Init, clone, commit, push, pull, simple merge conflict resolution."),
        ("Jupyter Notebooks", "MUST", "The de-facto standard environment for ML prototyping, interactive coding, and EDA.", "Command/edit modes, hotkeys, markdown, executing cells."),
        ("Basic Command Line", "MUST", "Essential for running scripts, configuring environments, and interacting with Docker/Cloud.", "ls, cd, mkdir, pip install, virtual environment management (`venv` or `conda`).")
    ]
    
    for name, level, why, suff in prereqs:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(f"<b>Why it matters:</b> {why}<br/><b>Sufficient competency:</b> {suff}", level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 1 ------------------
    story.append(Paragraph("Stage 1 — Mathematics &amp; Statistics for ML", h1_style))
    story.append(Paragraph("Deepen your understanding of optimization and probability to comprehend how learning algorithms operate under the hood.", body_style))
    
    math_topics = [
        ("Linear Algebra", [
            ("Vectors and Matrices", "MUST", "Building blocks of datasets. Features are vectors; datasets are matrices."),
            ("Matrix Multiplication", "MUST", "The primary computation in neural networks, projections, and linear transformations."),
            ("Eigenvalues & Eigenvectors", "SHOULD", "Core concept in Principal Component Analysis (PCA) and spectral decomposition.")
        ]),
        ("Calculus", [
            ("Derivatives & Partial Derivatives", "MUST", "Calculates instantaneous rate of change. Essential for parameter tuning."),
            ("Gradients", "MUST", "Vector of partial derivatives pointing to maximum change. Core of gradient descent."),
            ("Chain Rule", "MUST", "Used to compute derivative of composed functions. Critical for neural backpropagation.")
        ]),
        ("Probability & Statistics", [
            ("Conditional Probability & Bayes Theorem", "MUST", "Foundational for Naive Bayes, classification heuristics, and target calculations."),
            ("Random Variables & Distributions", "MUST", "Understanding normal, binomial, and Poisson distributions helps model expectations."),
            ("Expectation, Variance, Covariance & Correlation", "MUST", "Measures the center, spread, and linear dependency between variables."),
            ("Descriptive & Inferential Statistics", "SHOULD", "Summarizing datasets vs. drawing populations conclusions from samples."),
            ("Hypothesis Testing & Confidence Intervals", "SHOULD", "Used in A/B testing, model performance validation, and significance calculations.")
        ])
    ]
    
    for category, topics in math_topics:
        story.append(Paragraph(category, h2_style))
        for topic_name, level, desc in topics:
            story.append(Paragraph(f"<b>{topic_name}</b>", h3_style))
            story.append(create_callout_box(desc, level, styles))
            story.append(Spacer(1, 4))
            
    story.append(PageBreak())
    
    # ------------------ STAGE 2 ------------------
    story.append(Paragraph("Stage 2 — Data Preprocessing &amp; Exploratory Data Analysis", h1_style))
    story.append(Paragraph("Raw data is messy. Preprocessing transforms data into input vectors compatible with ML algorithms.", body_style))
    
    preprocess_topics = [
        ("Missing Value Imputation", "MUST", "Handling gaps in data. Drop rows (if sparse) or impute (mean/median/mode for numeric; mode for categorical; KNN/Iterative Imputer for complex datasets)."),
        ("Outlier Treatment", "MUST", "Detecting anomalies using Z-score or Interquartile Range (IQR). Handle via clipping (winsorization), log transformations, or dropping (only if noise)."),
        ("Categorical Encoding", "MUST", "One-hot encoding for nominal variables without order. Label/Ordinal encoding for ordered variables. Target/Mean encoding for high cardinality (e.g., zip codes)."),
        ("Scaling & Normalization", "MUST", "Ensuring distance-based models (KNN, SVM, K-Means) and gradient descents aren't dominated by large magnitudes. Standardize (mean=0, std=1) or Normalize (scale to 0-1)."),
        ("Feature Transformations", "SHOULD", "Applying Log, Box-Cox, or Yeo-Johnson transforms to convert highly skewed distributions into Gaussian distributions."),
        ("Feature Engineering", "MUST", "Creating new predictors out of existing fields: extraction (e.g., day_of_week from datetime), aggregations, and interaction terms ($x_1 \\times x_2$)."),
        ("Feature Selection", "SHOULD", "Reducing dimensionality to fight overfitting. Use filter methods (correlation, mutual info), wrapper methods (RFE), or embedded methods (L1 Lasso, tree importances)."),
        ("Data Leakage Prevention", "MUST", "Critical error where test information bleeds into training. Fix by split-first before fitting scalers or imputers, and avoid utilizing future target values."),
        ("Data Splitting Strategies", "MUST", "Train/Validation/Test splits. Use Stratified splits for class imbalances; temporal/rolling-window splits for time-series forecasting."),
        ("Exploratory Data Analysis (EDA)", "MUST", "Visualizing features to detect skewness, multicollinearity, correlation heatmaps, class distributions, and target relationships before modelling."),
        ("Handling Class Imbalance", "MUST", "Fixing skewed distributions using SMOTE (synthetic oversampling), random downsampling, or tuning cost-sensitive model parameters (class weights).")
    ]
    
    for name, level, desc in preprocess_topics:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 3 ------------------
    story.append(Paragraph("Stage 3 — Supervised Learning", h1_style))
    story.append(Paragraph("Comprehensive deep dive into the 12 essential supervised learning algorithms. Mastery of these is required for theoretical depth and coding tests.", body_style))
    story.append(Spacer(1, 10))
    
    alg_story = get_algorithm_blocks(styles)
    story.extend(alg_story)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 4 ------------------
    story.append(Paragraph("Stage 4 — Unsupervised Learning", h1_style))
    story.append(Paragraph("Finding hidden patterns or structural representations in unlabeled datasets.", body_style))
    
    unsupervised = [
        ("K-Means Clustering", "MUST", "Partitions data into $K$ spherical clusters by iteratively updating centroids to minimize inertia (within-cluster sum of squares). Determine optimal $K$ via the Elbow Method or Silhouette Score."),
        ("Hierarchical Clustering", "SHOULD", "Builds a tree of clusters (dendrogram) using agglomerative (bottom-up) or divisive (top-down) pathways. LINKAGE criteria (Ward, complete, average) dictates merging rules."),
        ("DBSCAN Clustering", "MUST", "Density-Based Spatial Clustering of Applications with Noise. Groups points close to each other while tagging outliers in sparse regions as noise. Handles arbitrary shapes."),
        ("Gaussian Mixture Models (GMM)", "ADVANCED", "Soft clustering model representing clusters as overlapping Gaussian distributions. Optimized using Expectation-Maximization (EM) algorithm."),
        ("Principal Component Analysis (PCA)", "MUST", "Linear dimensionality reduction that projects data onto orthogonal axes (principal components) that maximize variance. Inspect the cumulative explained variance ratio."),
        ("Non-Linear Dimensionality Reduction", "SHOULD", "t-SNE and UMAP. Used to map high-dimensional manifolds to 2D/3D spaces for visual clustering (not suitable for upstream feature reduction due to information loss)."),
        ("Anomaly Detection Algorithms", "SHOULD", "Identifying outliers in data. Leverage Isolation Forest (isolates anomalies via random partitioning), One-Class SVM, or reconstruction error from Autoencoders.")
    ]
    
    for name, level, desc in unsupervised:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 5 ------------------
    story.append(Paragraph("Stage 5 — Model Evaluation", h1_style))
    story.append(Paragraph("Evaluating model performance accurately is critical to prevent overfitting and ensure real-world success.", body_style))
    
    metrics = [
        ("Confusion Matrix", "MUST", "Table layout displaying True Positives, False Positives, True Negatives, and False Negatives."),
        ("Accuracy", "MUST", "Ratio of correct predictions. Misleading on imbalanced datasets (e.g., 99% accuracy on 1% positive class)."),
        ("Precision & Recall", "MUST", "Precision: TP / (TP + FP) (minimizing false alarms). Recall: TP / (TP + FN) (minimizing missed targets)."),
        ("F1 Score & F-beta", "MUST", "F1: Harmonic mean of Precision and Recall. F-beta allows weighting precision or recall higher."),
        ("ROC-AUC & PR-AUC", "MUST", "ROC-AUC plots TPR vs FPR (good for balanced data). PR-AUC plots Precision vs Recall (best for highly imbalanced datasets)."),
        ("Log Loss", "MUST", "Measures the performance of classification outputs whose prediction is a probability value."),
        ("MAE, MSE, RMSE, R²", "MUST", "MAE: L1 distance (outlier robust). MSE: L2 distance (punishes large errors). RMSE: root of MSE (same units as target). R²: variance explained."),
        ("Cross-Validation", "MUST", "Using K-Fold or Stratified K-Fold to evaluate generalization. Stratification is mandatory for imbalanced datasets.")
    ]
    
    for name, level, desc in metrics:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Metric Selection in Real-World Scenarios", h2_style))
    
    # Scenarios Table
    table_data = [
        [Paragraph("<b>Scenario</b>", th_style), Paragraph("<b>Target Metric</b>", th_style), Paragraph("<b>Rationale</b>", th_style)],
        [Paragraph("Credit Card Fraud (0.01% positive)", td_style), Paragraph("PR-AUC / Recall", td_style), Paragraph("Recall is critical to capture all fraud instances; PR-AUC tracks performance better than ROC-AUC when negatives dominate.", td_style)],
        [Paragraph("Medical Diagnostic (Fatal Disease)", td_style), Paragraph("Recall / Sensitivity", td_style), Paragraph("False negatives are catastrophic; we must catch every sick patient, even if it leads to some false positives.", td_style)],
        [Paragraph("Spam Email Classifier", td_style), Paragraph("Precision", td_style), Paragraph("False positives (blocking a safe, critical work email) are extremely annoying. We must ensure emails flagged as spam are definitely spam.", td_style)],
        [Paragraph("Stock Price Forecasting", td_style), Paragraph("RMSE / Directional Accuracy", td_style), Paragraph("RMSE punishes large prediction errors heavily. Directional accuracy validates trend changes.", td_style)],
        [Paragraph("E-Commerce User Retention", td_style), Paragraph("F1-Score", td_style), Paragraph("Balancing promotional cost (Precision) with capturing churning users (Recall).", td_style)]
    ]
    
    t = Table(table_data, colWidths=[150, 120, 234])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    
    story.append(PageBreak())
    
    # ------------------ STAGE 6 ------------------
    story.append(Paragraph("Stage 6 — Ensemble Learning", h1_style))
    story.append(Paragraph("Combining multiple individual models to create a stronger, more generalized aggregate predictor.", body_style))
    
    ensembles = [
        ("Bagging (Bootstrap Aggregation)", "MUST", "Trains multiple independent estimators in parallel on bootstrapped subsets of training data. Reduces variance. Main example: Random Forest."),
        ("Boosting (Sequential Learning)", "MUST", "Trains estimators sequentially. Each subsequent model is trained to correct the errors/residuals of the previous models. Reduces bias. Examples: AdaBoost, GBDT, XGBoost."),
        ("Stacking (Stacked Generalization)", "SHOULD", "Trains multiple diverse base models (e.g., SVM, Random Forest, KNN). Their predictions are fed as features into a 'meta-model' (usually simple linear models) that makes the final decision."),
        ("Blending", "SHOULD", "Similar to stacking, but the meta-model is trained on predictions made on a held-out validation dataset rather than out-of-fold cross-validation folds.")
    ]
    for name, level, desc in ensembles:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 7 ------------------
    story.append(Paragraph("Stage 7 — Advanced Machine Learning", h1_style))
    story.append(Paragraph("Techniques for fine-tuning models, regularizing equations, and interpreting black-box decision models.", body_style))
    
    advanced_ml = [
        ("Regularization (L1, L2, Elastic Net)", "MUST", "L1 (Lasso) adds absolute coefficient weights penalty ($||w||_1$), inducing weight sparsity (feature selection). L2 (Ridge) adds squared weights penalty ($||w||_2^2$), shrinking weights. Elastic Net combines both."),
        ("Hyperparameter Tuning (Bayesian Optimization)", "MUST", "Moving beyond slow Grid Search and Random Search. Bayesian optimization (e.g., Optuna) builds a surrogate probability model of the objective function to select optimal hyperparameters efficiently."),
        ("Probability Calibration", "SHOULD", "Ensures output probabilities correspond to real frequencies. Calibrate uncalibrated models (e.g., SVMs, Random Forests) using Platt Scaling (sigmoid) or Isotonic Regression."),
        ("Explainable AI (SHAP & LIME)", "SHOULD", "SHAP (Shapley Additive exPlanations) utilizes cooperative game theory to explain individual feature contributions. LIME builds local surrogate linear models around specific predictions."),
        ("Interpretability Tradeoffs", "MUST", "Recognizing that simple models (Linear Regression, Decision Trees) are highly interpretable but have lower capacity, whereas ensembles (XGBoost, GBDTs) are high-capacity black boxes.")
    ]
    for name, level, desc in advanced_ml:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 8 ------------------
    story.append(Paragraph("Stage 8 — Time Series Forecasting", h1_style))
    story.append(Paragraph("Specialized models and feature transformations designed to forecast data indexed chronologically.", body_style))
    
    timeseries = [
        ("Stationarity & Statistics", "MUST", "A stationary time-series has constant mean, variance, and autocorrelation over time. Test using the Augmented Dickey-Fuller (ADF) test. Make stationary using differencing or log-scaling."),
        ("Classical Forecasting Models", "SHOULD", "Autoregressive (AR), Moving Average (MA), ARIMA, and SARIMA (adds seasonality). Exponential Smoothing (ETS) models trend and seasonality exponentially."),
        ("Feature-Based ML Forecasting", "MUST", "Converting time series to a supervised tabular format. Create lag features ($y_{t-1}$), rolling window features (e.g., 7-day mean), and calendar features (day of week, month)."),
        ("Validation & Evaluation", "MUST", "Use TimeSeriesSplit (expanding window cross-validation) to prevent target leakage from future data. Evaluate using Mean Absolute Percentage Error (MAPE) or MASE.")
    ]
    for name, level, desc in timeseries:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 9 ------------------
    story.append(Paragraph("Stage 9 — ML Engineering", h1_style))
    story.append(Paragraph("Bridging the gap between raw data science scripts and reproducible, scalable software services.", body_style))
    
    ml_engineering = [
        ("Scikit-Learn Pipelines", "MUST", "Encapsulates data transformers (scaling, imputation) and estimators into a single object. Eliminates data leakage between validation folds."),
        ("Model Serialization", "MUST", "Saving trained parameters to disk. Use Joblib or Pickle for standard Python structures; use ONNX (Open Neural Network Exchange) for cross-platform model runtimes."),
        ("Experiment Tracking (MLflow)", "SHOULD", "Logging parameters, dataset versions, training metrics, and resulting model files. Ensures experiments are reproducible across teams."),
        ("Feature Stores & Validation", "SHOULD", "Centralized repository to store and serve features consistently for training and serving (e.g., Feast). Validate data schemas using Great Expectations."),
        ("Model Serving (FastAPI)", "MUST", "Building REST APIs to expose models for prediction. Write endpoints that accept JSON inputs, validate schemas with Pydantic, and return JSON inferences."),
        ("Inference Types (Batch vs Real-time)", "MUST", "Batch: Scoring millions of rows overnight, stored in databases. Real-time: Synchronous predictions responding to a user action within milliseconds (low latency).")
    ]
    for name, level, desc in ml_engineering:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 10 ------------------
    story.append(Paragraph("Stage 10 — MLOps", h1_style))
    story.append(Paragraph("Production deployment, automated pipeline workflows, model monitoring, and continuous integration.", body_style))
    
    mlops = [
        ("Continuous Integration & Deployment (CI/CD)", "SHOULD", "Automating testing of training scripts and model prediction APIs. Automatically building and deploying validated services to staging/production."),
        ("Cloud Infrastructure", "SHOULD", "Deploying models to cloud environments. Familiarity with managed services like AWS SageMaker, GCP Vertex AI, or raw containers on AWS ECS/EKS."),
        ("Model & Data Drift Monitoring", "MUST", "Data Drift: input distribution changes ($P(X)$). Concept Drift: relationship between input and target changes ($P(Y|X)$). Model Drift: metrics (e.g. Accuracy) decay. Detect using KS-test or PSI."),
        ("Observability & Logging", "SHOULD", "Storing inputs, predictions, service latency, CPU/memory metrics, and implementing silent fail-safes and model rollback mechanisms.")
    ]
    for name, level, desc in mlops:
        story.append(Paragraph(f"<b>{name}</b>", h3_style))
        story.append(create_callout_box(desc, level, styles))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ STAGE 11 ------------------
    story.append(Paragraph("Stage 11 — Progression Projects", h1_style))
    story.append(Paragraph("Build a progressive portfolio demonstrating your ability to transition from simple notebooks to scalable production systems.", body_style))
    story.append(Spacer(1, 10))
    
    # Project 1: Beginner
    story.append(Paragraph("Project 1: House Price Predictor (Beginner)", h2_style))
    proj1_desc = (
        "<b>Problem Statement:</b> Predict real estate prices based on spatial and physical attributes.<br/>"
        "<b>Dataset:</b> Boston Housing or Ames Housing dataset.<br/>"
        "<b>ML Techniques:</b> Linear Regression, Ridge, Lasso, Simple Decision Trees.<br/>"
        "<b>Expected Skills:</b> Data cleaning, outlier clipping, feature scaling, basic metrics evaluation.<br/>"
        "<b>Technologies:</b> Python, Pandas, NumPy, Scikit-learn, Seaborn.<br/>"
        "<b>What to Implement:</b> Impute missing values, fit regression models, calculate RMSE and R².<br/>"
        "<b>What Makes it Impressive:</b> Creating custom feature combinations (e.g., price per square foot of neighborhood) and presenting structured coefficient analysis (interpreting model weights).<br/>"
        "<b>Interview Points:</b> Why did you choose Ridge over OLS? How did you handle multicollinear features?"
    )
    story.append(create_callout_box(proj1_desc, "MUST", styles))
    story.append(Spacer(1, 8))
    
    # Project 2: Intermediate
    story.append(Paragraph("Project 2: Customer Churn Classifier (Intermediate)", h2_style))
    proj2_desc = (
        "<b>Problem Statement:</b> Classify whether a customer will churn or stay based on user activity logs.<br/>"
        "<b>Dataset:</b> Telecom Churn dataset (Kaggle).<br/>"
        "<b>ML Techniques:</b> Logistic Regression, Random Forest, XGBoost.<br/>"
        "<b>Expected Skills:</b> Class imbalance handling, hyperparameter tuning, metrics trade-offs.<br/>"
        "<b>Technologies:</b> Scikit-learn, XGBoost, Optuna, Imbalanced-learn (SMOTE).<br/>"
        "<b>What to Implement:</b> Apply SMOTE, perform random search, plot Confusion Matrix, ROC-AUC, and PR-AUC.<br/>"
        "<b>What Makes it Impressive:</b> Calibrating classification probabilities, performing a cost-benefit calculation to choose the probability threshold that maximizes company revenue.<br/>"
        "<b>Interview Points:</b> How did you select your classification threshold? Why is accuracy a poor metric here?"
    )
    story.append(create_callout_box(proj2_desc, "MUST", styles))
    story.append(Spacer(1, 8))
    
    # Project 3: Advanced
    story.append(Paragraph("Project 3: E-Commerce Recommendation Engine (Advanced)", h2_style))
    proj3_desc = (
        "<b>Problem Statement:</b> Build a hybrid recommender system that suggests items to users based on history and similarity.<br/>"
        "<b>Dataset:</b> MovieLens or Amazon product reviews.<br/>"
        "<b>ML Techniques:</b> Collaborative Filtering (Matrix Factorization/SVD), Content-Based filtering, LightFM.<br/>"
        "<b>Expected Skills:</b> Sparse matrix operations, implicit feedback handling, recommendation evaluation.<br/>"
        "<b>Technologies:</b> Scipy sparse, LightFM, implicit, Pandas.<br/>"
        "<b>What to Implement:</b> SVD decomposition, user-item similarity matrix computations, Precision@K and Recall@K evaluations.<br/>"
        "<b>What Makes it Impressive:</b> Building a hybrid model combining user reviews with transaction logs, and handling the 'cold-start' problem using content features.<br/>"
        "<b>Interview Points:</b> Explain SVD math. How do you evaluate recommended items that the user hasn't seen?"
    )
    story.append(create_callout_box(proj3_desc, "SHOULD", styles))
    story.append(Spacer(1, 8))
    
    # Project 4: Production-Grade
    story.append(Paragraph("Project 4: Real-Time Fraud Detection System (Production-Grade)", h2_style))
    proj4_desc = (
        "<b>Problem Statement:</b> Build an end-to-end service that infers transaction fraud under a 50ms SLA and monitors data drift.<br/>"
        "<b>Dataset:</b> Credit Card Fraud dataset.<br/>"
        "<b>ML Techniques:</b> LightGBM Classifier, Isolation Forest.<br/>"
        "<b>Expected Skills:</b> Containerization, API serving, drift detection, low-latency prediction.<br/>"
        "<b>Technologies:</b> FastAPI, Docker, LightGBM, MLflow, EvidentlyAI/Evidently.<br/>"
        "<b>What to Implement:</b> Scikit-learn preprocessing pipeline, model deployment inside FastAPI, containerization using Docker, drift monitoring script using Evidently.<br/>"
        "<b>What Makes it Impressive:</b> Fully functional API with request schema validation (Pydantic), integrated MLflow logging, a Docker Compose script initializing API + monitoring dashboard, and proof of automated drift detection.<br/>"
        "<b>Interview Points:</b> Describe how you designed the system to meet low latency. How does your drift monitor trigger retraining?"
    )
    story.append(create_callout_box(proj4_desc, "ADVANCED", styles))
    
    story.append(PageBreak())
    
    # ------------------ STAGE 12 ------------------
    story.append(Paragraph("Stage 12 — Interview Preparation", h1_style))
    story.append(Paragraph("Deep-dive answers to core interview questions testing machine learning systems and design capabilities.", body_style))
    story.append(Spacer(1, 10))
    
    questions_list = [
        ("Why does regularization work?",
         "Regularization works by adding a penalty to the loss function that discourages model coefficients from growing too large. "
         "L1 (Lasso) adds an absolute weight penalty ($||w||_1$), forcing insignificant weights to zero (creating sparse feature models). "
         "L2 (Ridge) adds a squared weight penalty ($||w||_2^2$), shrinking weights smoothly. "
         "This restricts model capacity and prevents it from fitting training noise, thereby improving generalization on unseen test data."),
        
        ("Why does XGBoost perform so well?",
         "XGBoost excels due to several innovations: "
         "1. It appends L1/L2 regularization directly to the tree objective function to restrict leaf complexity. "
         "2. It uses second-order Taylor expansion of the loss function, allowing the optimizer to use curvature information. "
         "3. It uses a fast histogram-based split finder and handles sparse data natively. "
         "4. Features are loaded into parallelized cache blocks to speed up training dramatically."),
        
        ("Explain Bias vs Variance.",
         "Bias is the error introduced by approximating real-world complex problems with simpler models (leads to underfitting). "
         "Variance is the model's sensitivity to small fluctuations in the training set (leads to overfitting on noise). "
         "The Goal: Find the sweet spot that minimizes the sum of squared bias and variance, achieving high generalization."),
        
        ("How do you handle imbalanced datasets?",
         "1. Data-level: Downsample the majority class or upsample the minority class (e.g., using SMOTE or ADASYN). "
         "2. Algorithm-level: Adjust model parameters (e.g., `class_weight='balanced'` in scikit-learn; adjusting scale_pos_weight in XGBoost). "
         "3. Metrics: Ignore accuracy. Use Precision, Recall, F1-Score, and PR-AUC to guide optimization."),
        
        ("How do you detect data leakage?",
         "1. Unusually high training and validation performance (e.g., 99.9% accuracy out-of-the-box). "
         "2. Check correlation of features with the target variable; features that update post-event (like 'churn_date' when predicting churn) must be dropped. "
         "3. Enforce strict pipeline boundaries: fit transformers (scalers, imputers) only on training splits, never on validation or global datasets."),
        
        ("How would you deploy an ML model?",
         "1. Serialize the trained model using Joblib or ONNX. "
         "2. Wrap it inside a REST API endpoint using FastAPI. "
         "3. Containerize the service using Docker to guarantee environment consistency. "
         "4. Deploy the container to cloud environments (e.g., AWS ECS or GCP Cloud Run) fronted by a Load Balancer."),
        
        ("How would you monitor a model in production?",
         "1. Track system metrics: request latency, memory, CPU load, and response error rates. "
         "2. Log inputs and outputs to track Data Drift (distribution changes in inputs) and Concept Drift (changes in prediction mapping). "
         "3. Run automated tests (e.g., Kolmogorov-Smirnov test or Population Stability Index) on input samples, triggering alerts when drift parameters breach set thresholds.")
    ]
    
    for q, ans in questions_list:
        story.append(Paragraph(f"<b>Q: {q}</b>", h3_style))
        story.append(Paragraph(ans, body_style))
        story.append(Spacer(1, 4))
        
    story.append(PageBreak())
    
    # ------------------ TIMELINES ------------------
    story.append(Paragraph("Recommended Learning Sequence &amp; Timelines", h1_style))
    story.append(Paragraph("Structured pathways designed to guide your progression depending on your timeline.", body_style))
    story.append(Spacer(1, 10))
    
    # Table of Roadmaps
    timeline_data = [
        [Paragraph("<b>Path</b>", th_style), Paragraph("<b>Target Focus</b>", th_style), Paragraph("<b>Milestones</b>", th_style)],
        [Paragraph("3-Month Plan", td_style), Paragraph("Tabular ML Foundations", td_style), Paragraph("Month 1: Prerequisites &amp; Math. Month 2: Basic preprocessing, linear models, KNN. Month 3: Decision Trees, Random Forest, model evaluation, and Project 1 &amp; 2.", td_style)],
        [Paragraph("6-Month Plan", td_style), Paragraph("Advanced Tabular &amp; Pipelines", td_style), Paragraph("Months 1-3: Tabular ML foundations. Month 4: Boosting algorithms (XGBoost, LightGBM), PCA, and clustering. Month 5: Regularization, hyperparameter tuning, pipeline orchestration. Month 6: Time-series forecasting and Project 3.", td_style)],
        [Paragraph("12-Month Plan", td_style), Paragraph("Production &amp; Engineering Role", td_style), Paragraph("Months 1-6: Advanced tabular ML. Month 7-8: Advanced optimization, explainable AI, calibration. Month 9-10: ML Engineering (FastAPI, Docker, serialization). Month 11: MLOps deployments, monitoring, and Project 4. Month 12: Interview preparation, system design, mock interviews.", td_style)]
    ]
    t_time = Table(timeline_data, colWidths=[100, 150, 254])
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
    
    story.append(Paragraph("What to Skip Initially", h2_style))
    story.append(Paragraph(
        "To avoid feeling overwhelmed, postpone these topics until you have fully mastered classical "
        "tabular ML and deployment pipelines: deep neural network architectures (CNNs, RNNs, Transformers), "
        "highly research-focused mathematical proofs, large-scale Kubernetes orchestrations, and complex "
        "reinforcement learning systems.",
        body_style
    ))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Final ML Specialist Checklist", h2_style))
    checklist_items = [
        "Can explain the bias-variance tradeoff mathematically and conceptually.",
        "Knows when to use Precision vs. Recall vs. ROC-AUC and PR-AUC.",
        "Can write data preprocessing pipelines in scikit-learn without causing data leakage.",
        "Understand internal operations, objective functions, and failure cases of the 12 key algorithms.",
        "Can package a trained model inside a Dockerized FastAPI service.",
        "Understand the distinction between data drift and concept drift and how to monitor both.",
        "Has implemented at least 1 production-grade, end-to-end ML project."
    ]
    for item in checklist_items:
        story.append(Paragraph(f"[  ] {item}", bullet_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated career roadmap PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
