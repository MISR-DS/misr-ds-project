from flask import Flask, request, jsonify
from flask import send_from_directory
import os
import json
import subprocess
import sys
import sqlite3
import random
import string

app = Flask(__name__)

DATA_FOLDER = "data"
BASE_DIR = "data"



@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory('videos', filename)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)


@app.route('/run_action', methods=['POST'])
def run_action():
    action = request.json['action']
    user_id = request.json["user_id"]

    # os.system("python Video_inserted/live_child.py")
    # os.system(f"python Video_inserted/compare_live.py {action}")

    subprocess.run([sys.executable, "Video_inserted/live_child.py"])
    subprocess.run([sys.executable, "Video_inserted/compare_live.py", action])

    if not os.path.exists("result.json"):
        return jsonify({
            "result": "Error",
            "score": 0
        })

    with open("result.json") as f:
        result_data = json.load(f)
        import datetime

        conn = sqlite3.connect("kids.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reports
         (
           user_id,
           action_name,
           score,
           result,
           test_date
          )
       VALUES (?,?,?,?,?)
        """,
      (
        user_id,
        action,
        result_data["score"],
        result_data["result"],
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
     ))

        conn.commit()
        conn.close()

    return jsonify(result_data)


@app.route('/record', methods=['POST'])
def record():
    data = request.json
    action_name = data['action_name']

    os.system(f'python record_video.py "{action_name}"')

    return jsonify({"status": "recorded", "file": action_name})


@app.route('/build', methods=['POST'])
def build():
    data = request.json

    video_path = data['video_path']
    action_name = data['action_name']

    os.system(f'python build_reference.py "{video_path}" "{action_name}"')

    return jsonify({"status": "built", "action": action_name})




@app.route('/get_actions', methods=['GET'])
def get_actions():
    

    actions = os.listdir("data")
    actions = [a.replace(".json", "") for a in actions]

    return jsonify({
        "actions": actions
    })


@app.route('/parent_record', methods=['POST'])
def parent_record():
    action_name = request.json['action_name']

    os.system(f'python Video_from_parent/record_video.py "{action_name}"')

    return jsonify({"status": "recorded"})



@app.route('/build_reference', methods=['POST'])
def build_reference():
    video_path = request.json['video_path']
    action_name = request.json['action_name']

    os.system(f'python Video_inserted/build_reference.py "{video_path}" "{action_name}"')

    return jsonify({"status": "done"})


@app.route("/upload_action", methods=["POST"])
def upload_action():

    action = request.form["action"]

    image = request.files["image"]
    video = request.files["video"]

    image_path = f"images/{action}.jpg"
    video_path = f"videos/{action}.mp4"

    image.save(image_path)
    video.save(video_path)

    result = subprocess.run(
         [sys.executable, "Video_inserted/build_reference.py", video_path],
        capture_output=True,
        text=True
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0 or not result.stdout.strip():
        return {"status": "error", "msg": result.stderr}

    try:
        ai_output = json.loads(result.stdout)
    except Exception as e:
        return {
            "status": "error",
            "msg": "Invalid AI output",
            "details": result.stdout
        }

    if isinstance(ai_output, dict) and "error" in ai_output:
        return ai_output

    landmarks = ai_output

    data = {
        "action": action,
        "image": image_path,
        "video": video_path,
        "landmarks": landmarks
    }

    with open(f"data/{action}.json", "w") as f:
        json.dump(data, f)

    return data


@app.route("/upload_action2", methods=["POST"])
def upload_action2():

    action = request.form["action"]
    image = request.files["image"]

    image_path = f"images/{action}.jpg"
    video_path = f"videos/{action}.mp4"

    image.save(image_path)

    if not os.path.exists(video_path):
        return {"status": "error", "msg": "الفيديو غير موجود، سجل الفيديو الأول"}

    result = subprocess.run(
        [sys.executable,  "Video_inserted/build_reference.py", video_path],
        capture_output=True,
        text=True
    )

    print("STDERR:", result.stderr)

    if result.returncode != 0 or not result.stdout.strip():
        return {"status": "error", "msg": result.stderr}

    landmarks = json.loads(result.stdout)

    data = {
        "action": action,
        "image": image_path,
        "video": video_path,
        "landmarks": landmarks
    }

    with open(f"data/{action}.json", "w") as f:
        json.dump(data, f)

    return {"status": "success"}


@app.route("/record_video", methods=["POST"])
def record_video():

    action = request.form.get("action")
    if not action:
       return {"error": "action is missing"}, 400

    import subprocess
    import traceback

    try:
        result = subprocess.run(
         [sys.executable, "Video_from_parent/record_video.py", action],
          capture_output=True,
          text=True
         )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return {"status": "error", "msg": result.stderr}, 500

       
        video_path = f"videos/{action}.mp4"

        return {
        "status": "success",
        "video_path": video_path
         }


    except Exception as e:
        print(traceback.format_exc())
        return {"status": "error", "msg": str(e)}, 500




@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data["username"]
    password = data["password"]
    phone = data["phone"]
    child_name = data["child_name"]
    pair_code = ''.join(
    random.choices(
        string.ascii_uppercase + string.digits,
        k=6
    )
)

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                phone,
                child_name,
                pair_code
            )
            VALUES (?,?,?,?,?)
            """,
            (
                username,
                password,
                phone,
                child_name,
                pair_code
            )
        )

        conn.commit()

        return {
            "status": "success",
            "pair_code": pair_code
        }

    except Exception as e:

        print(e)

        return {
            "status": "exists"
        }

    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, child_name
        FROM users
        WHERE username=? AND password=?
        """,
        (username,password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return {
            "status":"success",
            "user_id": user[0],
            "child_name": user[1]
        }

    return {
        "status":"failed"
    }       


@app.route("/generate_code", methods=["POST"])
def generate_code():

    user_id = request.json["user_id"]

    code = str(random.randint(100000,999999))

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET pair_code=?
        WHERE id=?
        """,
        (code,user_id)
    )

    conn.commit()
    conn.close()

    return {
        "code": code
    }


