
# Sustav za rezervaciju sportskih terena

---

- Projekt izrađen u sklopu kolegija Informacijski sustavi predstavlja web aplikaciju za online rezervaciju sportskih terena.

- Cilj sustava je omogućiti jednostavno, brzo i pregledno upravljanje rezervacijama sportskih objekata putem interneta.

- Aplikacija je razvijena korištenjem programskog jezika Python, HTML & CSS, JS, Flask web okvira, dok se za pohranu podataka koristi baza podataka uz Pony ORM tehnologiju.

- Sustav je prilagođen za rad u Docker-u, što omogućuje jednostavno pokretanje na različitim računalima i serverima.

- Osnovna funkcionalnost aplikacije omogućuje korisnicima pregled dostupnih sportskih terena, provjeru slobodnih termina te online rezervaciju željenog termina.

- Korisnik putem web sučelja može odabrati sportsku lokaciju, datum i vrijeme rezervacije, nakon čega sustav sprema podatke u bazu i prikazuje potvrdu rezervacije.

## UseCase dijagram

![alt text](https://github.com/VedranMiskic/Sustav-za-rezervaciju-sportskih-terena/blob/main/UseCasePhoto.jpeg)

## Kako pokrenuti aplikaciju

---

1. **Instalirajte Docker**

2. **Klonirajte repozitorij:**

    ```bash
    git clone https://github.com/VedranMiskic/Sustav-za-rezervaciju-sportskih-terena.git
    cd "Sustav-za-rezervaciju-sportskih-terena"
    ```

3. **Pokretanje:**

    ```bash
    docker build -t projekt .
    docker ps
    docker run -p 5001:5000 projekt
    ```
