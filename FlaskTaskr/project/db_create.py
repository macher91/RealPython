from views import db
import models
from datetime import date

db.create_all()
db.session.add(models.Task("Finish this tutorial", date(2015,03, 25), 10, 1))
db.session.add(models.Task("Finish Real Python Course 2", date(2015,03, 25), 10, 1))
db.session.commit()
