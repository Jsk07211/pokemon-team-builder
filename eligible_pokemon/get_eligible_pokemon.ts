import { SpeciesFormats } from "./format_data.js";
import * as fs from 'fs';

const eligiblePokemon = Object.entries(SpeciesFormats)
    .filter(([_, info]) =>
        info.doublesTier &&
        info.doublesTier !== "Uber" &&
        info.doublesTier !== "AG")
    .map(([pokemon, info]) => [pokemon, info.doublesTier]);

const pokemonDictionary = Object.fromEntries(eligiblePokemon);

const pokemonJson = JSON.stringify(pokemonDictionary, null, 2);
fs.writeFileSync('eligible_pokemon.json', pokemonJson);