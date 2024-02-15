# Project 3

# Importing the necessary libraries

from datetime import datetime
import pandas as pd
import hashlib
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import json
import os
from web3 import Web3
from dotenv import load_dotenv

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

#Loading and connecting to the Web3 provider from the .env file

load_dotenv("Env.env")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER"))) #http://127.0.0.1:7545


# Loading the contract ABI

@st.cache(allow_output_mutation=True)

def load_contract():
    with open(os.path.join("Compiled", "eliteeats_abi.json")) as c:
        contract_abi = json.load(c)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

smart_contract = load_contract()

# Creating a database of restaurants

restaurants = {
    "Azure": {
        "name": "Azure",
        "address": "225 Front St W, Toronto, ON",
        "cost": "0.5",
        "image": "resto_1.jpg",
    },
    "Bangkok Garden": {
        "name": "Bangkok Garden",
        "address": "18 Elm St, Toronto, ON",
        "cost": "0.5",
        "image": "resto_2.jpg"
    },
    "Chica": {
        "name": "Chica",
        "address": "131 Bloor St W, Toronto, ON",
        "cost": "0.5",
        "image": "resto_3.jpg"
    },
    "Amano Pasta": {
        "name": "Amano Pasta",
        "address": "65 Front St W, Toronto, ON",
        "cost": "0.5",
        "image": "resto_4.jpg"
    }
}



# Function to pin files and json to Pinata

def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.read())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json

st.title("Elite Eats")
st.markdown("Welcome to Elite Eats, a decentralized restaurant chain.")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")



# Creating a list to choose restaurant from

st.markdown("## Choose a Restaurant")
restaurant = st.selectbox("Select a Restaurant", list(restaurants.keys()))

def list_restaurant():
    list_r = list(restaurants.values())

    for number in range(len(list_r)):
        st.image(list_r[number]["image"], width=200)
        st.write("Name: ", list_r[number]["name"])
        st.write("Restaurant Address: ", list_r[number]["address"])
        st.write("Cost: ", list_r[number]["cost"], "ETH")
        st.text(" \n")

list_restaurant()

# Streamlit sidebar code
        
st.sidebar.markdown("## Client Account")
st.sidebar.write("Address: ", address)
st.sidebar.write("Balance: ", w3.eth.get_balance(address))

st.sidebar.markdown("## Restaurant Information")

st.sidebar.write("Name: ", [restaurant][0])


number_passes = st.sidebar.number_input("Number of Passes", min_value=1, max_value=10, value=1)

total = float(0.5) * number_passes
st.sidebar.write("Total: ", total, "ETH")

# Setting the NFT gif

st.markdown("## NFT")
nft = st.image("NFT_Card_optimized.gif")

# Streamlit main code to mint NFT

st.markdown("## Mint NFT")

if st.button("Mint NFT", total):

    # Mint the NFT
    tx_hash = smart_contract.functions.mintNFT(
    )

    st.write("Minting NFT...")
    st.balloons()

