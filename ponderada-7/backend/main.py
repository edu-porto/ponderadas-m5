from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from flask_cors import CORS
from datetime import datetime
import pydobot
from serial.tools import list_ports


app = Flask(__name__)
CORS(app) 
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

# Função para adicionar logs
def add_log(message):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.insert({'date': current_date, 'user_action': message})




############### ROTAS DO ROBÔ ############### 

# Listas as portas seriais disponíveis
available_ports = list_ports.comports()

# Pede para o usuário escolher uma das portas disponíveis
choose_door = available_ports[0].device  # For simplicity, I'm assuming the first port

@app.route('/move-robot', methods=['POST'])
def move_robot():
    data = request.json
  
    if request.content_type != 'application/json':
        return jsonify({"message": "Unsupported media type"}), 415

    if "x" not in data or "y" not in data or "z" not in data:
        return jsonify({"message": "Coordenadas x, y e z são necessárias."}), 400

    robo = pydobot.Dobot(port=choose_door, verbose=False)

    try:
        x = float(data["x"])
        y = float(data["y"])
        z = float(data["z"])
        r = float(data["r"])
        if x < 200 and y < 200 and z < 200:
            robo.move_to(x, y, z, r, wait=True)
            robo.close()    
            add_log("Robot moved to coordinates: ({}, {}, {})".format(x, y, z))

            return jsonify({"x": x, "y": y, "z": z, "r":r}), 200
        else:
            add_log("Robot couldn't be moved to coordinates: ({}, {}, {})".format(x, y, z))
            return jsonify({"message": "As coordenadas devem ser menores que 200."}), 400

    except ValueError:
        return jsonify({"message": "Entrada inválida. Por favor, insira um número inteiro válido."}), 400
    



@app.route('/reset-robot', methods=['POST'])
def reset_robot():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    # Valores recomendados pelo fabricante
    robo.move_to(220, 0, -6.5, 0, wait=True)
    add_log("Robot reset to default position")

    return jsonify({"message": "Robô resetado"}), 200

@app.route('/turn-on', methods=['POST'])
def turn_on_tool():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    robo.suck(True)
    add_log("Robot tool turned on")

    return jsonify({"message": "Atuador ligado"}), 200

@app.route('/turn-off', methods=['POST'])
def turn_off_tool():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    robo.suck(False)
    add_log("Robot tool turned off")

    return jsonify({"message": "Atuador desligado"}), 200

@app.route('/get-position', methods=['POST'])
def get_current_position():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    posicao_atual = robo.pose()
    return jsonify({"posicao_atual": posicao_atual}), 200

if __name__ == "__main__":
    app.run(debug=True)

