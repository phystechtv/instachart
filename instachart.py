from flask import Flask, render_template, jsonify
import simplejson as json
application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False

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
    return json.dumps(medias[:10], ensure_ascii=False)

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, use_reloader=True)