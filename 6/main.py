from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    resp = make_response()
    if request.method == "POST":
        username = request.form["username"]
        error = f"Invalid credentials for user {username}"
        resp = make_response(render_template_string(
            LOGIN_TEMPLATE, error=error))
    else:
        resp = make_response(render_template_string(
            LOGIN_TEMPLATE, error=None))
    resp.set_cookie('session', 's3cr3t_c00k13_v4lu3')
    return resp


LOGIN_TEMPLATE = """
<form method="POST">
  <input name="username" placeholder="Username">
  <input name="password" type="password" placeholder="Password">
  <button type="submit">Login</button>
</form>
  {% if error %}<p style="color:red;">{{ error | safe}}</p>{% endif %}
"""
if __name__ == '__main__':
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0')
