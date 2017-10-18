from flask import Flask, request, Response

ci_app = Flask("IzunaCI")


@ci_app.route("/git_hook", methods=["POST"])
def git_hook():
    print(request.form)
    return Response("OK", 200)


ci_app.run("0.0.0.0", 5000)

