from flask import Blueprint, render_template
import os
from flask_login import login_required

main = Blueprint("main", __name__, template_folder="templates/main", static_folder="static")


@main.route('/')
def home():
    caption = "🎥 Experience Streaming Like Never Before! 🌟 Dive into a world where YOU control the view! Switch " \
              "between multiple camera angles in real-time during your favorite streams. Don’t just watch—immerse " \
              "yourself! "
    infographics = 'https://infograph.venngage.com/ps/V8kKxhJisAE'
    return render_template("main.html", caption=caption, infographics=infographics)
