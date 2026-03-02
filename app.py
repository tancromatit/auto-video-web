from flask import Flask, render_template, request, send_file
import os
from video_merge import merge_videos

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/merge", methods=["POST"])
def merge():
    files = request.files.getlist("videos")

    paths = []

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        paths.append(path)

    output = ghep_video(paths, OUTPUT_FOLDER)

    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

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
