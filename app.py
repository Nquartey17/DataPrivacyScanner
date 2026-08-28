import os

from flask import Flask, request, render_template, redirect, url_for,flash
from scanner import *
from conversion import extract_text
from lists import *
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import plotly.express as px

#Idea: Add an option to type custom keywords
# Idea: Suggested keywords depending on selection. To avoid too many words found, suggest keywords to search

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app) #Connect SQLAlchemy to Flask

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Verify password
# if check_password_hash(user.password, entered_password):
#     print("Correct")
# hashed = generate_password_hash()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
@login_required
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))

        flash("Invalid username or password")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        print(request.form)

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check for existing users
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match")
            return render_template("register.html")

        hashed = generate_password_hash(password)

        user = User(username=username, password=hashed)

        db.session.add(user)
        db.session.commit()

        login_user(user) #Automatic login in
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/results", methods=["POST"])
@login_required
def upload_file():
    file = request.files.get("files")

    #If file doesn't exist, prevent crashing
    if not file:
        return {"error": "File missing"}, 400

    try:
        content = extract_text(file)
        results = text_scan(content)

        #Get selected inputs from index.html checklist
        pii_selections = request.form.getlist("pii_dropdown")
        phi_selections = request.form.getlist("phi_dropdown")
        finance_hdv = request.form.getlist("finance_hdv")
        security = request.form.getlist("security")

        # Taking values from DEFAULT_KEYWORDS and changing it into list
        all_keywords = []

        #always including default terms
        add_keywords(CATEGORIES["default"], all_keywords)


        add_keywords(pii_selections, all_keywords)
        add_keywords(phi_selections, all_keywords)
        add_keywords(finance_hdv, all_keywords)
        add_keywords(security, all_keywords)

        keywords = keyword_finder(content, all_keywords)

        # returning new dictionary for selected terms and only displaying selected terms
        selected_pii = checkbox_selections(pii_selections)
        pii_count = keyword_count(content, selected_pii)
        pii_keywords = keyword_hits(content, selected_pii)
        pii_convert = terms_to_labels(pii_keywords)

        selected_phi = checkbox_selections(phi_selections)
        phi_count = keyword_count(content, selected_phi)
        phi_keywords = keyword_hits(content, selected_phi)
        phi_convert = terms_to_labels(phi_keywords)

        selected_finance = checkbox_selections(finance_hdv)
        finance_hdv_count = keyword_count(content, selected_finance)
        fhdv_keywords = keyword_hits(content, selected_finance)
        fhdv_convert = terms_to_labels(fhdv_keywords)

        selected_security = checkbox_selections(security)
        security_count = keyword_count(content, selected_security)
        sq_keywords = keyword_hits(content, selected_security)
        sq_convert = terms_to_labels(sq_keywords)

        risk = calculate_average_risk(pii_count,phi_count,finance_hdv_count,security_count)

        # Donut chart display
        fig = px.pie(
            names=["Low", "Medium", "High"],
            values=[risk["low"],risk["medium"],risk["high"]],
            hole=0.5,
            title="Risk Level Distribution",
            color=["Low", "Medium", "High"],
            color_discrete_map={"Low": "green", "Medium": "gold", "High": "red"}
        )
        fig.update_traces(textinfo="percent+label")

        fig.add_annotation(
            text=f"Terms Found:<br><b>{risk['total']}</b>",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=20)
        )

        fig.update_layout(
            autosize=True,
            height=350,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        risk_donut = fig.to_html(
            full_html=False,
            config={"responsive": True}
        )

        #pii bar graph
        pii_bar = create_bar_chart(convert_keys_to_labels(pii_count),"PII Findings","#4C78A8")
        phi_bar = create_bar_chart(convert_keys_to_labels(phi_count), "PHI Findings", "#4C78A8")
        fhdv_bar = create_bar_chart(convert_keys_to_labels(finance_hdv_count), "Finance and HDV Findings", "#4C78A8")
        sq_bar = create_bar_chart(convert_keys_to_labels(security_count), "Security Finding", "#4C78A8")


        return render_template("results.html", results=results, keywords=keywords,
                               pii_keywords=pii_convert, phi_keywords=phi_convert,fhdv_keywords=fhdv_convert,
                               sq_keywords =sq_convert,risk=risk, risk_donut=risk_donut,pii_bar=pii_bar,
                               phi_bar=phi_bar,fhdv_bar=fhdv_bar, sq_bar=sq_bar)

    except ValueError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)