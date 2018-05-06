from flask import Flask, render_template
app = Flask(__name__)

from dbextract import extract_scores

@app.route("/")
def homepage():
    medias = extract_scores()
    # html = """ """
    # for m in top_scores:
    #     html += """<img src="{link}"> """.format(link=m["link"])
    #     html += """Фото от  <a href="{profile_link}"> {username} </a>""".format(
    #         profile_link="https://instagram.com/" + m["username"],
    #         username=m["username"]
    #     )
    #     html += """ Рейтинг: {score}""".format(score=m["score"])
    # return html

    return render_template("index.html", medias=medias[:10])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)