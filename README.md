# Power Scale Namer

Generischer Zahlennamen-Generator für Zehnerpotenzen nach der **deutschen langen Skala** (Chuquet / Conway–Wechsler-System).

Das Projekt besteht aus:
- `zahlennamen.py` → Kernlogik zur Konstruktion von Zahlennamen
- `app.py` → GUI-Anwendung (CustomTkinter)

---

## Features

- Generiert Zahlennamen für **beliebig große Exponenten**
- Unterstützt:
  - `10^(6N)` → *N-illion*
  - `10^(6N+3)` → *N-illiarde*
  - Zwischenstufen (*Zehn*, *Hundert*)
- Dynamische Bildung lateinischer Präfixe (rekursiv, unbegrenzt)
- Schritt-für-Schritt-Erklärung der Namenskonstruktion
- Vorschau der Zahl (gekürzt bei großen Exponenten)
- GUI mit Referenztabelle

---

## Beispiel

| Eingabe | Ausgabe |
|--------|--------|
| `10^6` | Million |
| `10^9` | Milliarde |
| `10^12` | Billion |
| `10^42` | Septillion |
| `10^100` | Googol |

---

## Installation

### Voraussetzungen

- Python 3.10+
- Abhängigkeiten:
  ```bash
  pip install customtkinter