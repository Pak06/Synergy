# synergy_backend.py - Versione Estesa
# Aggiungere alle importazioni: from datetime import datetime

# --- GESTORE DOCUMENTI (Scenario 4.2 RAD) ---
@app.route('/projects/<int:project_id>/documents', methods=['POST'])
@jwt_required()
def upload_document(project_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    # Inserimento metadati file e percorso (Vincolo SDD 3.4)
    cur.execute('INSERT INTO documents (name, path, project_id, uploaded_by) VALUES (%s, %s, %s, %s)',
                (data['fileName'], data['filePath'], project_id, get_jwt_identity()['id']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Documento caricato e indicizzato"}), 201

# --- GESTORE COMMENTI (Caso d'uso PostComment) ---
@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(task_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO comments (task_id, user_id, content, timestamp) VALUES (%s, %s, %s, %s)',
                (task_id, get_jwt_identity()['id'], data['content'], datetime.now()))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Commento aggiunto"}), 201

# --- AMMINISTRAZIONE (Caso d'uso ManageUsers) ---
@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if get_jwt_identity()['role'] != 'Admin':
        return jsonify({"error": "Solo gli Admin possono eliminare utenti"}), 403
    
    conn = get_db_connection()
    cur = conn.cursor()
    # Rispetto del GDPR: eliminazione definitiva dei dati (Diritto all'Oblio)
    cur.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Utente eliminato per conformità GDPR"}), 200
