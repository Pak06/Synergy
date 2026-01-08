import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt

app = Flask("Synergy")
CORS(app)
app.config['JWT_SECRET_KEY'] = 'synergy_secure_key' # Da cambiare in produzione
jwt = JWTManager(app)

# Gestore Database PostgreSQL (Vincolo SDD 3.4)
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="synergy_db",
        user="postgres",
        password="your_password"
    )

# --- ROTTE AUTENTICAZIONE (OAuth 2.0 / OpenID compliant) ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Hashing sicuro come da vincoli RAD
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                (data['username'], hashed_pw, data['role'])) # Admin, PM, o TeamMember
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Utente registrato"}), 201

# --- GESTIONE PROGETTI (Per Project Manager) ---
@app.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    user = get_jwt_identity()
    if user['role'] != 'ProjectManager':
        return jsonify({"error": "Accesso negato"}), 403
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO projects (name, description, pm_id) VALUES (%s, %s, %s) RETURNING id',
                (data['name'], data['description'], user['id']))
    project_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Progetto creato", "id": project_id}), 201

# --- GESTIONE TASK (Per Team Member) ---
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
@jwt_required()
def update_task_status(task_id):
    data = request.json # Es: {"status": "In Corso"}
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET status = %s WHERE id = %s', (data['status'], task_id))
    conn.commit()
    # Qui andrebbe integrato il NotificationService via WebSockets (Vincolo SDD 3.6)
    cur.close()
    conn.close()
    return jsonify({"message": "Stato aggiornato"}), 200

if __name__ == '__main__':
    app.run(debug=True)
