import requests
import json
import pandas as pd


def _get_pokemon_base_stats(api_key):
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_stats.json"
    response = requests.get(url, headers={"x-rapidapi-key": api_key})
    df = pd.DataFrame(json.loads(response.text))
    return df


def _get_pokemon_maximum_cp(api_key):
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_max_cp.json"
    response = requests.get(url, headers={"x-rapidapi-key": api_key})
    df = pd.DataFrame(json.loads(response.text))
    return df


def _get_candy_to_evolve(api_key):
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_candy_to_evolve.json"
    response = requests.get(url, headers={"x-rapidapi-key": api_key})
    data = json.loads(response.text)
    df = pd.DataFrame(
        columns=["pokemon_id", "pokemon_name", "form", "candy_required"]
    )
    for v in data.values():
        temp = pd.DataFrame(v)
        if "form" not in temp.columns:
            temp["form"] = None
        temp = temp[["pokemon_id", "pokemon_name", "form", "candy_required"]]
        df = pd.concat([df, temp], axis=0)
    return df


def _get_pokemon_types(api_key):
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_types.json"
    response = requests.get(url, headers={"x-rapidapi-key": api_key})
    df = pd.DataFrame(json.loads(response.text))
    df["type1"] = df["type"].apply(lambda x: x[0])
    df["type2"] = df["type"].apply(lambda x: x[1] if len(x) == 2 else None)
    return df


def get_pokemon_stats(api_key):
    df_stats = _get_pokemon_base_stats(api_key)
    df_stats = df_stats[[
        "pokemon_id", "pokemon_name", "form",
        "base_attack", "base_defense", "base_stamina"
    ]]

    df_cp = _get_pokemon_maximum_cp(api_key)
    df_cp = df_cp[["pokemon_id", "pokemon_name", "form", "max_cp"]]

    df_candy = _get_candy_to_evolve(api_key)

    df_types = _get_pokemon_types(api_key)
    df_types = df_types[[
        "pokemon_id", "pokemon_name", "form", "type1", "type2"
    ]]

    df = pd.merge(df_stats, df_cp, on=["pokemon_id", "pokemon_name", "form"])
    df = pd.merge(df, df_candy, on=["pokemon_id", "pokemon_name", "form"])
    df = pd.merge(df, df_types, on=["pokemon_id", "pokemon_name", "form"])

    return df
