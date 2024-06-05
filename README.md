# Rozpoznawanie i Przetwarzanie Obrazów - projekt

## Analiza

### Cel projektu
Stworzenie pgoramu realizującego funkcję samochodowej kamery cofania. Powinien on:
* wyświetlać na przetwarzanym nagraniu linie pomocnicze
* dysponować konfiguratorem, które umożliwi ustalenie parametrów kamery w tym układu pomocniczych
*  posiadać system wykrywania przeszkód, zrealizowaną przy pomocy wytrenowanej do rozpoznawania przeszkód (np. pieszych, samochodów, słupków) sieci neuronalnej

Do programu dostarczona zostanie również opisująca jego działanie oraz proces wytwórczy dokumentacja.

### Wykorzystane narzędzia
* Implementacja: *Python 3.11.2* & [*OpenCV 4.9*](https://opencv.org/)
* Kontrola wersji: *Git*
* Dokumentacja: *Microsoft Word*

### Materiały pomocnicze
* [Opis wymagań do etapu I](https://docs.google.com/document/d/1exun0MFuKCyoVetX0CCEUEVgM0_71UcGUWTj3PsSVzM/edit)
* [Dysk Google z plikami projektowymi](https://drive.google.com/drive/folders/1cslorDIcwKper_Hi5o5X1zpR4aH1MYiq)

## Struktura repozytorium
* `docs` - dokumentacja projektu
* `gfx` - zdjęcia oraz wideo używane w projekcie
* `src` - skrypty języka Python składające się na tworzoną aplikację
* `study` - materiały pomocnicze, tyczące się możliwości biblioteki *OpenCV*

## Sczegółowe założenia

### Pojazd i kamera
* Projekt zakłada, że obraz będzie zbierany przez kamerę z dowolnego pojazdu.
* Projekt zakłada, że typ kamery jest dowolny. Obejmuje to:
  *  Dowolny kąt widzenia: Kamery mogą mieć różne kąty widzenia, które są dostosowane do konkretnych potrzeb aplikacji.
  *  Rozdzielczość: Kamery mogą mieć różne rozdzielczości, które mogą być dostosowane do wymagań dotyczących jakości obrazu.
  *  Częstotliwość fal: Kamery mogą działać w różnych zakresach fal elektromagnetycznych, takich jak podczerwień, światło widzialne itd.
* Projekt nie narzuca ograniczeń co do umieszczenia kamery na pojeździe. Kamery mogą być umieszczone w dowolnym miejscu na pojeździe, które umożliwia skuteczne zbieranie danych z otoczenia.

### Źródła nagrań
* Projekt umożliwia pozyskiwanie obrazu z rzeczywistych pojazdów znajdujących się w terenie. Jest to proces, w którym obraz jest zbierany w czasie rzeczywistym z kamery zamontowanej na danym pojeździe.
* Projekt zakłada także możliwość pozyskiwania obrazu na bazie nagrań dostępnych w Internecie. Obejmuje to korzystanie z istniejących nagrań wideo, które zostały udostępnione publicznie i mogą być używane do celów analizy.

### Struktura systemu
* System składa się z dwóch głównych elementów: konfiguratora i oprogramowania wykonawczego.
* Konfigurator umożliwia wprowadzanie ustawień dla oprogramowania wykonawczego poprzez interfejs graficzny, który może być np. interfejsem webowym lub inną dowolną technologią.
* Proponowane ustawienia obejmują:
  * Kadrowanie: Możliwość dostosowania obszaru, który ma być analizowany przez oprogramowanie.
  * Edycję linii rysowanych na obrazie w oprogramowaniu wykonawczym: Pozwala na definiowanie linii i innych elementów na obrazie.
  * Wykrywanie obiektów: Ustawienia dotyczące wykrywania określonych obiektów, takich jak inne samochody, rowery, ludzie, ściany, słupki itp.
  * Parametry wykrywania obiektów: Ustawienia dotyczące precyzji i czułości wykrywania obiektów.
  * Metody informowania o wykryciu obiektów: Możliwość wyboru sposobu informowania o wykryciu obiektów, takich jak ramka, alert na ekranie, alert dźwiękowy.
* Oprogramowanie wykonawcze może być uruchamiane z wybraniem źródła obrazu, które może być:
  * Plik wideo.
  * Obraz na żywo z kamery podłączonej do komputera
  * Obraz na żywo z kamery IP połączonej przez sieć, na przykład z kamery zamontowanej na pojeździe
* W trakcie działania oprogramowanie wykonawcze wyświetla obraz z kamery w odpowiednim oknie i rysuje na nim odpowiednie elementy, takie jak linie, alerty, tagi, obwiednie wokół wykrytych obiektów itp.
* Na obrazie można również nakładać elementy developerskie, takie jak liczby i tekst pomocny w analizie działania programu, na przykład procent skuteczności wykrycia danego obiektu.

## Uruchomienie aplikacji (Windows Command Line)

1. Utworzenie wirtualnego środowiska (o ile jeszcze takie nie istnieje) w głównym katalogu projektu.

```bash
py -m venv ../.venv
```

2. Aktywacja wirutalnego środowiska

```bash
../.venv/Scripts/activate.bat
```

3. Zainstalowanie wymaganych zależności.

```bash
pip install -r ../requirements.txt
```

4. Uruchomienie skryptu `main.py`

```bash
py main.py
```

## Jak pobrać playsound
```bash
pip install playsound@git+https://github.com/taconi/playsound
```

## Dzwięk użyty w alertach
soft electronic ping by Metrolynn -- https://freesound.org/s/719210/ -- License: Creative Commons 0
