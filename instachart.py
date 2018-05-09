from flask import Flask, render_template
application = Flask(__name__)

from dbextract import extract_scores

@application.route("/")
def homepage():
    medias = extract_scores()
    return render_template("index.html", medias=medias[:10],
                           last_update=min([m["last_update"] for m in medias]),
                           total_mipt_users=len(set([m["username"] for m in medias])))

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, use_reloader=True)