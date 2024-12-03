from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'animals.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL COLLATE NOCASE
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appendages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id INTEGER,
        type TEXT NOT NULL,
        numm INTEGER NOT NULL,
        FOREIGN KEY (animal_id) REFERENCES animals(id)
    )
    ''')

def animaldef(cursor):
    animals_data = [
        ('Собака',),
        ('Кошка',),
        ('Лошадь',),
        ('Птица',),
        ('Змея',),
        ('Рыба',),
        ('Человек',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO animals (name) VALUES (?)", animals_data)

    kon_data = [
        (1, 'лапы', 4),
        (2, 'лапы', 4),
        (3, 'копыта', 4),
        (4, 'крылья', 2),
        (5, None, 0),
        (6, 'плавники', 5),
        (7, 'ноги', 2)
    ]
    cursor.executemany("INSERT OR IGNORE INTO appendages (animal_id, type, numm) VALUES (?, ?, ?)", kon_data)

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
        a.name AS animal_name,
        ap.type AS appendage_type,
        ap.numm AS appendage_count
    FROM animals a
    LEFT JOIN appendages ap ON a.id = ap.animal_id
    WHERE a.name = ?
    """, (animal_name,))
    animal_details = cursor.fetchall()
    conn.close()
    
    if animal_details:
        result = []
        for detail in animal_details:
            result.append({
                'animal_name': detail['animal_name'],
                'appendage_type': detail['appendage_type'],
                'appendage_count': detail['appendage_count']
            })
        return jsonify(result)
    else:
        return jsonify({'error': 'Животное не найдено'})

if __name__ == '__main__':
    conn = get_db_connection()
    cursor = conn.cursor()
    create_tables(cursor)
    animaldef(cursor)
    conn.commit()
    conn.close()
    app.run(debug=True, port=5001)