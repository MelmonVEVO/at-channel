CREATE TABLE IF NOT EXISTS boards (
    uri  VARCHAR(7) NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    new_thread_number INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS threads (
    thread_id INTEGER NOT NULL,
    board VARCHAR(7) NOT NULL,
    bump_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(50),

    PRIMARY KEY (thread_id, board),
    FOREIGN KEY (board) REFERENCES boards(uri)
);

CREATE TABLE IF NOT EXISTS posts (
    thread INTEGER NOT NULL,
    board VARCHAR(7) NOT NULL,
    reply_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    body TEXT NOT NULL,

    PRIMARY KEY (thread, board, reply_id),
    FOREIGN KEY (thread, board) REFERENCES threads(thread_id, board)
);