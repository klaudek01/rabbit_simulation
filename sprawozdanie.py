import csv
import random

class Królik:
    def __init__(self, id_królika, kolor, genotyp, id_rodzica1=None, id_rodzica2=None):
        self.id_królika = id_królika
        self.kolor = kolor
        self.genotyp = genotyp
        self.id_rodzica1 = id_rodzica1
        self.id_rodzica2 = id_rodzica2

class Populacja:
    def __init__(self):
        self.króliki = []

    def wczytaj_z_pliku_txt(self, nazwa_pliku):
        with open(nazwa_pliku, 'r', encoding='utf-8') as plik_txt:
            pierwszy_wiersz = True
            for linia in plik_txt:
                if pierwszy_wiersz:  # Pomiń pierwszy wiersz, jeśli jest to nagłówek
                    pierwszy_wiersz = False
                    continue
                
                id_rodzica1, id_rodzica2, id_królika, genotyp, kolor = linia.strip().split(',')
                id_rodzica1 = None if id_rodzica1 == 'None' else id_rodzica1
                id_rodzica2 = None if id_rodzica2 == 'None' else id_rodzica2
                królik = Królik(id_królika, kolor, genotyp, id_rodzica1, id_rodzica2)
                self.króliki.append(królik)



    def wyświetl_statystyki_kolorów(self):
        kolory = {}
        for królik in self.króliki:
            if królik.kolor in kolory:
                kolory[królik.kolor] += 1
            else:
                kolory[królik.kolor] = 1
        wynik = '\n'.join(f"Kolor: {kolor}, Liczba: {liczba}" for kolor, liczba in kolory.items())
        return wynik

    def sprawdź_genotyp(self, id_królika):
        for królik in self.króliki:
            if królik.id_królika == id_królika:
                return królik.genotyp
        return "Nie znaleziono królika o podanym ID."

class Symulator:

    def __init__(self):
        self.populacja = Populacja()
        self.historia_krzyżowań = []
        self.ostatnie_id = 99
        self.nazwa_pliku_danych = None

    def wczytaj_dane(self, nazwa_pliku):
        if not nazwa_pliku.endswith('.txt'):
            nazwa_pliku += '.txt'  # Automatycznie dodaj rozszerzenie .txt, jeśli jest to konieczne
        try:
            self.populacja.wczytaj_z_pliku_txt(nazwa_pliku)
            self.nazwa_pliku_danych = nazwa_pliku
            print("Dane wczytane pomyślnie.")
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}.")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania pliku: {e}")  
        
    def losuj_genotyp(self, genotyp_rodzica1, genotyp_rodzica2):
        genotyp_potomka = ""

        
        allele_rodzic1 = [genotyp_rodzica1[i:i+2] for i in range(0, len(genotyp_rodzica1), 2)]
        allele_rodzic2 = [genotyp_rodzica2[i:i+2] for i in range(0, len(genotyp_rodzica2), 2)]

        
        for i in range(2):
            genotyp_potomka += random.choice(allele_rodzic1[i]) + random.choice(allele_rodzic2[i])

        return genotyp_potomka

    def wykonaj_krzyżówkę(self, id_rodzica1, id_rodzica2):
        if not self.nazwa_pliku_danych:
            return "Nie wczytano danych o królikach."

        rodzic1 = rodzic2 = None
        for krolik in self.populacja.króliki:
            if krolik.id_królika == id_rodzica1:
                rodzic1 = krolik
            if krolik.id_królika == id_rodzica2:
                rodzic2 = krolik

        if not rodzic1 or not rodzic2:
            return "Nieprawidłowe ID rodziców."

        liczba_potomków = random.randint(1, 12)
        id_potomstwa = []

        for _ in range(liczba_potomków):
            nowy_id = self.znajdź_następne_wolne_id()
            if nowy_id is None:
                return "Osiągnięto maksymalny zakres ID."

            nowy_genotyp = self.losuj_genotyp(rodzic1.genotyp, rodzic2.genotyp)
            nowy_kolor = self.determinuj_kolor(nowy_genotyp)
            nowy_królik = Królik(nowy_id, nowy_kolor, nowy_genotyp)
            self.populacja.króliki.append(nowy_królik)
            id_potomstwa.append(nowy_id)

            # Zapisz do pliku tekstowego
            with open(self.nazwa_pliku_danych, 'a', encoding='utf-8') as plik_txt:
                # Sprawdź, czy plik jest pusty
                plik_txt.seek(0, 2)  # Przesuń wskaźnik na koniec pliku
                if plik_txt.tell() > 0:  # Jeśli plik nie jest pusty
                    plik_txt.write('\n')  # Dodaj nową linię przed zapisaniem nowego wpisu

                plik_txt.write(f"{id_rodzica1},{id_rodzica2},{nowy_id},{nowy_genotyp},{nowy_kolor}")

        self.historia_krzyżowań.append({
            'id_rodzica1': id_rodzica1,
            'id_rodzica2': id_rodzica2,
            'id_potomstwa': id_potomstwa
        })

        return id_potomstwa

    def determinuj_kolor(self, genotyp):
        mapa_kolorów = {
            "AABB": "czarny",
            "AABb": "rudy",
            "AAbB": "rudy",
            "AAbb": "srebrny",
            "aaBB": "czerwony",
            "AaBb": "szary",
            "aAbB": "szary",
            "AaBB": "podpalany",
            "aABB": "podpalany",
            "aabb": "biały",
            "aaBb": "biały z czarnymi kropkami",
            "Aabb": "czarny z białymi kropkami"
        }

        return mapa_kolorów.get(genotyp, "niezdefiniowany")


    def zapisz_historię_do_pliku_txt(self, nazwa_pliku):
        with open(nazwa_pliku, 'a', encoding='utf-8') as file:
            file.write('ID Rodzica 1,ID Rodzica 2,ID Potomka,Genotyp Potomka,Kolor Potomka\n')

            for wpis in self.historia_krzyżowań:
                id_rodzica1 = wpis['id_rodzica1']
                id_rodzica2 = wpis['id_rodzica2']
                for id_potomka in wpis['id_potomstwa']:
                    potomek = [k for k in self.populacja.króliki if k.id_królika == id_potomka]
                    if potomek:
                        file.write(f"{id_rodzica1},{id_rodzica2},{potomek[0].id_królika},{potomek[0].genotyp},{potomek[0].kolor}\n")
                    else:
                        nowe_id = self.znajdź_następne_wolne_id()  
                        if nowe_id:
                            file.write(f"{id_rodzica1},{id_rodzica2},{nowe_id},Nieznany genotyp,Niezdefiniowany kolor\n")

    def znajdź_następne_wolne_id(self):
        zajęte_id = {int(k.id_królika[1:]) for k in self.populacja.króliki}
        for wpis in self.historia_krzyżowań:
            for id_potomka in wpis['id_potomstwa']:
                if id_potomka.startswith('#'):
                    zajęte_id.add(int(id_potomka[1:]))

        for i in range(1000):
            if i not in zajęte_id:
                return f'#{i:03d}'
        return None  # Jeśli wszystkie ID są zajęte

