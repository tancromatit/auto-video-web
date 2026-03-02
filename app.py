from flask import Flask, request, render_template, send_file
import os
from auto_ghep_video import ghep_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("videos")

        paths = []
        for f in files:
            path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(path)
            paths.append(path)

        output = ghep_video(paths)

        return send_file(output, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()