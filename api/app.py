from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_githubusername = request.form.get("github_username")
    return render_template("hello.html",
                           name=input_name, age=input_age,
                           github_username=input_githubusername)


def get_github_username(github_username):
    response = requests.get
    ("https://api.github.com/users/{github_username}/repos")
    if response.status_code == 200:
        repos = response.json()
        # data returned is a list of ‘repository’ entities
        for repo in repos:
            print(repo["full_name"])

    else:
        # Handle the case where the request was not successful
        print(f"Failed to retrieve repositories for {github_username}." +
              f"Status code: {response.status_code}")


@app.route("/")
def hello_world():
    return render_template("index.html")


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    if query == "asteroids":
        return "Unknown"

    if query == "What is your name?":
        return "name"

    if "plus" in query:
        query_words = query.split(" ")
        numbers = []
        for word in query_words:
            if word[0].isdigit():
                if word[-1] == '?':
                    word = word[:-1]
                numbers.append(int(word))
        if numbers:
            return str(sum(numbers))
        else:
            return "No"

    if "minus" in query:
        query_words = query.split(" ")
        numbers = []
        operation = None
        for word in query_words:
            if word[0].isdigit():
                if word[-1] == '?':
                    word = word[:-1]
                numbers.append(int(word))
            elif word == "minus":
                operation = "subtract"

        if operation == "subtract":
            if len(numbers) == 2:
                result = numbers[0] - numbers[1]
                return str(result)
            else:
                return "Invalid subtraction format: Need two numbers"
        else:
            return "Unknown operation"

    if "multiplied" in query:
        query_words = query.split(" ")
        numbers = []
        operation = None
        for word in query_words:
            if word[0].isdigit():
                if word[-1] == '?':
                    word = word[:-1]
                numbers.append(int(word))
            elif word == "multiplied":
                operation = "multiplication"

        if operation == "multiplication":
            if len(numbers) == 2:
                result = numbers[0] * numbers[1]
                return str(result)
            else:
                return "Invalid subtraction format: Need two numbers"
        else:
            return "Unknown operation"

    return "Unknown"


@app.route("/query", methods=["GET"])
def handle_query():
    query_query = request.args.get('q')
    return process_query(query_query)
