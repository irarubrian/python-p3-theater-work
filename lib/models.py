from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="auditions")

    def __init__(self, actor, location, phone, hired=False, role=None):
        self.actor = actor
        self.location = location
        self.phone = phone
        self.hired = hired
        self.role = role  

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String(50))
    auditions = relationship("Audition", back_populates="role")

    def __init__(self, character_name):
        self.character_name = character_name

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) >= 2 else 'no actor has been hired for understudy for this role'

# Database setup
engine = create_engine("sqlite:///theater.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Sample data (unchanged)
role = Role(character_name="Lead Actor")
audition1 = Audition(actor="Mike Wamalwa", location="Kenya", phone=254743435490, role=role)
audition2 = Audition(actor="Bizian Kk", location="China", phone=5463747836, role=role)


session.add_all([role, audition1, audition2])
session.commit()