from flask import Flask, render_template, request, redirect, flash

from pony.orm import *

from datetime import datetime

import database

from models import *


app = Flask(__name__)

app.secret_key = "moja_tajna_sifra"


@app.route("/statistika")
@db_session
def statistika():

    obrisi_stare_rezervacije()

    sve_rezervacije = Rezervacija.select()

    ukupno = len(sve_rezervacije)

    nogomet = 0
    kosarka = 0
    padel = 0
    tenis = 0
    badminton = 0

    danasnje_rezervacije = 0


    for rezervacija in sve_rezervacije:

        if rezervacija.sport == "Nogomet":

            nogomet += 1


        elif rezervacija.sport == "Košarka":

            kosarka += 1


        elif rezervacija.sport == "Padel":

            padel += 1


        elif rezervacija.sport == "Tenis":

            tenis += 1


        elif rezervacija.sport == "Badminton":

            badminton += 1

        if rezervacija.datum == datetime.today().date():

            danasnje_rezervacije += 1


    return render_template(

        "statistika.html",

        nogomet=nogomet,

        kosarka=kosarka,

        padel=padel,

        tenis=tenis,

        badminton=badminton,

        ukupno=ukupno,

        danasnje_rezervacije=danasnje_rezervacije
    )


@app.route("/pretraga")
@db_session
def pretraga():

    obrisi_stare_rezervacije()

    sport_filter = request.args.get("sport")

    datum_filter = request.args.get("datum")


    sve_rezervacije = sorted(

        Rezervacija.select(),

        key=lambda r: (

            r.datum,

            r.vrijeme_od

        )
    )

    filtrirane_rezervacije = []


    for rezervacija in sve_rezervacije:

        sport_ok = True

        datum_ok = True



        if sport_filter and sport_filter != "Svi":

            if rezervacija.sport != sport_filter:

                sport_ok = False



        if datum_filter:

            datum_obj = datetime.strptime(

                datum_filter,

                "%Y-%m-%d"

            ).date()


            if rezervacija.datum != datum_obj:

                datum_ok = False



        if sport_ok and datum_ok:

            filtrirane_rezervacije.append(

                rezervacija
            )


    return render_template(

        "pretraga.html",

        rezervacije=filtrirane_rezervacije,

        danas=datetime.today().strftime("%Y-%m-%d")
    )


@app.route("/upravljanje")
@db_session
def upravljanje():

    obrisi_stare_rezervacije()

    rezervacije = sorted(

        Rezervacija.select(),

        key=lambda r: (

            r.datum,

            r.vrijeme_od

        )
    )

    return render_template(

        "upravljanje.html",

        rezervacije=rezervacije,

        danas=datetime.today().strftime("%Y-%m-%d")
    )

@app.route("/obrisi/<int:id>")
@db_session
def obrisi(id):

    rezervacija = Rezervacija.get(id=id)

    if rezervacija:

        rezervacija.delete()

        flash("Rezervacija obrisana!")

    return redirect("/upravljanje")



@app.route("/spremi_izmjene/<int:id>", methods=["POST"])
@db_session
def spremi_izmjene(id):

    rezervacija = Rezervacija.get(id=id)


    rezervacija.korisnik = request.form["korisnik"]

    rezervacija.sport = request.form["sport"]

    rezervacija.datum = datetime.strptime(
        request.form["datum"],
        "%Y-%m-%d"
    ).date()

    rezervacija.vrijeme_od = request.form["vrijeme_od"]

    rezervacija.vrijeme_do = request.form["vrijeme_do"]

    vrijeme_od_obj = datetime.strptime(

        rezervacija.vrijeme_od,

        "%H:%M"

        ).time()


    vrijeme_do_obj = datetime.strptime(

        rezervacija.vrijeme_do,

        "%H:%M"

        ).time()


    trajanje = (

        datetime.combine(datetime.today(), vrijeme_do_obj)

        -

        datetime.combine(datetime.today(), vrijeme_od_obj)

        ).seconds / 3600



    if rezervacija.sport == "Nogomet":

        if trajanje <= 2:

            rezervacija.cijena = 30

        else:

            rezervacija.cijena = 60




    elif rezervacija.sport == "Košarka":

        if trajanje <= 2:

            rezervacija.cijena = 20

        else:

            rezervacija.cijena = 40



    elif rezervacija.sport == "Padel":

        if trajanje <= 2:

            rezervacija.cijena = 15

        else:

            rezervacija.cijena = 30



    elif rezervacija.sport == "Tenis":

        if trajanje <= 2:

            rezervacija.cijena = 18

        else:

            rezervacija.cijena = 36



    elif rezervacija.sport == "Badminton":

        if trajanje <= 2:

            rezervacija.cijena = 10

        else:

            rezervacija.cijena = 20


    flash("Rezervacija uređena!")

    return redirect("/upravljanje")




