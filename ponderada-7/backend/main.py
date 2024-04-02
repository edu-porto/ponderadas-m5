from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
db = TinyDB('db.json')

# Esta é a rota que cria um log 
@app.route('/create-log', methods=['POST'])
def add_log():
    # Generate current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Example log message
    log_message = "Hello log "

    # Insert log into TinyDB
    db.insert({'date': current_date, 'user_action': log_message})

    return jsonify({'message': 'Log added successfully'})


# Esta é a rota que retorna todos os logs 
@app.route('/get-logs', methods=['GET'])
def get_logs():
    logs = db.all()
    return jsonify(logs)

# Esta é a rota que retorna um log específico
@app.route('/get-log/<int:log_id>', methods=['GET'])
def get_log(log_id):
    log = db.get(doc_id=log_id)
    if log:
        return jsonify(log)
    return jsonify({'error': 'Log not found'})

# Esta é a rota que atualiza um log específico
@app.route('/update-log/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    log = db.get(doc_id=log_id)
    if log:
        # Pega a hora automatica e permite o usuario alterar a mensagem no body da requisição
        updated_message = request.json.get('log_message')
        updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.update({'user_action': updated_message, 'date': updated_date}, doc_ids=[log_id])
        return jsonify({'message': 'Log updated successfully'})
    return jsonify({'error': 'Log not found'})

# Esta é a rota que deleta um log específico
@app.route('/delete-log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    log = db.get(doc_id=log_id)
    if log:
        db.remove(doc_ids=[log_id])
        return jsonify({'message': 'Log deleted successfully'})
    return jsonify({'error': 'Log not found'})

if __name__ == '__main__':
    app.run(debug=True)