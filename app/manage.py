from flask_migrate import Migrate
from main import get_app_db
from models import User, Podcast, Progress, Queue, Subscription

from flask_sqlalchemy import SQLAlchemy
    
app, db = get_app_db()
migrate = Migrate(app, db)

if __name__ == '__main__':
  app.run()
