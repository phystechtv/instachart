from flask import Flask, render_template, jsonify
application = Flask(__name__)

from dbextract import extract_scores

@application.route("/")
def homepage():
    medias = extract_scores()
    return render_template("index.html", medias=medias[:10],
                           last_update=min([m["last_update"] for m in medias]),
                           total_mipt_users=len(set([m["username"] for m in medias])))

@application.route("/medias")
def media_data():
    medias = extract_scores()
    return jsonify(medias[:10])

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, use_reloader=True)