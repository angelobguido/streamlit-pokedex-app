import sqlite3
from app.pokemon_examples import get_pokemon_examples

DB_FILE = "pokemons.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemons (
                name TEXT PRIMARY KEY,
                image TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        
        cursor.execute("SELECT COUNT(name) FROM pokemons")
        if cursor.fetchone()[0] == 0:
            print("Database is empty, populating with initial data...")
            initial_pokemons = get_pokemon_examples()
            cursor.executemany(
                'INSERT INTO pokemons (name, image, type, description) VALUES (:name, :image, :type, :description)',
                initial_pokemons
            )
        
        conn.commit()
    print("Database initialized successfully.")

def get_pokemons():
    with get_db_connection() as conn:
        pokemons_rows = conn.execute('SELECT * FROM pokemons').fetchall()
        return [dict(row) for row in pokemons_rows]

def get_pokemon(name: str):
    with get_db_connection() as conn:
        pokemon_row = conn.execute(
            'SELECT * FROM pokemons WHERE lower(name) = ?', 
            (name.lower(),)
        ).fetchone()
        
        if pokemon_row is None:
            return None
        return dict(pokemon_row)

def add_pokemon(pokemon: dict):
    try:
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO pokemons (name, image, type, description) VALUES (?, ?, ?, ?)',
                (pokemon['name'], pokemon['image'], pokemon['type'], pokemon['description'])
            )
            conn.commit()
            return pokemon
    except sqlite3.IntegrityError:
        return {"error": f"Pokemon '{pokemon['name']}' already exists."}

def delete_pokemon(name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pokemons WHERE lower(name) = ?', (name.lower(),))
        conn.commit()
        
        if cursor.rowcount == 0:
            return {"message": "Pokemon not found"}
        return {"message": "Pokemon deleted successfully"}

def update_pokemon(name: str, updated_data: dict):
    if not get_pokemon(name):
        return None

    set_clause = ", ".join([f"{key} = ?" for key in updated_data.keys()])
    values = list(updated_data.values())
    values.append(name.lower())

    query = f"UPDATE pokemons SET {set_clause} WHERE lower(name) = ?"
    
    with get_db_connection() as conn:
        conn.execute(query, tuple(values))
        conn.commit()

    new_name = updated_data.get('name', name)
    return get_pokemon(new_name)


init_db()