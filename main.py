import random
import sys
#Dane wejściowe
liczba_klas = 3
liczba_dni = 2
liczba_godzin_dziennie = 3

#Definicja zajęć
zajecia = ['Matematyka', 'Fizyka', 'Chemia', 'Historia','okienko']
dni_tygodnia = ['Poniedziałek','Wtorek','Środa','Czwartek','Piątek']
godziny_zajec = ['8:00-8:45','8:55-9:40','9:50-10:35','10:45-11:30','11:50-12:35','12:45-13:30','13:40-14:25','14:35-15:15']
#Możliwość zapisywania do pliku
original_stdout = sys.stdout
#Funkcja celu - ocena planu zajęć
def ocena_planu(plan):
    ocena = 0
    #sprawdzenie długości plany zajęć
    for i in range(liczba_klas):
        if(len(plan[i])!=liczba_dni*liczba_godzin_dziennie):
            ocena=-1000
            return ocena
    #sprawdzanie powtarzalności zajęć
    for x in range(liczba_klas):
        list = []
        for y in range(liczba_dni*liczba_godzin_dziennie):
            if(plan[x][y]!='okienko'):
                if(plan[x][y] in list):
                    ocena-=1
                else:
                    list.append(plan[x][y])
    #sprawdzenie czy każdy przedmiot jest nauczany w klasie
    for x in range(liczba_klas):
        for y in zajecia:
            if(y not in plan[x]):
                ocena-=1
    #jak najmniesza liczba okienek obok siebie
    for x in range(liczba_klas):
        for y in range(liczba_dni*liczba_godzin_dziennie):
            if(y%liczba_godzin_dziennie!=0):
                if(plan[x][y]=='okienko'):
                    if(plan[x][y-1]!='okienko'):
                        new_tmp=y
                        while True:
                            new_tmp+=1
                            if(new_tmp%liczba_godzin_dziennie==0):
                                break
                            if(plan[x][new_tmp]!='okienko'):
                                ocena-=1
                                break
    #brak możliwości aby jeden przedmiot był nauczany w tym samym czasie
    for x in range(liczba_klas):
        for y in range(liczba_dni*liczba_godzin_dziennie):
            for z in range(x+1,liczba_klas):
                if plan[x][y]==plan[z][y]:
                    if plan[x][y]!='null':
                        ocena-=1
    return ocena

#Tworzenie populacji początkowej
def tworz_populacje(rozmiar_populacji):
    populacja = []
    for _ in range(rozmiar_populacji):
        plan = []
        for _ in range(liczba_klas):
            dzien = []
            for _ in range(liczba_dni*liczba_godzin_dziennie):
                godzina = random.choice(zajecia)
                dzien.append(godzina)
            plan.append(dzien)
        populacja.append(plan)
    return populacja

#Krzyżowanie dwóch planów zajęć
def krzyzowanie(plan1, plan2):
    nowy_plan = []
    for i in range(liczba_klas):
        nowy_dzien = []
        for j in range(liczba_dni*liczba_godzin_dziennie):
            if random.random() < 0.5:
                nowy_dzien.append(plan1[i][j])
            else:
                nowy_dzien.append(plan2[i][j])
        nowy_plan.append(nowy_dzien)
    return nowy_plan

#Mutowanie planu zajęć
def mutacja(plan, prawdopodobienstwo_mutacji):
    posiadane_zajecia=[]
    for i in range(liczba_klas):
        for j in range(liczba_dni*liczba_godzin_dziennie):
            if random.random() < prawdopodobienstwo_mutacji:
                plan[i][j] = random.choice(zajecia)
    return plan

#Algorytm genetyczny
def algorytm_genetyczny(liczba_iteracji, rozmiar_populacji, prawdopodobienstwo_mutacji):
    populacja = tworz_populacje(rozmiar_populacji)
    for _ in range(liczba_iteracji):
        oceny = [ocena_planu(plan) for plan in populacja]
        najlepszy_plan = populacja[oceny.index(max(oceny))]
        najlepsza_ocena = max(oceny)
        nowa_populacja = [najlepszy_plan]

        while len(nowa_populacja) < rozmiar_populacji:
            rodzic1 = random.choice(populacja)
            rodzic2 = random.choice(populacja)
            dziecko = krzyzowanie(rodzic1, rodzic2)
            dziecko = mutacja(dziecko, prawdopodobienstwo_mutacji)
            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    return najlepszy_plan,najlepsza_ocena


#Wypisanie końcowego planu
def wypisz_plan(plan_zajec):
    for x in range(liczba_klas):
        print("Plan klasy: "+str(x+1))
        for y in range(0,liczba_dni*liczba_godzin_dziennie,liczba_godzin_dziennie):
            print(plan_zajec[x][y:y+liczba_godzin_dziennie])
#Lepsze wypisywanie planu
def zapisz_plan(plan_zajec):
    with open('plan_zajec.txt', 'w') as f:
        tmp =0
        sys.stdout = f
        for x in range(liczba_klas):
            print("Plan dla klasy: "+str(x+1))
            tmp = -1*liczba_godzin_dziennie
            for y in range(liczba_dni):
                print(dni_tygodnia[y])
                tmp+=liczba_godzin_dziennie
                for z in range(liczba_godzin_dziennie):
                    if(plan_zajec[x][z+tmp]!='okienko'):
                        print(godziny_zajec[z]+" "+plan_zajec[x][z+tmp])
                    else:
                        print(godziny_zajec[z])
            print("")
        sys.stdout = original_stdout

#Użycie algorytmu genetycznego
while True:
    plan_zajec,najlepsza_ocena = algorytm_genetyczny(10000, 100, 0.2)
    print(plan_zajec)
    print(najlepsza_ocena)
    if(najlepsza_ocena==0):
        break
wypisz_plan(plan_zajec)
zapisz_plan(plan_zajec)

