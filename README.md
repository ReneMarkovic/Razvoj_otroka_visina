# Višina Otroka

To je preprosta aplikacija za izračun in analizo pričakovane višine otroka glede na višino staršev ter starost otroka. Aplikacija uporablja podatke Svetovne zdravstvene organizacije (WHO) za izračun percentilnih krivulj rasti otrok.

# Zmožnosti aplikacije

Aplikacija omogoča naslednje funkcionalnosti:

- **Vnos podatkov:** Uporabnik lahko vpiše višino matere, višino očeta, spol otroka ter starost otroka v letih in mesecih.

- **Izračun percentila:** Aplikacija izračuna pričakovani percentil rasti otroka glede na višino staršev in starost otroka.

- **Grafični prikaz rezultatov:** Aplikacija prikaže grafični prikaz različnih percentilnih krivulj rasti otrok ter prikazuje dejansko višino otroka glede na starost.

- **Napoved nadaljnje rasti:** Aplikacija omogoča tudi napoved nadaljnje rasti otroka glede na njegovo trenutno višino ter predvideno percentilno krivuljo.

- **Prenos poročila:** Po analizi aplikacija omogoča prenos poročila v obliki PDF datoteke, ki vsebuje rezultate in grafični prikaz.

# Namestitev in zagon aplikacije

Klonirajte ta GitHub repozitorij na svoj računalnik.

V ukazni vrstici ali terminalu se premaknite v mapo z repozitorijem.

Namestite potrebne odvisnosti s pomočjo ukaza `pip install -r requirements.txt`.

Zaženite aplikacijo s pomočjo ukaza `streamlit run app.py`.

Aplikacija bo dostopna na lokalnem računalniku preko naslova `http://localhost:8501`.

# Tehnične zahteve
Aplikacija je napisana v Pythonu in uporablja naslednje ključne tehnologije:

Streamlit: Orodje za ustvarjanje interaktivnih aplikacij s pomočjo Pythona.
Pandas: Knjižnica za obdelavo in analizo podatkov.
Plotly: Knjižnica za ustvarjanje interaktivnih grafov in vizualizacij.
Matplotlib: Knjižnica za ustvarjanje statičnih in dinamičnih grafov.
NumPy: Knjižnica za znanstveno računanje in delo z numeričnimi podatki.

# Prispevanje
Veselimo se vašega prispevanja k izboljšanju te aplikacije! Če želite prispevati, sledite naslednjim korakom:

Forkajte ta GitHub repozitorij.

Naredite spremembe in izboljšave v svojem lokalnem repozitoriju.

Oddajte pull zahtevo (Pull Request) s svojimi spremembami za pregled.

Vaša pull zahteva bo pregledana in vključena v glavni repozitorij, če bo ustrezala smernicam prispevanja.

# Licenca
Ta aplikacija je licencirana pod MIT licenco. Prosim, preberite datoteko LICENSE za več informacij.