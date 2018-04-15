import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("gintoki","sakata")
session.add(user)

user = User("jesuisune","shagua")
session.add(user)

user = User("nico","lanoixdecoco")
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()
