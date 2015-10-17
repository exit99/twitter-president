from extensions import Base, engine
from models import *


Base.metadata.create_all(engine)
print("Tables create!")
