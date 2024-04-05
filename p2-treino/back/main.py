from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app) 

# Instanciando o banco de dados e os logs  
db = TinyDB('db.json')
logs = TinyDB('logs.json')

# Essa é a rota que cria uma tarefa  
@app.route('/create-task', methods=['POST'])
def create_task():
    # Pega a hora atual
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pega o nome da tarefa no body da requisição
    task_name = request.json.get('task_name')

    # Insere a tarefa no banco de dados
    db.insert({'date': current_date, 'task_name': task_name})

    add_log(message="Task created")

    return jsonify({'message': 'Task created successfully'})

# Essa é a rota que retorna todas as tarefas
@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    tasks = db.all()
    return jsonify(tasks)

# Essa é a rota que retorna uma tarefa específica
@app.route('/get-task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.get(doc_id=task_id)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'})

# Essa é a rota que deleta uma tarefa específica 
@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.get(doc_id=task_id)
    if task:
        db.remove(doc_ids=[task_id])
        add_log(message=f"The task number {task_id} was deleted")

        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'error': 'Task not found'})

# Essa é a rota que atualiza uma tarefa específica 
@app.route('/update-task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.get(doc_id=task_id)
    if task:
        # Pega a hora atual e permite o usuario alterar o nome da tarefa no body da requisição
        updated_task_name = request.json.get('task_name')
        updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.update({'task_name': updated_task_name, 'date': updated_date}, doc_ids=[task_id])
        add_log(message=f"The task number {task_id} was updated to {updated_task_name}")
        return jsonify({'message': 'Task updated successfully'})
    return jsonify({'error': 'Task not found'})

# Função para adicionar logs
def add_log(message):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.insert({'Data e horário': current_date, 'Tipo de requisição': message})

if __name__ == "__main__":
    app.run(debug=True)

