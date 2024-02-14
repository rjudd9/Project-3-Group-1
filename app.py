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
    "Azure": [
        "Azure",
        "225 Front St W, Toronto, ON"
        "0.5",
        "image": "resto1.jpg",
    ],
    "Bangkok Garden": [
        "Bangkok Garden",
        "18 Elm St, Toronto, ON",
        "0.5",
        "resto2.jpg"
    ],
    "Chica": [
        "Chica",
        "131 Bloor St W, Toronto, ON",
        "0.5",
        "resto3.jpg"
    ],
    "Amano Pasta": [
        "Amano Pasta",
        "65 Front St W, Toronto, ON",
        "0.5",
        "resto4.jpg"
    ]
}



# Function to pin files and json to Pinata

def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

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

    for number in range(len(restaurants)):
        st.image(list_r["image"], width=200)
        st.write("Name: ", list[number][0])
        st.write("Restaurant Address: ", list[number][1])
        st.write("Cost: ", list[number][2], "ETH")
        st.text(" \n")

list_restaurant()

# Streamlit sidebar code
        
st.sidebar.markdown("## Client Account")
st.sidebar.write("Address: ", address)
st.sidebar.write("Balance: ", w3.eth.get_balance(address))

st.sidebar.markdown("## Restaurant Information")

st.sidebar.write("Name: ", restaurants[restaurant][0])
st.sidebar.write("Address: ", restaurants[restaurant][1])
st.sidebar.write("Cost: ", restaurants[restaurant][2])

number_passes = st.sidebar.number_input("Number of Passes", min_value=1, max_value=10, value=1)

total = float(restaurants[restaurant][2]) * number_passes
st.sidebar.write("Total: ", total, "ETH")

# Setting the NFT gif

st.markdown("## NFT")
nft = st.image("NFT_Card_optimized.gif")

# Streamlit main code to mint NFT

st.markdown("## Mint NFT")

if st.button("Mint NFT"):
    # Use the `pin_artwork` helper function to pin the file to IPFS
    artwork_ipfs_hash, token_json = pin_artwork(restaurants[restaurant][0], open(nft, "rb"))

    # Mint the NFT
    tx_hash = smart_contract.functions.mintNFT(
        address,
        artwork_ipfs_hash,
        total
    ).transact()

    st.write("Minting NFT...")
    st.write("Transaction Hash: ", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.balloons()
