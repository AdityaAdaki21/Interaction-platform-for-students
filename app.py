from datetime import datetime
from flask import (
    Flask,
    flash,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    session,
)
import mysql.connector
import logging
from decimal import Decimal  # Import Decimal for handling Decimal values


mydb = mysql.connector.connect(
    host="localhost", user="root", password="Aditya@21", database="cp"
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_secret_key"  # Replace with a strong secret key

# Configure logging
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG or the desired level
handler = logging.FileHandler("app.log")  # Log messages to a file named app.log
handler.setLevel(logging.DEBUG)  # Set the log level for the file handler
app.logger.addHandler(handler)


@app.route("/")
def login_or_register():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle the POST request for logging in
        email = request.form["email"]
        prn = request.form["prn"]

        mycursor = mydb.cursor()
        sql = "SELECT * FROM students WHERE Mail = %s AND PRN = %s"
        val = (email, prn)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        if user:
            # Existing user, perform login
            session["user_email"] = email
            session["user_name"] = user[
                1
            ]  # Assuming that the user's name is in the second column of the database table
            session["user_prn"] = user[0]  # Set user's PRN in the session

            return redirect(url_for("index"))
        else:
            # Authentication failed, display an error
            return render_template(
                "login.html",
                error="Authentication failed. Please check your credentials.",
            )
    else:
        # Handle the GET request, which may include rendering the login/registration form
        return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        # Handle registration as you did before
        PRN = request.form["prn"]
        Name = request.form["student_name"]
        Year = request.form["year"]
        Mail = request.form["email"]
        GitHub = request.form.get(
            "github"
        )  # Use request.form.get to handle optional fields
        LinkedIn = request.form.get(
            "linkedin"
        )  # Use request.form.get to handle optional fields
        Bio = request.form.get("bio")  # Use request.form.get to handle optional fields

        mycursor = mydb.cursor()
        sql = "INSERT INTO students (PRN, Name, Year, Mail, GitHub, LinkedIn, Bio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (PRN, Name, Year, Mail, GitHub, LinkedIn, Bio)
        mycursor.execute(sql, val)
        mydb.commit()

        session["user_email"] = Mail  # Automatically log in the user after registration
        session[
            "user_name"
        ] = Name  # Set user_name in the session based on the provided Name

        return redirect(url_for("index"))

    # Handle cases where the method is not POST (e.g., GET request)
    return redirect(url_for("login_or_register"))


# Add a new route for logout
@app.route("/logout")
def logout():
    # Clear the user's session
    session.clear()
    # Redirect to the login page
    return redirect(url_for("login"))


@app.route("/index")
def index():
    if "user_email" in session:
        # The user is logged in, continue to your index page
        return render_template("index.html")
    else:
        # The user is not logged in, redirect to the login page
        return redirect(url_for("login_or_register"))


@app.route("/submit_question", methods=["POST"])
def submit_question():
    if "user_email" in session:
        if request.method == "POST":
            # Get the form data
            D_ID = request.form["domain"]
            question_text = request.form["question"]
            user_name = session[
                "user_name"
            ]  # Retrieve the user's name from the session

            mycursor = mydb.cursor()
            get_prn_sql = "SELECT PRN FROM students WHERE Mail = %s"
            mycursor.execute(get_prn_sql, (session["user_email"],))
            user_prn = mycursor.fetchone()

            if user_prn:
                user_prn = user_prn[0]
                # Insert the question into the database without specifying Q_ID
                insert_question_sql = "INSERT INTO questions (D_ID, PRN, Timestamp, Question) VALUES (%s, %s, NOW(), %s)"
                values = (D_ID, user_prn, question_text)

                mycursor.execute(insert_question_sql, values)
                mydb.commit()

                return redirect(url_for("question"))
            else:
                return render_template("index.html", error="User PRN not found.")
        else:
            return render_template("index.html", error="Invalid request method.")
    else:
        return redirect(url_for("login_or_register"))


@app.route("/question")
def question():
    if "user_email" in session:
        # Fetch recent questions from the database
        mycursor = mydb.cursor(dictionary=True)
        fetch_questions_sql = "SELECT * FROM questions ORDER BY Timestamp DESC LIMIT 10"
        mycursor.execute(fetch_questions_sql)
        recent_questions = mycursor.fetchall()

        return render_template("Question_page.html", recent_questions=recent_questions)
    else:
        # User is not logged in, redirect to login or registration page
        return redirect(url_for("login_or_register"))


# Add a new route to display answers for a specific question
@app.route("/answer_question/<int:question_id>", methods=["GET", "POST"])
def answer_question(question_id):
    if "user_email" in session:
        if request.method == "POST":
            # Get the answer text from the form
            answer_text = request.form["answer"]

            user_prn = None  # Initialize user_prn to None
            mycursor = mydb.cursor()
            get_prn_sql = "SELECT PRN FROM students WHERE Mail = %s"
            mycursor.execute(get_prn_sql, (session["user_email"],))
            user_prn = mycursor.fetchone()

            if user_prn:
                user_prn = user_prn[0]

                # Insert the answer into the database, associating it with the question (Q_ID)
                insert_answer_sql = "INSERT INTO answers (Q_ID, PRN, Timestamp, Answer) VALUES (%s, %s, NOW(), %s)"
                values = (question_id, user_prn, answer_text)

                mycursor.execute(insert_answer_sql, values)
                mydb.commit()  # Commit the transaction

                # After inserting the answer into the database, stay on the same page
                return redirect(url_for("answer_question", question_id=question_id))
            else:
                return render_template("index.html", error="User PRN not found.")
        else:
            # Handle the GET request, fetch the question and answers for display
            mycursor = mydb.cursor(dictionary=True)
            fetch_question_sql = "SELECT Q_ID, Question FROM questions WHERE Q_ID = %s"
            mycursor.execute(fetch_question_sql, (question_id,))
            question = mycursor.fetchone()

            if question:
                # Fetch answers for the question
                fetch_answers_sql = """
                SELECT answers.A_ID, answers.PRN, answers.Answer, students.Name, AVG(reviews.Rating) as AvgRating
                FROM answers
                JOIN students ON answers.PRN = students.PRN
                LEFT JOIN reviews ON answers.A_ID = reviews.A_ID
                WHERE answers.Q_ID = %s
                GROUP BY answers.A_ID, answers.PRN, answers.Answer, students.Name, students.PRN
                """

                mycursor.execute(fetch_answers_sql, (question_id,))
                answers = mycursor.fetchall()

                return render_template(
                    "answer.html",
                    question=question,
                    answers=answers,
                    user_name=session["user_name"],
                )
            else:
                flash("Question not found.")
                return redirect(url_for("recent_questions"))
    else:
        # User is not logged in, redirect to the login or registration page
        return redirect(url_for("login_or_register"))


def user_has_reviewed_answer(answer_id, user_prn):
    if "user_email" in session:
        try:
            answer_id = int(answer_id)  # Attempt to convert to an integer
            if user_prn is not None:
                user_prn = int(user_prn)  # Attempt to convert to an integer

                mycursor = mydb.cursor()

                # Check if a review exists for the answer by the current user
                check_review_sql = "SELECT * FROM reviews WHERE A_ID = %s AND PRN = %s"
                check_values = (answer_id, user_prn)
                mycursor.execute(check_review_sql, check_values)
                existing_review = mycursor.fetchone()

                if existing_review:
                    return True
        except ValueError:
            # Handle the case where the conversion to integers failed
            return False
    return False


@app.before_request
def add_template_context():
    if "user_email" in session:
        user_prn = session.get("user_prn")
        app.jinja_env.globals.update(user_has_reviewed_answer=user_has_reviewed_answer)
        app.jinja_env.globals["user_prn"] = user_prn


# @app.before_request
# def add_template_context():
#     app.jinja_env.globals.update(user_has_reviewed_answer=user_has_reviewed_answer)


@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    if "user_email" in session:
        if request.method == "POST":
            answer_id = request.form.get("answer_id")
            rating = int(request.form.get("rating"))

            print("Received POST request for submitting a rating.")
            print(f"Received answer_id: {answer_id}")
            print(f"Received rating: {rating}")

            if rating in range(1, 6):
                user_prn = session.get("user_prn")

                if user_prn is not None:
                    try:
                        mycursor = mydb.cursor()

                        # Check if the user has already reviewed this answer
                        check_rating_sql = (
                            "SELECT * FROM reviews WHERE A_ID = %s AND PRN = %s"
                        )
                        check_values = (answer_id, user_prn)
                        mycursor.execute(check_rating_sql, check_values)
                        existing_rating = mycursor.fetchone()

                        if existing_rating:
                            print("You have already reviewed this answer.")
                        else:
                            # Construct the SQL query to insert the rating into the reviews table
                            insert_rating_sql = "INSERT INTO reviews (A_ID, PRN, Rating, Timestamp) VALUES (%s, %s, %s, NOW())"
                            values = (answer_id, user_prn, rating)

                            mycursor.execute(insert_rating_sql, values)
                            mydb.commit()
                            print(mycursor.statement)  # Print the SQL statement

                            print("Rating successfully inserted into the database.")

                        # Redirect back to the same question's answers page
                        return redirect(
                            url_for("answer_question", question_id=answer_id)
                        )
                    except mysql.connector.Error as err:
                        print(f"Database error: {err}")
                        flash(
                            "An error occurred while submitting the rating. Please try again."
                        )
                else:
                    flash("Rating submission failed: User PRN not found.")
            else:
                flash("Rating submission failed: Invalid rating value.")
        return redirect(url_for("answer_question", question_id=answer_id))
    else:
        return redirect(url_for("login_or_register"))


@app.route("/api/answers/<int:question_id>")
def fetch_answers(question_id):
    # Fetch answers for the specified question from the database
    mycursor = mydb.cursor(dictionary=True)
    fetch_answers_sql = "SELECT A_ID, Answer FROM answers WHERE Q_ID = %s"
    mycursor.execute(fetch_answers_sql, (question_id,))
    answers = mycursor.fetchall()

    # Render the "answer.html" template with the question and answers
    mycursor.execute("SELECT Question FROM questions WHERE Q_ID = %s", (question_id,))
    question = mycursor.fetchone()

    return render_template("answer.html", question=question, answers=answers)


@app.route("/recent_questions")
def recent_questions():
    if "user_email" in session:
        mycursor = mydb.cursor(dictionary=True)
        fetch_questions_sql = "SELECT * FROM questions ORDER BY Timestamp DESC LIMIT 10"
        mycursor.execute(fetch_questions_sql)
        recent_questions = mycursor.fetchall()

        return render_template(
            "recent_questions.html", recent_questions=recent_questions
        )
    else:
        return redirect(url_for("login_or_register"))


@app.route("/profile")
def profile():
    if "user_email" in session:
        mycursor = mydb.cursor(dictionary=True)

        # Fetch user's basic information
        fetch_user_info_sql = (
            "SELECT Name, PRN, GitHub, LinkedIn, Bio FROM students WHERE Mail = %s"
        )
        mycursor.execute(fetch_user_info_sql, (session["user_email"],))
        user_info = mycursor.fetchone()

        # Fetch user's selected expertise
        fetch_expertise_sql = "SELECT domains.Domain FROM expertise JOIN domains ON expertise.Expertise = domains.D_ID WHERE expertise.PRN = %s"
        mycursor.execute(fetch_expertise_sql, (user_info["PRN"],))
        selected_expertise = mycursor.fetchone()

        # Fetch user's questions and answers (if needed)
        fetch_user_questions_sql = "SELECT * FROM questions WHERE PRN = %s"
        mycursor.execute(fetch_user_questions_sql, (user_info["PRN"],))
        user_questions = mycursor.fetchall()

        fetch_user_answers_sql = "SELECT * FROM answers WHERE PRN = %s"
        mycursor.execute(fetch_user_answers_sql, (user_info["PRN"],))
        user_answers = mycursor.fetchall()

        num_questions = len(user_questions)
        num_answers = len(user_answers)

        # Fetch available domains
        available_domains = fetch_available_domains()
        print("Available Domains (in /profile):", available_domains)

        return render_template(
            "profile.html",
            available_domains=available_domains,
            user=user_info,
            selected_expertise=selected_expertise,
            user_questions=user_questions,
            user_answers=user_answers,
            num_questions=num_questions,
            num_answers=num_answers,
        )
    else:
        return redirect(url_for("login_or_register"))


def fetch_available_domains():
    mycursor = mydb.cursor()
    fetch_domains_sql = "SELECT Domain FROM domains"
    mycursor.execute(fetch_domains_sql)
    available_domains = mycursor.fetchall()
    print("Available Domains:", available_domains)
    return available_domains


@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "user_email" in session:
        user_email = session["user_email"]
        github = request.form.get("github")
        linkedin = request.form.get("linkedin")
        bio = request.form.get("bio")
        expertise = request.form.get("expertise")  # Add expertise to form data

        mycursor = mydb.cursor()

        # Construct an SQL query to update the profile
        sql = "UPDATE students SET"
        updates = []

        # Check if the user provided GitHub and add it to the query if not empty
        if github:
            updates.append(f"GitHub = '{github}'")

        # Check if the user provided LinkedIn and add it to the query if not empty
        if linkedin:
            updates.append(f"LinkedIn = '{linkedin}'")

        # Check if the user provided Bio and add it to the query if not empty
        if bio:
            updates.append(f"Bio = '{bio}'")

        # Check if the user provided expertise and add it to the query if not empty
        if expertise:
            updates.append(f"Expertise = '{expertise}'")

        # Join all the update clauses
        update_clause = ", ".join(updates)

        # Finalize the query
        sql = f"{sql} {update_clause} WHERE Mail = '{user_email}'"

        mycursor.execute(sql)
        mydb.commit()

        # Redirect to the profile page after the update
        return redirect("/profile")
    else:
        # Handle the case when the user is not logged in
        return redirect("/login")


@app.route("/update_expertise", methods=["POST"])
def update_expertise():
    if "user_email" in session:
        # Get the selected expertise from the form
        selected_expertise = request.form.get("expertise")
        print(f"Selected Expertise: {selected_expertise}")

        # Look up the PRN of the current user based on their email
        mycursor = mydb.cursor(dictionary=True)
        fetch_user_prn_sql = "SELECT PRN FROM students WHERE Mail = %s"
        mycursor.execute(fetch_user_prn_sql, (session["user_email"],))
        user_prn = mycursor.fetchone()

        if user_prn:
            user_prn = user_prn["PRN"]

            # Check if the selected expertise exists in the domains table
            check_expertise_sql = "SELECT D_ID FROM domains WHERE Domain = %s"
            mycursor.execute(check_expertise_sql, (selected_expertise,))
            expertise_result = mycursor.fetchone()

            if expertise_result:
                # The expertise exists in the domains table, you can proceed to update the expertise
                expertise_id = expertise_result["D_ID"]
                print(f"Expertise ID: {expertise_id}")

                # Update the user's expertise in the expertise table
                update_expertise_sql = "INSERT INTO expertise (PRN, Expertise) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Expertise = VALUES(Expertise)"
                mycursor.execute(update_expertise_sql, (user_prn, expertise_id))
                mydb.commit()

                # Redirect back to the profile page
                return redirect(url_for("profile"))
            else:
                # Handle the case where the selected expertise doesn't exist in the domains table
                flash(
                    "Selected expertise doesn't exist. Please choose a valid expertise."
                )
                return redirect(url_for("profile"))
        else:
            # Handle the case where the user's PRN couldn't be found
            flash("User not found. Please log in again.")
            return redirect(url_for("login_or_register"))
    else:
        return redirect(url_for("login_or_register"))


if __name__ == "__main__":
    app.before_request(add_template_context)
    app.run(host="192.168.224.3", port=5000)
