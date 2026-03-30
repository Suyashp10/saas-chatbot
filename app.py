from flask import Flask, request, jsonify, render_template
from bot import get_response
import uuid

#FLASK SETUP
app = Flask(__name__)

#ROUTES 

@app.route("/")
def index():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    return render_template("index.html", session_id=session_id)

    
@app.route('/chat', methods=['POST'])
def chat(): 
    data = request.get_json() 

    session_id = data.get('session_id') if data else None
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please type a message."}), 400

    response = get_response(session_id, message)
    return jsonify({"response": response})

#RUN APP
if (__name__ == '__main__'):
    app.run(debug=True)