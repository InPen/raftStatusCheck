# run.py
from app import create_app, db
from app import models  # so models are registered with SQLAlchemy when we run migrations later

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
