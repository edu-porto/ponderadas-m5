from flask import Flask, jsonify
from tinydb import TinyDB, Query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize TinyDB and create a sample database
db = TinyDB('db.json')


# Define a route to fetch data
@app.route('/data/<int:data_id>', methods=['GET'])
def get_data(data_id):
    # Query the database for the data with the specified ID
    Data = Query()
    result = db.get(Data.id == data_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
