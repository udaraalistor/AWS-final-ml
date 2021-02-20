from flask import Flask, request
from oauthlib.uri_validate import host
from werkzeug.utils import secure_filename
from Object_detector import IdentityObject

app = Flask(__name__)

object_finder = IdentityObject()


@app.route("/api/v1/detect_object", methods=["POST"])
def detect_object():
    result_res = []
    if request.method == "POST":
        image_file = request.files["image"]
        file_name = secure_filename(filename=image_file.filename)
        file_save = f"uploads/{file_name}"
        image_file.save(file_save)
        result = object_finder.identify(file_save)
        for idx, score in enumerate(result["detection_scores"]):
            score = score * 100
            if score > 30:
                entity = str(result["detection_class_entities"][idx])
                name = str(result["detection_class_names"][idx])
                box = result["detection_boxes"][idx]
                box = [float(b) for b in box]

                print(type(name), type(box), type(score), type(entity))

                result_res.append({
                    "name": name,
                    "entity": entity,
                    "box": box,
                    "score": float(score)
                })

    return {
        "status": "success",
        "result": result_res
    }


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
