from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'animals.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Для удобного доступа к данным по имени столбца
    return conn

@app.route('/animals', methods=['GET'])
def get_animals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animals")
    animals = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(animals)

@app.route('/animals/<animal_name>', methods=['GET'])
def get_animal(animal_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            a.name,
            ap.type,
            ap.numm
        FROM animals a
        LEFT JOIN appendages ap ON a.id = ap.animal_id
        WHERE a.name = ?
    """, (animal_name,))
    animal = cursor.fetchone()
    conn.close()
    if animal:
        return jsonify(dict(animal))
    else:
        return jsonify({'error': 'Animal not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)