from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies', overlaps='freebies')

    @classmethod
    def oldest_company(cls, session: Session):
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, item_name, value, session: Session):
        freebie = Freebie(
            dev_id=dev.id,
            company_id=self.id,
            item_name=item_name,
            value=value
        )
        session.add(freebie)
        session.commit()
        return freebie

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs', overlaps='freebies')

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie, session: Session):
        if freebie.dev == self:
            freebie.dev = other_dev
            session.add(freebie)
            return True
        return False

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies', overlaps='companies,devs')
    company = relationship('Company', back_populates='freebies', overlaps='companies,devs')

    def print_details(self):
        dev_name = self.dev.name if self.dev else "Unknown Dev"
        company_name = self.company.name if self.company else "Unknown Company"
        return f"{dev_name} owns a {self.item_name} from {company_name}"

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
