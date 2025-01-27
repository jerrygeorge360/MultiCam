from flask import Blueprint, render_template


main = Blueprint("main", __name__, template_folder="templates/main", static_folder="static")



@main.route('/')
def home():
    """
       Home page for the streaming service
       ---
       description: This endpoint renders the homepage of the streaming service, providing a caption and an infographic link.
       responses:
         200:
           description: Renders the homepage with a caption and infographic link.
           content:
             text/html:
               schema:
                 type: string
                 example: "<html>...main page content...</html>"
       """

    caption = "🎥 Experience Streaming Like Never Before! 🌟 Dive into a world where YOU control the view! Switch " \
              "between multiple camera angles in real-time during your favorite streams. Don’t just watch—immerse " \
              "yourself! "
    infographics = 'https://infograph.venngage.com/ps/V8kKxhJisAE'
    return render_template("main.html", caption=caption, infographics=infographics)
