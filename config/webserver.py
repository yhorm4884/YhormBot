from __init__ import Flask, Thread

app = Flask('')


@app.route('/')
def home():
    return "El bot está activo"


def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
