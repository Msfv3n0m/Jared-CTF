from flask import Flask, abort, request, render_template_string

app = Flask(__name__)


@app.route('/', methods=['GET'])
def no_filter():

    payload = request.args.get('payload')

    template = '''
        <!DOCTYPE html>
        <html>
          <body>
            <p>''' + payload + '''</p>
          </body>
        </html>'''

    return render_template_string(template)


if __name__ == '__main__':
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0')
