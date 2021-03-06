from __future__ import absolute_import
import os
from pgoapi.pokemon import Pokemon
from pgoapi.game_master import PokemonData
import csv


def parse_game_master():
    line_count = 0
    game_master = {}
    with open("GAME_MASTER_POKEMON_v0_2.tsv") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        attributes = []
        for line in tsvreader:
            if line_count == 0:
                attributes = line
                line_count += 1
                continue
            pokemon_data = PokemonData()
            for x in range(0, len(line)):
                setattr(pokemon_data, attributes[x], line[x])
            game_master[int(line[0])] = pokemon_data
    return game_master


def pokemonIVPercentage(pokemon):
    return ((pokemon.get('individual_attack', 0) + pokemon.get('individual_stamina', 0) + pokemon.get(
        'individual_defense', 0) + 0.0) / 45.0) * 100.0


def get_inventory_data(res, poke_names):
    inventory_delta = res['responses']['GET_INVENTORY'].get('inventory_delta', {})
    inventory_items = inventory_delta.get('inventory_items', [])
    pokemons = map(lambda x: Pokemon(x['pokemon_data'], poke_names),
                   filter(lambda x: 'pokemon_data' in x,
                          map(lambda x: x.get('inventory_item_data', {}), inventory_items)))
    inventory_items_pokemon_list = filter(lambda x: not x.is_egg, pokemons)
    inventory_items_pokemon_list = sorted(inventory_items_pokemon_list,
                                          key=lambda pokemon: pokemon.pokemon_data['pokemon_id'])

    return os.linesep.join(map(str, inventory_items_pokemon_list))


DISK_ENCOUNTER = {0: "UNKNOWN",
                  1: "SUCCESS",
                  2: "NOT_AVAILABLE",
                  3: "NOT_IN_RANGE",
                  4: "ENCOUNTER_ALREADY_FINISHED"}
