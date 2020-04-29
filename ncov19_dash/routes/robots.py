from flask import Blueprint, current_app


robots = Blueprint(
    "robots", __name__, static_folder="assets", static_url_path="/static"
)


@robots.route("/robots.txt")
def static_from_root():
    """robots.txt
    """
    response = current_app.send_static_file("robots.txt")
    return response