def menu():
    symulator = Symulator()
    while True:
        print("\nWitaj w symulatorze krzyżowania królików!")
        print("1. Wczytaj dane o królikach z pliku")
        print("2. Wyświetl statystyki kolorów")
        print("3. Sprawdź genotyp królika")
        print("4. Wykonaj krzyżówkę")
        print("5. Zapisz historię krzyżowań do pliku")
        print("6. Zakończ program")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            nazwa_pliku = input("Podaj nazwę pliku (bez rozszerzenia .txt): ")  # Zaktualizowana instrukcja dla użytkownika
            symulator.wczytaj_dane(nazwa_pliku)
        elif wybor == '2':
            symulator.populacja.wyświetl_statystyki_kolorów()
        elif wybor == '3':
            id_królika = input("Podaj ID królika: ")
            genotyp = symulator.populacja.sprawdź_genotyp(id_królika)
            print(f"Genotyp królika {id_królika}: {genotyp}" if genotyp else "Nie znaleziono królika.")
        elif wybor == '4':
            id_rodzica1 = input("Podaj ID pierwszego rodzica: ")
            id_rodzica2 = input("Podaj ID drugiego rodzica: ")
            wynik_krzyżówki = symulator.wykonaj_krzyżówkę(id_rodzica1, id_rodzica2)
            if isinstance(wynik_krzyżówki, list):
                print(f"Krzyżówka zakończona sukcesem. ID potomków: {', '.join(wynik_krzyżówki)}")
            else:
                print(wynik_krzyżówki)
        elif wybor == '5':
            nazwa_pliku = input("Podaj nazwę pliku do zapisu historii krzyżowań (z rozszerzeniem .txt): ")
            if not nazwa_pliku.endswith('.txt'):
                nazwa_pliku += '.txt'
            symulator.zapisz_historię_do_pliku_txt(nazwa_pliku)
            print(f"Zapisano historię krzyżowań do pliku {nazwa_pliku}.")
        elif wybor == '6':
            print("Dziękujemy za skorzystanie z programu!")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")

if __name__ == "__main__":
    menu()

