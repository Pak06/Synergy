-- Creazione delle tabelle per il sistema Synergy

-- 1. Tabella Utenti (Gestisce Admin, PM e TeamMember) [cite: 184, 685]
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    fiscal_code CHAR(16) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL, -- Hash Argon2 o bcrypt [cite: 69]
    role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'ProjectManager', 'TeamMember'))
);

-- 2. Tabella Progetti [cite: 184, 676]
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pm_id INTEGER REFERENCES users(id) ON DELETE SET NULL -- Il Project Manager responsabile [cite: 84]
);

-- 3. Tabella Attività (Tasks) [cite: 184, 735]
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(10) CHECK (priority IN ('Bassa', 'Media', 'Alta')), [cite: 163]
    status VARCHAR(20) DEFAULT 'Da Fare' CHECK (status IN ('Da Fare', 'In Corso', 'Completato')), [cite: 24]
    deadline DATE, [cite: 166]
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL -- Team Member assegnato [cite: 23]
);

-- 4. Tabella Documenti [cite: 184, 646]
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    path TEXT NOT NULL, -- Percorso del file nel sistema storage
    uploaded_by INTEGER REFERENCES users(id)
);

-- 5. Tabella Commenti sui Documenti/Task [cite: 186, 609]
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabella Messaggi (Chat) [cite: 186, 647]
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);
