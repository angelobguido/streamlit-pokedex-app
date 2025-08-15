
pokemons = [
    {
        "name": "Pikachu",
        "image": "https://img.pokemondb.net/artwork/large/pikachu.jpg",
        "type": "Electric",
        "description": "Pikachu is an Electric-type Pokémon."
    },
    {
        "name": "Charmander",
        "image": "https://img.pokemondb.net/artwork/large/charmander.jpg",
        "type": "Fire",
        "description": "Charmander is a Fire-type Pokémon."
    },
    {
        "name": "Squirtle",
        "image": "https://img.pokemondb.net/artwork/large/squirtle.jpg",
        "type": "Water",
        "description": "Squirtle is a Water-type Pokémon."
    },
    {
        "name": "Bulbasaur",
        "image": "https://img.pokemondb.net/artwork/large/bulbasaur.jpg",
        "type": "Grass",
        "description": "Bulbasaur is a Grass-type Pokémon."
    }
]

def get_pokemons():
    global pokemons
    return pokemons

def get_pokemon(name: str):
    global pokemons
    for pokemon in pokemons:
        if pokemon["name"].lower() == name.lower():
            return pokemon
    return None

def add_pokemon(pokemon: dict):
    global pokemons
    pokemons.append(pokemon)
    return pokemon

def delete_pokemon(name: str):
    global pokemons
    pokemons = [pokemon for pokemon in pokemons if pokemon["name"].lower() != name.lower()]
    return {"message": "Pokemon deleted successfully"}

def update_pokemon(name: str, updated_pokemon: dict):
    global pokemons
    for i, pokemon in enumerate(pokemons):
        if pokemon["name"].lower() == name.lower():
            pokemons[i] = updated_pokemon
            return updated_pokemon
    return None