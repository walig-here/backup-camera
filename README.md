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

### Dodatkowe założenia
* Program niekoniecznie musi działać na realnym, odstarczanym w czasie rzeczywistym nagraniu z kamery. Priorytetmowym zadaniem będzie zatem wytowrzenie programu, który działać będzie na już gotowych nagraniach.

## Struktura repozytorium
* `docs` - dokumentacja projektu
* `gfx` - zdjęcia oraz wideo używane w projekcie
* `src` - skrypty języka Python składające się na tworzoną aplikację
* `study` - materiały pomocnicze, tyczące się możliwości biblioteki *OpenCV*
