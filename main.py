import streamlit as st
import pandas as pd
import numpy as np
import app.pokemon_db as pokemon

st.title('Pokedex')
st.header('Pokemons')

pokemons = pokemon.get_pokemons()

with st.sidebar:
    with st.form("add_pokemon_form", clear_on_submit=True):
        st.subheader("Adicionar Pokemon")
        new_pokemon_name = st.text_input("Nome do Pokemon:")
        new_pokemon_image = st.text_input("URL da Imagem:")
        new_pokemon_type = st.text_input("Tipo do Pokemon:")
        new_pokemon_description = st.text_area("Descrição do Pokemon:")
        add_pokemon_button = st.form_submit_button("Adicionar Pokemon")

    with st.form("Atualizar Pokemon", clear_on_submit=True):
        update_pokemon_name = st.text_input("Nome do Pokemon a ser atualizado:")
        update_pokemon_image = st.text_input("Nova URL da Imagem:")
        update_pokemon_type = st.text_input("Novo Tipo do Pokemon:")
        update_pokemon_description = st.text_area("Nova Descrição do Pokemon:")
        update_pokemon_button = st.form_submit_button("Atualizar Pokemon")

    with st.form("Deletar Pokemon", clear_on_submit=True):
        delete_pokemon_name = st.text_input("Nome do Pokemon a ser deletado:")
        delete_pokemon_button = st.form_submit_button("Deletar Pokemon")

if add_pokemon_button:
    if new_pokemon_name and new_pokemon_image and new_pokemon_type and new_pokemon_description:
        pokemon.add_pokemon({
            "name": new_pokemon_name,
            "image": new_pokemon_image,
            "type": new_pokemon_type,
            "description": new_pokemon_description
        })
        st.success(f"Pokemon '{new_pokemon_name}' adicionado com sucesso!")
        st.rerun()
    else:
        st.warning("Por favor, preencha todos os campos.")

if update_pokemon_button:
    if update_pokemon_name:
        pokemon_to_update = pokemon.get_pokemon(update_pokemon_name)
        if not pokemon_to_update:
            st.error(f"Pokemon '{update_pokemon_name}' não encontrado.")
        else:
            if not update_pokemon_image:
                update_pokemon_image = pokemon_to_update["image"]
            if not update_pokemon_type:
                update_pokemon_type = pokemon_to_update["type"]
            if not update_pokemon_description:
                update_pokemon_description = pokemon_to_update["description"]
        pokemon.update_pokemon(update_pokemon_name, {
            "image": update_pokemon_image,
            "type": update_pokemon_type,
            "description": update_pokemon_description
        })
        st.success(f"Pokemon '{update_pokemon_name}' atualizado com sucesso!")
        st.rerun()
    else:
        st.warning("Por favor, preencha o nome do pokemon que deseja atualizar.")

if delete_pokemon_button:
    if delete_pokemon_name:
        pokemon.delete_pokemon(delete_pokemon_name)
        st.success(f"Pokemon '{delete_pokemon_name}' deletado com sucesso!")
        st.rerun()
    else:
        st.warning("Por favor, preencha o nome do pokemon que deseja deletar.")


search_query = st.text_input("Buscar:", placeholder="Coloque o nome do pokemon...")
if search_query:
    st.write(f"Buscando por '{search_query}':")
    searched_pokemon = pokemon.get_pokemon(search_query)
    if searched_pokemon:
        pokemons = [searched_pokemon]
    else:
        st.write("Nenhum pokemon encontrado.")
        pokemons = []

num_columns = 3

cols = st.columns(num_columns)

for index, p in enumerate(pokemons):
    col = cols[index % num_columns]

    with col:
        with st.container(border=True):
            st.subheader(p['name'])
            st.image(p['image'], width=150, use_column_width='auto') 
            st.write(f"**Tipo:** {p['type']}")
            st.write(p['description'])