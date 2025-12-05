# Grocery Hub

This project contains:
- Flask backend (port 3001)
- React frontend (port 3000)

Features:
- User registration/login (simple token)
- Product catalog (list/search/filter/detail)
- Cart operations (add/update/remove)
- Checkout -> Order creation
- Order history per user

Backend:
- Python + Flask + Flask-Smorest + SQLAlchemy (SQLite)
- API docs at /docs

Run backend:
1. cd grocery_backend
2. python3 -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. cp .env.example .env (and edit as needed)
5. FLASK_RUN_PORT=3001 python run.py

Frontend:
1. cd ../grocery-hub-220328-220338/grocery_frontend
2. npm install
3. cp .env.example .env
4. npm start

Set REACT_APP_API_BASE to http://localhost:3001 if needed.

Open http://localhost:3000 to use the app.
