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