@app.route("/")
@db_session
def home():

    obrisi_stare_rezervacije()

    rezervacije = sorted(

        Rezervacija.select(),

        key=lambda r: (

            r.datum,

            r.vrijeme_od

        )
    )

    return render_template(

        "index.html",
        rezervacije=rezervacije,
        danas=datetime.today().strftime("%Y-%m-%d")

    )




@app.route("/rezervacija", methods=["POST"])
@db_session
def rezervacija():

    korisnik = request.form["korisnik"]

    sport = request.form["sport"]

    datum_string = request.form["datum"]

    vrijeme_od = request.form["vrijeme_od"]

    vrijeme_do = request.form["vrijeme_do"]



    datum = datetime.strptime(
        datum_string,
        "%Y-%m-%d"
    ).date()
    

    vrijeme_od_obj = datetime.strptime(
        vrijeme_od,
        "%H:%M"
    ).time()

    vrijeme_do_obj = datetime.strptime(
        vrijeme_do,
        "%H:%M"
    ).time()

    trenutni_datum = datetime.today().date()

    trenutno_vrijeme = datetime.now().time()

    if datum.weekday() == 6:

        flash("Nedjeljom nije moguće rezervirati termine!")

        return redirect("/")

    if datum < datetime.today().date():

        flash("Nije moguće rezervirati prošle datume!")

        return redirect("/")
    
    if datum == trenutni_datum:

        if vrijeme_od_obj <= trenutno_vrijeme:

            flash("Nije moguće rezervirati prošlo vrijeme!")

            return redirect("/")
    

    if vrijeme_od_obj >= vrijeme_do_obj:

        flash(
            "Vrijeme završetka mora biti nakon početnog vremena!"
        )

        return redirect("/")


    

    postojece_rezervacije = Rezervacija.select()


    trajanje = (

        datetime.combine(datetime.today(), vrijeme_do_obj)

        -

        datetime.combine(datetime.today(), vrijeme_od_obj)

        ).seconds / 3600



    if sport == "Nogomet":

        if trajanje <= 2:

            ukupna_cijena = 30

        else:

            ukupna_cijena = 60


    elif sport == "Košarka":

        if trajanje <= 2:

            ukupna_cijena = 20

        else:

            ukupna_cijena = 40



    elif sport == "Padel":

        if trajanje <= 2:

            ukupna_cijena = 15

        else:

            ukupna_cijena = 30



    elif sport == "Tenis":

        if trajanje <= 2:

            ukupna_cijena = 18

        else:

            ukupna_cijena = 36



    elif sport == "Badminton":

        if trajanje <= 2:

            ukupna_cijena = 10

        else:

            ukupna_cijena = 20
    

    for rezervacija in postojece_rezervacije:

        if (
            rezervacija.sport == sport
            and rezervacija.datum == datum
        ):

            postojece_od = datetime.strptime(
                rezervacija.vrijeme_od,
                "%H:%M"
            ).time()

            postojece_do = datetime.strptime(
                rezervacija.vrijeme_do,
                "%H:%M"
            ).time()


           

            if (
                vrijeme_od_obj < postojece_do
                and vrijeme_do_obj > postojece_od
            ):

                flash("Termin je već zauzet!")

                return redirect("/")



    Rezervacija(

        korisnik=korisnik,

        sport=sport,

        datum=datum,

        vrijeme_od=vrijeme_od,

        vrijeme_do=vrijeme_do,

        cijena=ukupna_cijena
    )


    flash("Rezervacija uspješno dodana!")

    return redirect("/")

def obrisi_stare_rezervacije():

    trenutno_vrijeme = datetime.now()

    sve_rezervacije = Rezervacija.select()

    for rezervacija in sve_rezervacije:

        kraj_termina = datetime.strptime(

            f"{rezervacija.datum} {rezervacija.vrijeme_do}",

            "%Y-%m-%d %H:%M"

        )


        if trenutno_vrijeme > kraj_termina:

            rezervacija.delete()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
