import numpy as np

#Zadanie 1
def analiza_testu(filename: str = "answers.txt") -> None:
    raw = np.loadtxt(filename, delimiter=",")
    data = raw[:, 1:]  # pomijamy nr ucznia
    suma_uczniowie = np.sum(data, axis=1)
    srednia = np.mean(suma_uczniowie)
    mediana = np.median(suma_uczniowie)
    print("podstawowe statystyki:\n")
    print(f"srednia liczba poprawnych odpowiedzi: {srednia:.2f}")
    print(f"mediana liczby poprawnych odpowiedzi: {mediana:.2f}")
    odchylenie = np.std(suma_uczniowie)
    cv = (odchylenie / srednia) * 100
    print("\nzroznicowanie wynikow:\n")
    print(f"odchylenie standardowe: {odchylenie:.2f}")
    print(f"wspolczynnik zmienności: {cv:.2f}%")
    n_pytan = data.shape[1]
    procenty = (suma_uczniowie / n_pytan) * 100
    zakresy = {
        "0% - 24%": np.sum((procenty >= 0) & (procenty < 25)),
        "25% - 49%": np.sum((procenty >= 25) & (procenty < 50)),
        "50% - 74%": np.sum((procenty >= 50) & (procenty < 75)),
        "75% - 100%": np.sum((procenty >= 75) & (procenty <= 100)),
    }
    print("\nrozklad procentowy wynikow:\n")
    for przedzial, liczba in zakresy.items():
        print(f"{przedzial}: {liczba} uczniow")
    poprawne_na_pytanie = np.mean(data, axis=0) * 100
    print("\nanaliza wynikow pytan:\n")
    for i, procent in enumerate(poprawne_na_pytanie, start=1):
        print(f"pytanie {i}: {procent:.1f}% uczniow odpowiedzialo poprawnie")


#Zadanie 2
def jacobi(T: np.ndarray) -> np.ndarray:
    T1 = T.copy()
    T1[1:-1, 1:-1] = 0.25 * (
        T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:] + T[1:-1, :-2]
    )
    return T1


def symulacja_brzegi(N: int, iteracje: int = 50) -> None:
    T = np.zeros((N, N))
    T[0, :] = 100
    T[-1, :] = 0
    T[:, 0] = 0
    T[:, -1] = 0
    for k in range(iteracje):
        T = jacobi(T)
        T[0, :] = 100
        T[-1, :] = 0
        T[:, 0] = 0
        T[:, -1] = 0
        if k + 1 in [25, 50]:
            print(
                f"\nzadanie (N={N}): srednia temperatura po {k+1} iteracjach = {np.mean(T):.2f}"
            )


def symulacja_latka(album: str, N: int = 100, iteracje: int = 50) -> None:
    print("\nzadanie 3 (latka 3x3):")
    T = np.full((N, N), 20)
    T[0, :] = 20
    T[-1, :] = 20
    T[:, 0] = 20
    T[:, -1] = 20
    s = sum(int(c) for c in album[-3:])
    print(f"suma cyfr nr albumu = {s}")
    n_s = s if s <= N - 3 else N - 3
    T[n_s : n_s + 3, n_s : n_s + 3] = 100
    for _ in range(iteracje):
        T_new = jacobi(T)
        T_new[0, :] = 20
        T_new[-1, :] = 20
        T_new[:, 0] = 20
        T_new[:, -1] = 20
        T_new[n_s : n_s + 3, n_s : n_s + 3] = 100
        T = T_new
    rows = np.arange(0, N, 20)
    for r in rows:
        print(f"wiersz {r}: {np.mean(T[r, :]):.2f}")
    for c in rows:
        print(f"kolumna {c}: {np.mean(T[:, c]):.2f}")


#Zadanie 3
def generuj_dane():
    temperatura = np.random.uniform(10, 35, (7, 4))
    wilgotnosc = np.random.uniform(30, 90, (7, 4))
    opady = np.random.uniform(0, 25, (7, 4))
    return temperatura, wilgotnosc, opady


def analiza_pogodowa() -> None:
    np.random.seed(42)
    stacje = [generuj_dane() for _ in range(3)]
    print("srednie dzienne pomiary:\n")
    for i, (temp, wilg, opad) in enumerate(stacje, start=1):
        srednia_temp = np.mean(temp, axis=1)
        srednia_wilg = np.mean(wilg, axis=1)
        srednia_opad = np.mean(opad, axis=1)
        print(f"stacja {i}:")
        for dzien in range(7):
            print(
                f" dzien {dzien+1}: temp={srednia_temp[dzien]:.1f}C, wilg={srednia_wilg[dzien]:.1f}%, opad={srednia_opad[dzien]:.1f}mm"
            )
        print()
    max_temp = -np.inf
    min_opad = np.inf
    for st_id, (temp, wilg, opad) in enumerate(stacje, start=1):
        dzien_max = np.argmax(np.mean(temp, axis=1))
        dzien_min_opad = np.argmin(np.mean(opad, axis=1))
        if np.mean(temp, axis=1)[dzien_max] > max_temp:
            max_temp = np.mean(temp, axis=1)[dzien_max]
            stacja_max_temp = st_id
            dzien_max_temp = dzien_max + 1
        if np.mean(opad, axis=1)[dzien_min_opad] < min_opad:
            min_opad = np.mean(opad, axis=1)[dzien_min_opad]
            stacja_min_opad = st_id
            dzien_min_opad = dzien_min_opad + 1
    print(
        f"najwyzsza srednia temperatura: {max_temp:.1f}C w Stacji {stacja_max_temp}, Dzien {dzien_max_temp}"
    )
    print(
        f"najnizsze srednie opady: {min_opad:.1f}mm w Stacji {stacja_min_opad}, Dzien {dzien_min_opad}\n"
    )
    print("dni z ekstremalnymi warunkami:\n")
    for st_id, (temp, wilg, opad) in enumerate(stacje, start=1):
        for dzien in range(7):
            t_srednia = np.mean(temp[dzien])
            w_srednia = np.mean(wilg[dzien])
            o_srednia = np.mean(opad[dzien])
            ekstremalne = []
            if t_srednia > 30:
                ekstremalne.append(f"temp>30C ({t_srednia:.1f}C)")
            if w_srednia > 45:
                ekstremalne.append(f"wilgotnosc>45% ({w_srednia:.1f}%)")
            if o_srednia > 20:
                ekstremalne.append(f"opady>20mm ({o_srednia:.1f}mm)")
            if ekstremalne:
                print(f"stacja {st_id}, dzien {dzien+1}: {'; '.join(ekstremalne)}")
    print("\nkorelacja temperatura vs wilgotnosc:")
    for st_id, (temp, wilg, _) in enumerate(stacje, start=1):
        temp_flat = temp.flatten()
        wilg_flat = wilg.flatten()
        corr = np.corrcoef(temp_flat, wilg_flat)[0, 1]
        print(f"stacja {st_id}: korelacja = {corr:.2f}")


if __name__ == "__main__":
    analiza_testu("answers.txt")
    symulacja_brzegi(30)
    symulacja_brzegi(100)
    symulacja_latka(album="160916", N=100)
    analiza_pogodowa()