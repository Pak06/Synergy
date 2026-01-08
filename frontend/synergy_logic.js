const API_URL = "http://127.0.0.1:5000";

// Gestione Login (Task 1 RAD)
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('role', data.role);
            
            // Reindirizzamento basato sul ruolo (Vincolo RAD 4.1)
            if (data.role === 'ProjectManager') {
                window.location.href = 'pm_dashboard.html';
            } else {
                window.location.href = 'tm_dashboard.html';
            }
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Errore connessione:", error);
    }
});

// Funzione per aggiornare lo stato di una task (Scenario 4.2 RAD)
async function changeTaskStatus(taskId, newStatus) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/tasks/${taskId}/status`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({status: newStatus})
    });

    if (response.ok) {
        alert("Stato aggiornato con successo!");
        location.reload();
    }
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}
