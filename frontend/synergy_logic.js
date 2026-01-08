// Gestione aggiornamento stato attività (Task 3 del Test Usabilità)
async function updateTaskStatus(taskId, newStatus) {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            alert("Stato aggiornato! Notifica inviata al Project Manager.");
            location.reload(); // Aggiorna la dashboard
        }
    } catch (error) {
        console.error("Errore nell'aggiornamento:", error);
    }
}

// Funzione per caricamento documenti (Task 4 - RAD)
// Nota: RAD suggerisce di implementare il Drag-and-Drop in futuro
function uploadDocument(projectId) {
    console.log("Apertura interfaccia DocumentUI per il progetto:", projectId);
}
