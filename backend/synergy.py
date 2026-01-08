import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt

app = Flask("Synergy")
CORS(app)
app.config['JWT_SECRET_KEY'] = 'synergy_secret_key_123' # Usa variabili d'ambiente in produzione
jwt = JWTManager(app)

# Configurazione Database PostgreSQL (Vincolo SDD 3.4)
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="synergy_db",
        user="postgres",
        password="your_password"
    )

# --- AUTENTICAZIONE E REGISTRAZIONE ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Hashing password con algoritmi moderni (Vincolo RAD 3.4)
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (name, surname, username, password, role) VALUES (%s, %s, %s, %s, %s)',
                    (data['name'], data['surname'], data['username'], hashed_pw, data['role']))
        conn.commit()
        return jsonify({"message": "Registrazione completata"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, password, role FROM users WHERE username = %s', (data['username'],))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user[2].encode('utf-8')):
        # Generazione Token JWT con ruolo incluso (Vincolo SDD 3.5)
        access_token = create_access_token(identity={"id": user[0], "username": user[1], "role": user[3]})
        return jsonify({"access_token": access_token, "role": user[3]}), 200
    return jsonify({"error": "Credenziali non valide"}), 401

# --- GESTIONE PROGETTI (Per Project Manager) ---
@app.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    current_user = get_jwt_identity()
    if current_user['role'] != 'ProjectManager':
        return jsonify({"error": "Permessi insufficienti"}), 403
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO projects (name, description, pm_id) VALUES (%s, %s, %s) RETURNING id',
                (data['name'], data['description'], current_user['id']))
    project_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Progetto creato", "project_id": project_id}), 201

# --- AGGIORNAMENTO STATO ATTIVITÀ (Per Team Member) ---
@app.route('/tasks/<int:task_id>/status', methods=['PATCH'])
@jwt_required()
def update_task_status(task_id):
    data = request.json # Es: {"status": "Completato"}
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET status = %s WHERE id = %s', (data['status'], task_id))
    conn.commit()
    cur.close()
    conn.close()
    # Qui andrebbe l'invio della notifica real-time (Vincolo SDD 3.6)
    return jsonify({"message": "Stato attività aggiornato"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
