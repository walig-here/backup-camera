# Uruchomienie aplikacji (Windows Command Line)

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
