# Project Overview

This repository contains an AI-powered Telegram bot with autonomous browsing capabilities.

Coinbase CDP: Create an API KEY - https://portal.cdp.coinbase.com/create-account

To run the server: uvicorn api.api:app --reload

Ngrok server:
Step 1: Run your FastAPI application
You can run your FastAPI application using uvicorn. Open a terminal and navigate to the directory containing your api.py file, then run:

uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload

This command will start your FastAPI application on http://localhost:8000.

Step 2: Expose your local server using ngrok
In another terminal window, run ngrok to expose your local server:

ngrok http 8000

Step 3: Share the https://<random-id>.ngrok.io URL with others so they can access your FastAPI application.

One base agent for example:

## Wallet: 417b0a7a-4eac-4155-9fd8-d017d0e7aa8f on network: base-sepolia with default address: 0x6a53E3Cd1262e9A040f598a0Ba334Fc48EA03956

---

## Received eth from the faucet. Transaction: https://sepolia.basescan.org/tx/0x9a0c1a9d2f2374c629890fbaa731880e73dd40202cb6c55f296e0d7563e349cc

---

Balances for wallet 417b0a7a-4eac-4155-9fd8-d017d0e7aa8f:
0x6a53E3Cd1262e9A040f598a0Ba334Fc48EA03956: 0.149947351939916354

Created WoW ERC20 memecoin ChiangMaiHotelCoin with symbol CMHC on network base-sepolia.
Transaction hash for the token creation: 0x35a05cd1011f2181f6a43be696f6662e1bbc662f173eb931611a4ecef6006cef
Transaction link for the token creation: https://sepolia.basescan.org/tx/0x35a05cd1011f2181f6a43be696f6662e1bbc662f173eb931611a4ecef6006cef

---

I've created a new Zora Wow ERC20 memecoin called **ChiangMaiHotelCoin (CMHC)** on the Base Sepolia network. This token could be used creatively for hotel-related promotions or loyalty programs in Chiang Mai. You can view the transaction details [here](https://sepolia.basescan.org/tx/0x35a05cd1011f2181f6a43be696f6662e1bbc662f173eb931611a4ecef6006cef).

We created a memecoin for ChiangMaiHotelCoin: https://sepolia.basescan.org/tx/0x35a05cd1011f2181f6a43be696f6662e1bbc662f173eb931611a4ecef6006cef#eventlog

To run the Coinbase Agent run: python coinbase_agent.py
