#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie
import os

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'freebies.db')
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    google = Company(name="Google", founding_year=1998)
    microsoft = Company(name="Microsoft", founding_year=1975)
    apple = Company(name="Apple", founding_year=1976)
    session.add_all([google, microsoft, apple])
    session.commit()
    
    alice = Dev(name="Alice")
    bob = Dev(name="Bob")
    charlie = Dev(name="Charlie")
    session.add_all([alice, bob, charlie])
    session.commit()
    
    google_sticker = google.give_freebie(alice, "Sticker", 5, session)
    microsoft_mug = microsoft.give_freebie(bob, "Mug", 10, session)
    apple_tshirt = apple.give_freebie(charlie, "T-Shirt", 20, session)

    print("\nTesting relationships:")
    print(f"Alice's companies: {[c.name for c in alice.companies]}")
    print(f"Google's devs: {[d.name for d in google.devs]}")
    
    print("\nTesting aggregate methods:")
    print(f"Oldest company: {Company.oldest_company(session).name}")
    print(f"Freebie details: {google_sticker.print_details()}")
    
    print("\nTesting give_away:")
    alice.give_away(bob, google_sticker, session)
    session.commit()
    print(f"Bob's freebies: {[f.item_name for f in bob.freebies]}")
    print(f"Alice's freebies: {[f.item_name for f in alice.freebies]}")
    
    print("\nTesting received_one:")
    print(f"Bob received sticker: {bob.received_one('Sticker')}")
    print(f"Charlie received sticker: {charlie.received_one('Sticker')}")
    
    session.close()