@app.route("/users")
def users():

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    conn.close()

    return {"users": data}




# @app.route("/reports/<int:user_id>")
# def get_reports(user_id):

#     conn = sqlite3.connect("kids.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT action_name, score, result, test_date
#     FROM reports
#     WHERE user_id = ?
#     ORDER BY id DESC
#     """, (user_id,))

#     rows = cursor.fetchall()

#     conn.close()

#     reports = []

#     for row in rows:
#         reports.append({
#             "action": row[0],
#             "score": row[1],
#             "result": row[2],
#             "date": row[3]
#         })

#     return {"reports": reports}



# @app.route("/parent_login", methods=["POST"])
# def parent_login():

#     data = request.json

#     pair_code = data["pair_code"]

#     conn = sqlite3.connect("kids.db")
#     cursor = conn.cursor()

# 


@app.route("/parent_login", methods=["POST"])
def parent_login():

    pair_code = request.json["pair_code"]

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, child_name
        FROM users
        WHERE pair_code=?
        """,
        (pair_code,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "status": "success",
            "user_id": user[0],
            "child_name": user[1]
        }

    return {
        "status": "failed"
    }

@app.route("/reports/<int:user_id>", methods=["GET"])
def get_reports(user_id):

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            action_name,
            score,
            result,
            test_date
        FROM reports
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    reports = []

    for row in rows:
        reports.append({
            "action_name": row[0],
            "score": row[1],
            "result": row[2],
            "test_date": row[3]
        })

    return jsonify(reports)


@app.route("/child_code/<int:user_id>")
def child_code_page(user_id):

    conn = sqlite3.connect("kids.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pair_code, child_name
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    if user:
        return f"""
        <html>
            <head>
                <title>Child Code</title>
                <style>
                    body {{
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        height:100vh;
                        font-family:Arial;
                        background:#f2f2f2;
                    }}
                    .box {{
                        padding:40px;
                        background:white;
                        border-radius:20px;
                        box-shadow:0 0 10px #ccc;
                        text-align:center;
                    }}
                    h1 {{
                        color:#333;
                    }}
                    .code {{
                        font-size:40px;
                        font-weight:bold;
                        color:blue;
                        margin-top:20px;
                    }}
                </style>
            </head>

            <body>
                <div class="box">
                    <h1>Child Name: {user[1]}</h1>
                    <div class="code">{user[0]}</div>
                </div>
            </body>
        </html>
        """

    return "<h1>User not found</h1>"



@app.route("/")
def home():
    return "Server is running "


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

