from flask import Flask, render_template
import subprocess

app = Flask(__name__)

def run_kubectl_cmd(command):
    try:
        result = subprocess.check_output(["sudo" , "kubectl"] + command.split(), stderr=subprocess.STDOUT)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error running command: {e.output.decode('utf-8')}"

@app.route("/")
def index():
    pods = run_kubectl_cmd("get pods -o wide --all-namespaces")
    nodes = run_kubectl_cmd("get nodes -o wide")
    return render_template("index.html", pods=pods, nodes=nodes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

