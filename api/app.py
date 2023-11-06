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


def get_github_repositories(github_username):
    url = f"https://api.github.com/users/{github_username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        repository_list = []
        # data returned is a list of ‘repository’ entities
        for repo in repos:
            repo_info = {
                "name": repo["name"],
                "url": repo["html_url"]
            }

            # Fetch commit information for the repository
            commit_url = (
                f"https://api.github.com/repos/"
                f"{github_username}/{repo['name']}/commits"
            )

            commit_response = requests.get(commit_url)

            if commit_response.status_code == 200:
                commits = commit_response.json()
                if commits:
                    latest_commit = commits[0]
                    # The first commit in the list is the latest
                    commit_info = {
                        "hash": latest_commit["sha"],
                        "author": latest_commit["commit"]["author"]["name"],
                        "date": latest_commit["commit"]["author"]["date"],
                        "message": latest_commit["commit"]["message"]
                    }
                    repo_info["commit_info"] = commit_info
                else:
                    repo_info["commit_info"] = {}
            else:
                print(f"Failed to retrieve commit information"
                      f"for {github_username}/{repo['name']}. "
                      f"Status code: {commit_response.status_code}")
                repo_info["commit_info"] = {}

            repository_list.append(repo_info)

        return repository_list

    else:
        # Handle the case where the request was not successful
        print(f"Failed to retrieve repositories for {github_username}." +
              f"Status code: {response.status_code}")
        return []


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
