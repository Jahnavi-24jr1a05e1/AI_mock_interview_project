import streamlit as st
import random
import csv
import io
from html import escape

st.set_page_config(
    page_title="AI Powered Mock Interview Performance Evaluation System",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #131d35);
    color: #f1f5f9;
}
[data-testid="stSidebar"] { background-color: #111a2e; }
h1, h2, h3 { color: #f8fafc !important; }
p, label, .stMarkdown { color: #dbe4f0; }
div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    border: 1px solid #c4b5fd;
    color: white;
}
.metric-card, .question-card {
    background: #192641;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #334466;
    margin-bottom: 12px;
}
.question-card { border-left: 5px solid #818cf8; }
.small-note { color: #a5b4cc; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# Each role and difficulty has a larger bank to reduce repetition.
QUESTION_BANK = {
    "Python Developer": {
        "Beginner": [
            ("What is the difference between a list and a tuple?", ["mutable", "immutable", "list", "tuple"], "Explain mutability and give a use case."),
            ("What is a Python dictionary?", ["key", "value", "mapping", "unique"], "Explain key-value pairs and how to access a value."),
            ("What is the purpose of a Python function?", ["def", "reusable", "parameter", "return"], "Explain how functions help reuse code."),
            ("What is exception handling in Python?", ["try", "except", "error", "exception"], "Explain how a program handles errors."),
            ("What is the difference between a variable and a constant?", ["variable", "value", "constant", "change"], "Explain whether values can be changed."),
            ("What are Python data types?", ["int", "string", "list", "type"], "Name common types and give examples."),
            ("What is the purpose of indentation in Python?", ["block", "indentation", "syntax", "code"], "Explain how indentation groups statements."),
            ("What is a module in Python?", ["module", "file", "import", "reuse"], "Explain how modules organize reusable code."),
            ("What is the difference between append() and extend()?", ["append", "extend", "element", "iterable"], "Explain how each method changes a list."),
            ("What is a loop and when would you use it?", ["loop", "iteration", "for", "while"], "Describe repeating instructions.")
        ],
        "Intermediate": [
            ("What is the difference between == and is?", ["equality", "identity", "value", "object"], "Compare values versus object identity."),
            ("Explain list comprehensions.", ["list", "iteration", "expression", "condition"], "Give an example of creating a list in one expression."),
            ("What are decorators in Python?", ["function", "wrapper", "modify", "behavior"], "Explain how a decorator adds functionality."),
            ("What is object-oriented programming?", ["class", "object", "inheritance", "encapsulation"], "Describe classes and key OOP concepts."),
            ("What is a lambda function?", ["lambda", "anonymous", "expression", "function"], "Explain short anonymous functions."),
            ("What is the difference between shallow copy and deep copy?", ["shallow", "deep", "copy", "nested"], "Explain how nested objects are copied."),
            ("What is a virtual environment?", ["environment", "dependencies", "isolate", "package"], "Explain why projects use separate environments."),
            ("What is a Python package?", ["package", "module", "init", "import"], "Explain how packages organize modules."),
            ("How does the with statement work?", ["with", "context", "resource", "cleanup"], "Explain automatic resource cleanup."),
            ("What is a generator expression?", ["generator", "yield", "lazy", "memory"], "Explain lazy value generation.")
        ],
        "Advanced": [
            ("Explain generators and the yield keyword.", ["yield", "iterator", "memory", "lazy"], "Discuss lazy evaluation and memory efficiency."),
            ("What is a context manager?", ["with", "resource", "cleanup", "enter", "exit"], "Explain safe resource management."),
            ("How does Python manage memory?", ["reference", "garbage", "allocation", "memory"], "Discuss references and garbage collection."),
            ("What is a thread compared with a process?", ["thread", "process", "memory", "concurrency"], "Compare memory sharing and execution."),
            ("What is the Global Interpreter Lock?", ["GIL", "thread", "bytecode", "parallel"], "Explain its impact on Python threads."),
            ("How do async and await work?", ["async", "await", "coroutine", "event loop"], "Explain asynchronous execution."),
            ("What is method resolution order?", ["MRO", "inheritance", "class", "order"], "Explain how Python finds inherited methods."),
            ("What is a metaclass?", ["metaclass", "class", "creation", "type"], "Explain how classes can be customized."),
            ("How would you profile a slow Python program?", ["profile", "bottleneck", "measure", "performance"], "Describe measuring before optimizing."),
            ("What are type hints used for?", ["type", "hint", "static", "annotation"], "Explain readability and tooling benefits.")
        ]
    },
    "Data Analyst": {
        "Beginner": [
            ("What is data cleaning?", ["missing", "duplicate", "incorrect", "data"], "Explain how you prepare data for analysis."),
            ("What is the difference between mean and median?", ["average", "middle", "outlier", "value"], "Explain how extreme values affect each measure."),
            ("What is a primary key in SQL?", ["unique", "identify", "record", "null"], "Explain how a table's records are identified."),
            ("What is data visualization?", ["chart", "graph", "pattern", "insight"], "Explain how charts help communicate findings."),
            ("What is a spreadsheet used for in data analysis?", ["data", "formula", "calculate", "organize"], "Describe how spreadsheets support analysis."),
            ("What is the difference between qualitative and quantitative data?", ["qualitative", "quantitative", "category", "numeric"], "Compare categories and numbers."),
            ("What is a data set?", ["collection", "records", "variables", "data"], "Describe rows and columns in a dataset."),
            ("What is a bar chart useful for?", ["bar", "category", "compare", "values"], "Explain when categories should be compared."),
            ("What are missing values?", ["missing", "null", "empty", "data"], "Explain why missing information matters."),
            ("What is a filter in a spreadsheet?", ["filter", "rows", "condition", "display"], "Explain how filters focus on relevant records.")
        ],
        "Intermediate": [
            ("What is the difference between INNER JOIN and LEFT JOIN?", ["matching", "rows", "table", "unmatched"], "Explain which rows each join returns."),
            ("How do you handle missing values in a dataset?", ["remove", "impute", "median", "missing"], "Discuss deletion and imputation."),
            ("What is correlation?", ["relationship", "variables", "positive", "negative"], "Explain direction and strength of a relationship."),
            ("What is the purpose of a pivot table?", ["summarize", "aggregate", "group", "values"], "Explain how data can be grouped and summarized."),
            ("What is normalization in data preparation?", ["scale", "range", "normalize", "features"], "Explain bringing values onto comparable scales."),
            ("What is the difference between WHERE and HAVING in SQL?", ["where", "having", "rows", "group"], "Compare filtering rows and groups."),
            ("What is conditional formatting?", ["format", "condition", "highlight", "values"], "Explain how rules highlight important values."),
            ("How would you remove duplicate records?", ["duplicate", "identify", "remove", "unique"], "Explain how to identify and handle duplicates."),
            ("What is a KPI?", ["key", "performance", "indicator", "metric"], "Explain how a KPI tracks a goal."),
            ("What is sampling in data analysis?", ["sample", "population", "subset", "representative"], "Explain why a subset may be analyzed.")
        ],
        "Advanced": [
            ("What is the difference between correlation and causation?", ["relationship", "cause", "effect", "confounding"], "Explain why association alone does not prove causality."),
            ("How would you detect outliers?", ["IQR", "z-score", "distribution", "threshold"], "Mention a statistical method and validate results."),
            ("What is a window function in SQL?", ["partition", "order", "rows", "aggregate"], "Explain calculations across related rows."),
            ("How do you validate a business KPI?", ["definition", "source", "accuracy", "consistency"], "Discuss metric definitions and data quality checks."),
            ("What is a confidence interval?", ["estimate", "range", "confidence", "population"], "Explain uncertainty around an estimate."),
            ("What is a p-value?", ["null", "hypothesis", "significance", "probability"], "Explain its role in hypothesis testing."),
            ("What is a star schema?", ["fact", "dimension", "table", "warehouse"], "Describe its use in analytical databases."),
            ("How would you investigate a sudden metric drop?", ["validate", "segment", "source", "cause"], "Check data quality, segments, and recent changes."),
            ("What is cohort analysis?", ["cohort", "group", "time", "behavior"], "Explain how groups are tracked over time."),
            ("What is the difference between ETL and ELT?", ["extract", "transform", "load", "warehouse"], "Compare where transformation occurs.")
        ]
    },
    "Web Developer": {
        "Beginner": [
            ("What is the difference between HTML, CSS, and JavaScript?", ["structure", "style", "behavior", "web"], "Explain the role of each technology."),
            ("What is responsive web design?", ["screen", "device", "media", "layout"], "Explain how a site adapts to different screen sizes."),
            ("What is an HTTP request?", ["client", "server", "request", "response"], "Describe communication between a browser and server."),
            ("What is the DOM?", ["document", "object", "tree", "elements"], "Explain how scripts access page elements."),
            ("What is the purpose of a hyperlink?", ["link", "navigate", "url", "page"], "Explain how links connect resources."),
            ("What is a CSS selector?", ["selector", "element", "style", "target"], "Explain how CSS targets elements."),
            ("What is semantic HTML?", ["semantic", "meaning", "element", "accessibility"], "Give examples of meaningful HTML elements."),
            ("What is a web browser?", ["browser", "render", "html", "page"], "Explain how a browser displays a website."),
            ("What is the difference between id and class in CSS?", ["id", "class", "unique", "multiple"], "Compare their intended uses."),
            ("What is form validation?", ["input", "validate", "error", "form"], "Explain checking user input.")
        ],
        "Intermediate": [
            ("What is a REST API?", ["http", "endpoint", "resource", "methods"], "Mention resources and HTTP methods."),
            ("What is the difference between authentication and authorization?", ["identity", "permission", "access", "user"], "Distinguish identity verification from permission."),
            ("What is the purpose of Git?", ["version", "commit", "branch", "collaboration"], "Explain tracking changes and teamwork."),
            ("What is the difference between SQL and NoSQL?", ["relational", "schema", "document", "database"], "Compare relational tables with common NoSQL models."),
            ("What is a JavaScript promise?", ["promise", "asynchronous", "resolve", "reject"], "Explain how asynchronous results are handled."),
            ("What is event bubbling?", ["event", "parent", "child", "propagation"], "Explain how events travel through elements."),
            ("What is CORS?", ["origin", "browser", "request", "permission"], "Explain cross-origin browser restrictions."),
            ("What is responsive break-point design?", ["breakpoint", "media", "screen", "layout"], "Explain how layouts change at screen widths."),
            ("What is client-side routing?", ["route", "client", "navigation", "url"], "Explain page navigation without full reloads."),
            ("What is lazy loading?", ["load", "defer", "resource", "performance"], "Explain delaying resources until needed.")
        ],
        "Advanced": [
            ("What is cross-site scripting (XSS)?", ["script", "input", "browser", "sanitize", "escape"], "Explain untrusted input and output encoding."),
            ("How does caching improve web performance?", ["store", "reuse", "latency", "request"], "Discuss avoiding repeated computation or network requests."),
            ("What is the purpose of database indexing?", ["index", "query", "search", "performance"], "Explain faster lookups and possible write overhead."),
            ("How would you debug a slow web application?", ["profile", "network", "database", "measure"], "Describe measuring performance and isolating bottlenecks."),
            ("What is content security policy?", ["policy", "script", "source", "security"], "Explain how browser resource rules reduce risk."),
            ("What is server-side rendering?", ["server", "html", "render", "client"], "Compare rendering on the server and browser."),
            ("What is a web worker?", ["worker", "background", "thread", "main"], "Explain work away from the main browser thread."),
            ("How do you prevent CSRF attacks?", ["token", "request", "cookie", "origin"], "Describe request verification protections."),
            ("What is a reverse proxy?", ["proxy", "server", "forward", "backend"], "Explain how it sits in front of application servers."),
            ("What is code splitting?", ["bundle", "split", "load", "performance"], "Explain loading application code in smaller parts.")
        ]
    },
    "AI / ML Engineer": {
        "Beginner": [
            ("What is machine learning?", ["data", "model", "learn", "prediction"], "Explain how a model learns patterns from data."),
            ("What is the difference between supervised and unsupervised learning?", ["label", "unlabeled", "training", "data"], "Compare labeled data with discovering patterns."),
            ("What is overfitting?", ["training", "generalize", "unseen", "model"], "Explain why a model can perform poorly on new data."),
            ("Why do we split data into training and testing sets?", ["train", "test", "unseen", "evaluation"], "Explain how independent evaluation estimates generalization."),
            ("What is a feature in machine learning?", ["input", "variable", "model", "data"], "Explain what information a feature provides."),
            ("What is a label in supervised learning?", ["target", "label", "example", "prediction"], "Explain the expected output for training examples."),
            ("What is classification?", ["class", "category", "prediction", "model"], "Describe predicting a category."),
            ("What is regression?", ["continuous", "value", "prediction", "model"], "Describe predicting a numeric value."),
            ("What is a dataset split?", ["training", "validation", "test", "evaluate"], "Explain the purpose of separate subsets."),
            ("What is accuracy?", ["correct", "prediction", "total", "classification"], "Explain the fraction of correct predictions.")
        ],
        "Intermediate": [
            ("What is the difference between precision and recall?", ["true positive", "false positive", "false negative", "classification"], "Explain false positives and false negatives."),
            ("What is feature engineering?", ["feature", "transform", "data", "model"], "Explain preparing useful input variables."),
            ("What is cross-validation?", ["fold", "validation", "training", "evaluation"], "Explain how multiple data splits assess model stability."),
            ("What is the purpose of regularization?", ["overfitting", "penalty", "complexity", "model"], "Explain how penalties discourage overly complex models."),
            ("What is a confusion matrix?", ["actual", "predicted", "classification", "matrix"], "Explain how it summarizes classification results."),
            ("What is class imbalance?", ["class", "distribution", "minority", "dataset"], "Explain why unequal class counts can affect training."),
            ("What is hyperparameter tuning?", ["parameter", "validation", "search", "performance"], "Explain choosing settings using validation data."),
            ("What is a baseline model?", ["baseline", "simple", "compare", "performance"], "Explain why a simple benchmark is useful."),
            ("What is dimensionality reduction?", ["features", "dimensions", "reduce", "information"], "Explain reducing feature count while retaining useful information."),
            ("What is a loss function?", ["loss", "error", "prediction", "optimize"], "Explain how model errors are measured.")
        ],
        "Advanced": [
            ("Explain gradient descent.", ["loss", "gradient", "parameter", "learning rate"], "Explain updating parameters to reduce a loss function."),
            ("What is data leakage in machine learning?", ["test", "training", "information", "leakage"], "Explain how unavailable information can produce misleading scores."),
            ("What is an embedding in natural language processing?", ["vector", "semantic", "representation", "similarity"], "Explain how text is represented numerically."),
            ("How would you monitor a deployed ML model?", ["drift", "performance", "data", "monitoring"], "Discuss changing data, quality, and prediction performance."),
            ("What is concept drift?", ["relationship", "target", "change", "monitor"], "Explain changes in the relationship between inputs and targets."),
            ("What is explainable AI?", ["explain", "prediction", "interpret", "model"], "Explain why model decisions should be interpretable."),
            ("What is a transformer architecture?", ["attention", "token", "sequence", "embedding"], "Explain attention and token representations."),
            ("What is quantization in model deployment?", ["precision", "weights", "memory", "inference"], "Explain reducing numeric precision to improve efficiency."),
            ("What is the difference between batch and online inference?", ["batch", "online", "request", "prediction"], "Compare grouped and individual predictions."),
            ("How do you evaluate a language model?", ["benchmark", "quality", "task", "metric"], "Discuss task-specific measures and human evaluation.")
        ]
    }
}

EXTRA_ROLES = [
    "Java Developer", "SQL Developer", "Full Stack Developer",
    "Cybersecurity Analyst", "Cloud / DevOps Engineer",
    "Software Tester / QA", "UI/UX Designer",
    "Digital Marketing Specialist", "Business Analyst",
    "Other / Custom Job Role"
]

CUSTOM_TEMPLATES = {
    "Beginner": [
        ("What are the main responsibilities of a {role}?", ["responsibilities", "skills", "work", "team"], "Describe the main tasks and skills needed for this role."),
        ("Which tools or technologies are commonly used by a {role}?", ["tools", "technology", "purpose", "example"], "Name relevant tools and explain how they are used."),
        ("What skills should a beginner learn for a {role}?", ["skills", "practice", "learn", "example"], "Mention important skills and how you would practise them."),
        ("How would you approach a basic task as a {role}?", ["requirements", "steps", "result", "check"], "Explain your steps from understanding the task to checking the result."),
        ("What common mistakes should a {role} avoid?", ["mistakes", "risk", "check", "quality"], "Name common mistakes and how to prevent them."),
        ("How does a {role} work with a team?", ["team", "communication", "task", "feedback"], "Explain collaboration and communication.")
    ],
    "Intermediate": [
        ("How would you solve a common problem faced by a {role}?", ["problem", "analyze", "solution", "result"], "Explain how you identify the cause, choose a solution, and check the result."),
        ("How do you choose the right tools or methods for a {role} task?", ["requirements", "tools", "tradeoff", "decision"], "Connect requirements to your choice and explain trade-offs."),
        ("Describe a project relevant to a {role} and your contribution.", ["project", "role", "challenge", "result"], "Use a clear situation, your actions, and the outcome."),
        ("How would you ensure quality and accuracy in your work as a {role}?", ["quality", "test", "review", "feedback"], "Discuss checks, testing or review, and improvements."),
        ("How would you prioritize multiple tasks as a {role}?", ["priority", "deadline", "impact", "plan"], "Explain how urgency and impact guide your plan."),
        ("How would you respond to feedback on your work as a {role}?", ["feedback", "review", "improve", "action"], "Describe how you use feedback to improve.")
    ],
    "Advanced": [
        ("How would you handle a complex, high-impact problem as a {role}?", ["impact", "root cause", "approach", "tradeoff"], "Explain prioritization, root-cause analysis, and trade-offs."),
        ("How would you measure success in a {role}?", ["metrics", "baseline", "target", "results"], "Name measurable indicators and how you would track them."),
        ("How would you improve an existing process used by a {role}?", ["baseline", "bottleneck", "improvement", "measure"], "Describe measuring the current process, finding bottlenecks, and validating improvement."),
        ("How would you explain a difficult decision to stakeholders as a {role}?", ["context", "evidence", "options", "communication"], "Explain how you present context, evidence, options, and risks."),
        ("How would you assess risks in a major project as a {role}?", ["risk", "impact", "likelihood", "mitigation"], "Explain risk assessment and mitigation."),
        ("How would you balance speed, cost, and quality as a {role}?", ["tradeoff", "cost", "quality", "priority"], "Describe how you evaluate competing constraints.")
    ]
}

def generate_role_questions(role, difficulty):
    return [
        {"q": q.format(role=role), "keywords": keywords, "hint": hint}
        for q, keywords, hint in CUSTOM_TEMPLATES[difficulty]
    ]

def normalize_bank(bank):
    return [
        {"q": q, "keywords": keywords, "hint": hint}
        for q, keywords, hint in bank
    ]

def evaluate_answer(answer, keywords):
    answer = answer.strip().lower()
    if not answer:
        return {
            "score": 0,
            "matched": [],
            "missing": keywords,
            "feedback": "No answer provided. Explain the key concepts before submitting."
        }

    matched = [word for word in keywords if word.lower() in answer]
    coverage = len(matched) / len(keywords) * 100 if keywords else 0
    word_count = len(answer.split())
    length_score = min(word_count / 50, 1) * 20
    score = round(coverage * 0.8 + length_score)
    missing = [word for word in keywords if word not in matched]

    if score >= 80:
        feedback = "Good coverage! Review technical accuracy and add a clear example."
    elif score >= 50:
        feedback = "A reasonable start. Explain more key concepts and include an example."
    else:
        feedback = "Try a structured answer: define the concept, explain how it works, and give an example."

    return {
        "score": min(score, 100),
        "matched": matched,
        "missing": missing,
        "feedback": feedback
    }

# Session state
defaults = {
    "started": False,
    "finished": False,
    "results": [],
    "questions": [],
    "index": 0,
    "used_questions": {},
    "pending_evaluation": None,
    "current_answer": "",
    "role": "",
    "difficulty": "",
    "candidate": "Candidate",
    "bank_reset_notice": False
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.markdown("## 🎯 Interview Studio")
    st.caption("Practice. Improve. Succeed.")
    st.divider()

    role_choice = st.selectbox(
        "Choose job role",
        list(QUESTION_BANK.keys()) + EXTRA_ROLES
    )

    custom_role = ""
    role = role_choice
    if role_choice == "Other / Custom Job Role":
        custom_role = st.text_input(
            "Enter any job role you want",
            placeholder="e.g. Robotics Engineer, SAP Consultant"
        )
        role = custom_role.strip() or role_choice

    difficulty = st.selectbox(
        "Difficulty level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    number_of_questions = st.slider(
        "Questions per interview", min_value=3, max_value=6, value=4
    )
    candidate = st.text_input("Candidate name", placeholder="Enter your name")

    st.divider()
    st.markdown("### Interview tips")
    st.caption("• Explain concepts clearly")
    st.caption("• Give examples where possible")
    st.caption("• Use technical terms correctly")
    st.caption("• You can edit an answer before confirming it")

st.markdown("# 🎯 AI Powered Mock Interview Performance Evaluation System")
st.markdown("### Your personal technical interview practice room")
st.write("Practise role-based questions, revise answers before confirming, and review your performance.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f'<div class="metric-card"><h4>💼 Job Role</h4><h3>{escape(role)}</h3></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f'<div class="metric-card"><h4>📚 Difficulty</h4><h3>{escape(difficulty)}</h3></div>',
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f'<div class="metric-card"><h4>❓ Questions</h4><h3>{number_of_questions}</h3></div>',
        unsafe_allow_html=True
    )

if not st.session_state.started and not st.session_state.finished:
    st.markdown("## 🚀 Ready to begin?")
    st.write("Each interview uses questions you have not seen recently in this app session, whenever unused questions remain.")

    if st.button("Start Interview", use_container_width=True):
        if role == "Other / Custom Job Role" or not role.strip():
            st.warning("Please enter a custom job role first.")
            st.stop()

        if role in QUESTION_BANK:
            bank = normalize_bank(QUESTION_BANK[role][difficulty])
        else:
            bank = generate_role_questions(role, difficulty)

        pool_key = f"{role}|||{difficulty}"
        used = set(st.session_state.used_questions.get(pool_key, []))
        unused = [item for item in bank if item["q"] not in used]
        reset_notice = False

        if len(unused) < number_of_questions:
            used = set()
            unused = bank[:]
            reset_notice = True

        selected = random.sample(unused, min(number_of_questions, len(unused)))
        st.session_state.questions = selected
        st.session_state.results = []
        st.session_state.index = 0
        st.session_state.started = True
        st.session_state.finished = False
        st.session_state.pending_evaluation = None
        st.session_state.current_answer = ""
        st.session_state.role = role
        st.session_state.difficulty = difficulty
        st.session_state.candidate = candidate.strip() or "Candidate"
        st.session_state.bank_reset_notice = reset_notice
        st.session_state.active_pool_key = pool_key
        st.rerun()

if st.session_state.started and not st.session_state.finished:
    if st.session_state.bank_reset_notice:
        st.info("You have used most of the available questions for this role and level. The question pool has been refreshed, so some questions may repeat.")
        st.session_state.bank_reset_notice = False

    index = st.session_state.index
    questions = st.session_state.questions
    question = questions[index]

    st.progress((index + 1) / len(questions))
    st.caption(f"Question {index + 1} of {len(questions)}")

    st.markdown(
        f'<div class="question-card"><h3>Question {index + 1}</h3><p>{escape(question["q"])}</p></div>',
        unsafe_allow_html=True
    )

    with st.expander("💡 Need a hint?"):
        st.write(question["hint"])

    answer_key = f"answer_{index}"
    if answer_key not in st.session_state:
        st.session_state[answer_key] = st.session_state.current_answer

    answer = st.text_area(
        "Your answer (you can edit it and submit again)",
        key=answer_key,
        placeholder="Type your answer here...",
        height=180
    )
    st.caption(f"Words written: {len(answer.split())}")

    if st.button("Submit / Update Answer", use_container_width=True):
        if not answer.strip():
            st.warning("Please enter an answer before submitting.")
        else:
            st.session_state.current_answer = answer
            st.session_state.pending_evaluation = evaluate_answer(
                answer, question["keywords"]
            )
            st.rerun()

    if st.session_state.pending_evaluation is not None:
        evaluation = st.session_state.pending_evaluation
        st.markdown("### 📝 Answer review")
        st.metric("Current answer score", f'{evaluation["score"]}/100')
        st.write(evaluation["feedback"])

        left, right = st.columns(2)
        with left:
            st.markdown("**Matched concepts**")
            st.write(", ".join(evaluation["matched"]) if evaluation["matched"] else "No expected keywords detected.")
        with right:
            st.markdown("**Concepts to review**")
            st.write(", ".join(evaluation["missing"]) if evaluation["missing"] else "All listed keywords were detected.")

        st.info("Want to improve your answer? Edit the text above and click “Submit / Update Answer” again. Only the version you confirm will be saved.")

        if st.button("Confirm Answer & Continue", use_container_width=True):
            saved_answer = st.session_state.get(answer_key, "").strip()
            final_evaluation = evaluate_answer(saved_answer, question["keywords"])
            st.session_state.results.append({
                "question": question["q"],
                "answer": saved_answer,
                "score": final_evaluation["score"],
                "matched": final_evaluation["matched"],
                "missing": final_evaluation["missing"],
                "feedback": final_evaluation["feedback"]
            })

            pool_key = st.session_state.active_pool_key
            used = set(st.session_state.used_questions.get(pool_key, []))
            used.add(question["q"])
            st.session_state.used_questions[pool_key] = list(used)

            st.session_state.pending_evaluation = None
            st.session_state.current_answer = ""

            if index + 1 < len(questions):
                st.session_state.index += 1
            else:
                st.session_state.finished = True
                st.session_state.started = False
            st.rerun()

if st.session_state.finished:
    results = st.session_state.results
    total = len(results)
    average = round(sum(item["score"] for item in results) / total) if total else 0

    st.balloons()
    st.markdown("## 🏆 Interview Performance Report")
    st.write(f'Candidate: **{st.session_state.candidate}**')
    st.write(f'Role: **{st.session_state.role}** · Difficulty: **{st.session_state.difficulty}**')

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Score", f"{average}/100")
    c2.metric("Questions Answered", total)
    c3.metric("Strong Answers", sum(item["score"] >= 70 for item in results))
    st.progress(average / 100)

    if average >= 80:
        st.success("Great practice session! Keep refining your explanations.")
    elif average >= 50:
        st.info("Good effort. Review the missing concepts and try again.")
    else:
        st.warning("Use the feedback below to strengthen your fundamentals.")

    st.markdown("### 📋 Question-by-question feedback")
    for i, item in enumerate(results, 1):
        with st.expander(f'Q{i}. {item["question"]} — {item["score"]}/100'):
            st.markdown("**Your final answer**")
            st.write(item["answer"])
            st.markdown("**Matched concepts**")
            st.write(", ".join(item["matched"]) if item["matched"] else "No expected keywords detected.")
            st.markdown("**Concepts to review**")
            st.write(", ".join(item["missing"]) if item["missing"] else "All listed keywords were detected.")
            st.markdown("**Feedback**")
            st.write(item["feedback"])

    st.markdown("### 📥 Download your report")
    report = io.StringIO()
    writer = csv.writer(report)
    writer.writerow([
        "Candidate", "Role", "Difficulty", "Question", "Answer",
        "Score", "Matched Concepts", "Concepts to Review", "Feedback"
    ])
    for item in results:
        writer.writerow([
            st.session_state.candidate, st.session_state.role,
            st.session_state.difficulty, item["question"], item["answer"],
            item["score"], ", ".join(item["matched"]),
            ", ".join(item["missing"]), item["feedback"]
        ])

    st.download_button(
        "Download Interview Report (CSV)",
        data=report.getvalue(),
        file_name="interview_performance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Start a New Interview", use_container_width=True):
        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.results = []
        st.session_state.questions = []
        st.session_state.index = 0
        st.session_state.pending_evaluation = None
        st.session_state.current_answer = ""
        st.rerun()

st.markdown("---")
st.markdown(
    '<p class="small-note">Questions already completed are tracked during the current app session by job role and difficulty. When the available question pool is exhausted, it refreshes and some questions may repeat. Scores are based on keyword coverage and answer length; they do not establish factual correctness or predict hiring outcomes.</p>',
    unsafe_allow_html=True
)
