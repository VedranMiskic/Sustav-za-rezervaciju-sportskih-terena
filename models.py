from pony.orm import *

from datetime import date

db = Database()

class Rezervacija(db.Entity):

    id = PrimaryKey(int, auto=True)

    korisnik = Required(str)

    sport = Required(str)

    datum = Required(date)

    vrijeme_od = Required(str)

    vrijeme_do = Required(str)

    cijena = Required(float)