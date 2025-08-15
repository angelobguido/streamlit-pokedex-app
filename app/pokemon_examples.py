import requests

pokemon_list_url = "https://pokeapi.co/api/v2/pokemon/?limit=10"

def get_pokemon_examples():
    response = requests.get(pokemon_list_url)
    data = response.json()

    pokemon_list = data['results']
    pokemon_list_formatted = []

    for pokemon in pokemon_list:
        pokemon_name = pokemon['name']
        print(pokemon_name)
        pokemon_details = requests.get(pokemon['url']).json()
        pokemon_types = str([type['type']['name'] for type in pokemon_details['types']])
        pokemon_image = f"https://img.pokemondb.net/artwork/large/{pokemon_name}.jpg"
        pokemon_description = f"A pokemon of type: {pokemon_types}"
        pokemon_list_formatted.append({
            'name': pokemon_name,
            'image': pokemon_image,
            'type': pokemon_types,
            'description': pokemon_description
        })

    return pokemon_list_formatted
