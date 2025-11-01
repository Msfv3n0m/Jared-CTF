from flask import Flask, request, jsonify, render_template_string
from lxml import etree
import time
import os
import uuid

app = Flask(__name__)

STORAGE_DIR = "./"


def _save_temp_file(file_storage):
    filename = f"{int(time.time()*1000)}-{uuid.uuid4().hex}.xml"
    path = os.path.join(STORAGE_DIR, filename)
    file_storage.save(path)
    return path


def _extract_summary(root):
    summary = {}
    summary["root_tag"] = root.tag

    text_snippet = None
    if root.text and root.text.strip():
        text_snippet = root.text.strip()
    else:
        for ch in root.iter():
            if ch is root:
                continue
            if ch.text and ch.text.strip():
                text_snippet = ch.text.strip()
                break
    summary["text_snippet"] = text_snippet

    counts = {}
    for child in root:
        counts[child.tag] = counts.get(child.tag, 0) + 1
    summary["child_counts"] = counts

    def find_text(case_insensitive_names):
        for name in case_insensitive_names:
            el = root.find(".//" + name)
            if el is not None and el.text:
                return el.text.strip()
        for el in root.iter():
            if el.tag.lower() in [n.lower() for n in case_insensitive_names] and el.text:
                return el.text.strip()
        return None

    summary["title"] = find_text(["title", "bookTitle", "name"])
    summary["author"] = find_text(["author", "creator", "by"])

    return summary


@app.route("/process", methods=["GET", "POST"])
def process():
    if not request.files:
        return render_template_string("""
        <h3>Upload an XML file</h3>
        <form method="POST" enctype="multipart/form-data">
          <input type="file" name="file"><br/><br/>
          <input type="submit" value="Upload">
        </form>
        """)
    first_file = next(iter(request.files.values()))
    saved_path = _save_temp_file(first_file)

    try:
        with open(saved_path, "rb") as fh:
            data = fh.read()

        os.remove(saved_path)

        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        root = etree.fromstring(data, parser=parser)

        summary = _extract_summary(root)

        summary["original_file"] = saved_path

        return jsonify(summary), 200

    except Exception as e:
        return jsonify({"error": f"parse error: {e}", "saved_file": saved_path}), 400


if __name__ == "__main__":
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0')
