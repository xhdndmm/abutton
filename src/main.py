from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "clicks.json"

# 初始化点击次数
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"count": 0}, f)

def get_count():
    with open(DATA_FILE, "r") as f:
        return json.load(f)["count"]

def save_count(count):
    with open(DATA_FILE, "w") as f:
        json.dump({"count": count}, f)

# 页面模板
HTML_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>一个按钮</title>
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 100px; }
        button { font-size: 20px; padding: 10px 20px; cursor: pointer; }
        #count { font-size: 24px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>一个按钮</h1>
    <button id="btn">点击我</button>
    <div id="count">已被点击次数：<span id="num">0</span></div>

    <script>
        async function getCount() {
            const res = await fetch("/get_count");
            const data = await res.json();
            document.getElementById("num").textContent = data.count;
        }

        document.getElementById("btn").addEventListener("click", async () => {
            const res = await fetch("/add", {method: "POST"});
            const data = await res.json();
            document.getElementById("num").textContent = data.count;
        });

        getCount();  // 页面加载时获取初始次数
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/get_count")
def get_count_api():
    return jsonify({"count": get_count()})

@app.route("/add", methods=["POST"])
def add_count():
    count = get_count() + 1
    save_count(count)
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True,debug = False)
