from flask import Flask, request, send_file, jsonify
from utils.style_transfer import style_transfer
from PIL import Image
import io

app = Flask(__name__)

@app.route("/stylize", methods=["POST"])
def stylize():
    try:
        content_file = request.files.get("content")
        style_file = request.files.get("style")
        strength = float(request.form.get("strength", 1.0))

        if not content_file or not style_file:
            return jsonify({"error": "Missing images"}), 400

        # Read image bytes and open with PIL
        content_img = Image.open(io.BytesIO(content_file.read())).convert("RGB")
        style_img = Image.open(io.BytesIO(style_file.read())).convert("RGB")

        output_img = style_transfer(content_img, style_img, strength)

        buffer = io.BytesIO()
        output_img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)