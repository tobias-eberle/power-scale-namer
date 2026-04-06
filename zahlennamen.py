"""
Generischer Zahlennamen-Generator (deutsche lange Skala).

System (kurz):
  10^(6N)      = N-illion          (N=2 → Billion)
  10^(6N+3)    = N-illiarde        (N=2 → Billiarde)
  10^(6N+1)    = Zehn N-illionen
  10^(6N+2)    = Hundert N-illionen
  10^(6N+4)    = Zehn N-illiarden
  10^(6N+5)    = Hundert N-illiarden

Die lateinische Vorsilbe für N wird aus Einer-, Zehner- und Hunderter-
Komponenten zusammengesetzt (Reihenfolge: Einer + Zehner + Hunderter).
Für N ≥ 1000 wird N in Dreiergruppen zerlegt und mit "lli" verbunden;
leere Gruppen werden durch "ni" markiert (Chuquet-Rekursion).
"""

# ─────────────────────────────────────────────────────────────────────────
# Lateinische Vorsilben-Komponenten
# ─────────────────────────────────────────────────────────────────────────

# Einer 1-9, wenn N nur aus Einern besteht (N=1..9 → Million..Nonillion)
ONES_STANDALONE = {
    1: "mi", 2: "bi", 3: "tri", 4: "quadri", 5: "quinti",
    6: "sexti", 7: "septi", 8: "okti", 9: "noni",
}

# Hunderter (immer auf "i" endend)
HUNDREDS = {
    1: "zenti", 2: "duzenti", 3: "trezenti", 4: "quadringenti",
    5: "quingenti", 6: "seszenti", 7: "septingenti", 8: "oktingenti",
    9: "nongenti",
}

# Zehner-Stämme: (terminal "i"-Form, nicht-terminal "a"-Form)
TENS_STEMS = {
    1: ("deki", "dezi"),
    2: ("viginti", "viginti"),
    3: ("triginti", "triginta"),
    4: ("quadraginti", "quadraginta"),
    5: ("quinquaginti", "quinquaginta"),
    6: ("sexaginti", "sexaginta"),
    7: ("septuaginti", "septuaginta"),
    8: ("oktoginti", "oktoginta"),
    9: ("nonaginti", "nonaginta"),
}


def _tens_prefix(t: int, is_terminal: bool, is_alone: bool) -> str:
    """Vorsilbe für die Zehner-Stelle.
    is_terminal = es folgt KEIN Hunderter-Bestandteil
    is_alone    = es gibt KEINE Einer-Stelle in dieser Gruppe
    """
    if t == 0:
        return ""
    if t == 1:
        # "deki" nur, wenn die Zehnerstelle die einzige Komponente ist (N=10)
        return "deki" if (is_alone and is_terminal) else "dezi"
    if t == 2:
        return "viginti"
    return TENS_STEMS[t][0] if is_terminal else TENS_STEMS[t][1]


def _ones_compound(u: int, next_char: str) -> str:
    """Einer-Vorsilbe in Verbindung mit folgender Zehner/Hunderter-Komponente.

    Die Form hängt vom Anlaut der nachfolgenden Komponente ab
    (vereinfachte Conway-Wechsler-Regel)."""
    if u == 0:
        return ""
    fixed = {1: "un", 2: "duo", 4: "quattuor", 8: "okto"}
    if u in fixed:
        return fixed[u]

    c = (next_char or "").lower()
    # "harter" Anlaut: o (oktoginta), z (zenti), n (nonaginta/nongenti), c
    hard = c in ("o", "z", "c", "n")

    if u == 3:
        return "tres" if c in ("s", "o", "c", "z") else "tre"
    if u == 5:
        # vor "dezi" → "quin", sonst → "quinqua"
        return "quin" if c == "d" else "quinqua"
    if u == 6:
        return "ses" if hard else "sex"
    if u == 7:
        return "septem" if hard else "septen"
    if u == 9:
        return "novem" if hard else "noven"
    return ""


def _build_group_prefix(n: int, is_final_group: bool = True) -> str:
    """Lateinische Vorsilbe für 1 ≤ n ≤ 999 (eine Dreiergruppe).

    is_final_group: True wenn diese Gruppe direkt vor 'llion'/'lliarde' steht;
                    False wenn 'lli' (nächste Gruppe) folgt.
    Wirkt sich nur auf den Sonderfall N=10 aus:
       - finale Gruppe : 'deki' → 'Dekillion'
       - Zwischengruppe: 'dezi' → 'Dezillinillion'
    """
    assert 1 <= n <= 999, n

    u = n % 10
    t = (n // 10) % 10
    h = (n // 100) % 10

    has_t = t > 0
    has_h = h > 0

    # Reine Einer (N=1..9)
    if not has_t and not has_h:
        return ONES_STANDALONE[u]

    parts: list[str] = []

    # Einer (Form abhängig von folgender Komponente)
    if u > 0:
        if has_t:
            next_char = _tens_prefix(t, not has_h, False)[0]
        else:
            next_char = HUNDREDS[h][0]
        parts.append(_ones_compound(u, next_char))

    # Zehner
    if has_t:
        parts.append(
            _tens_prefix(
                t,
                is_terminal=not has_h,
                is_alone=(u == 0) and is_final_group,
            )
        )

    # Hunderter
    if has_h:
        parts.append(HUNDREDS[h])

    return "".join(parts)


def build_latin_prefix(n: int) -> str:
    """Lateinische Vorsilbe für beliebiges n ≥ 1 (rekursive Tausendergruppen)."""
    if n < 1:
        raise ValueError("n muss ≥ 1 sein")
    if n <= 999:
        return _build_group_prefix(n)

    # Zerlege N in Dreiergruppen (Basis 1000, von rechts)
    groups = []
    temp = n
    while temp > 0:
        groups.append(temp % 1000)
        temp //= 1000

    # Baue von höchster zu niedrigster Gruppe, getrennt durch "lli"
    parts: list[str] = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        is_final = i == 0
        if g == 0:
            parts.append("ni")
        else:
            parts.append(_build_group_prefix(g, is_final_group=is_final))
        if i > 0:
            parts.append("lli")
    return "".join(parts)


# ─────────────────────────────────────────────────────────────────────────
# Hauptfunktion: Potenz → Name
# ─────────────────────────────────────────────────────────────────────────

SMALL_NAMES = {
    0: "Eins", 1: "Zehn", 2: "Hundert", 3: "Tausend",
    4: "Zehntausend", 5: "Hunderttausend",
}

SPECIAL_ALIASES = {
    100: "Googol",
}


def power_to_name(exponent: int) -> str:
    """10^exponent → deutscher Zahlenname (lange Skala)."""
    if exponent < 0:
        return "Ungültig (negativer Exponent)"
    if exponent in SMALL_NAMES:
        return SMALL_NAMES[exponent]

    n, r = divmod(exponent, 6)
    prefix = build_latin_prefix(n)

    base = prefix + ("llion" if r < 3 else "lliarde")
    base = base[0].upper() + base[1:]

    if r in (0, 3):
        return base

    # Plural: "...llion" → "...llionen", "...lliarde" → "...lliarden"
    plural = base + "en" if base.endswith("on") else base + "n"
    return ("Zehn " if r in (1, 4) else "Hundert ") + plural


def explain_construction(exponent: int) -> str:
    """Schritt-für-Schritt-Erklärung wie der Name aufgebaut wird."""
    if exponent < 0:
        return ""
    if exponent in SMALL_NAMES:
        return f"10^{exponent} ist eine Grundzahl: {SMALL_NAMES[exponent]}"

    n, r = divmod(exponent, 6)
    lines = [
        f"Exponent E = {exponent:,}",
        f"N = E ÷ 6 = {n:,}    (Rest {r})",
    ]

    rest_meaning = {
        0: "→ N-illion",
        1: "→ Zehn N-illionen   (10 × N-illion)",
        2: "→ Hundert N-illionen   (100 × N-illion)",
        3: "→ N-illiarde   (1000 × N-illion)",
        4: "→ Zehn N-illiarden",
        5: "→ Hundert N-illiarden",
    }
    lines.append(rest_meaning[r])

    if n <= 999:
        u, t, h = n % 10, (n // 10) % 10, (n // 100) % 10
        comp = []
        if h: comp.append(f"H={h}·100")
        if t: comp.append(f"Z={t}·10")
        if u: comp.append(f"E={u}")
        if comp:
            lines.append("Zerlegung von N: " + " + ".join(comp))
    else:
        groups = []
        temp = n
        while temp > 0:
            groups.append(temp % 1000)
            temp //= 1000
        groups.reverse()
        # Bei sehr großem N nur die ersten/letzten Gruppen anzeigen
        if len(groups) <= 8:
            shown = str(groups)
        else:
            shown = f"[{groups[0]}, {groups[1]}, …, {groups[-2]}, {groups[-1]}] ({len(groups)} Gruppen)"
        lines.append(f"N = {n:,} → Tausender-Gruppen (MSB→LSB): {shown}")
        lines.append("Verbindung der Gruppen mit 'lli', leere Gruppen = 'ni'")

    prefix = build_latin_prefix(n)
    suffix = "llion" if r < 3 else "lliarde"
    if len(prefix) <= 200:
        lines.append(f"Lateinische Vorsilbe: '{prefix}'")
        lines.append(f"+ Endung '{suffix}'")
    else:
        lines.append(f"Lateinische Vorsilbe: '{prefix[:80]}…{prefix[-40:]}'  ({len(prefix)} Zeichen)")
        lines.append(f"+ Endung '{suffix}'")
    return "\n".join(lines)


def number_preview(exponent: int, max_chars: int = 90) -> str:
    """Stelle die Zahl als '1' gefolgt von Nullen dar (gekürzt bei Bedarf)."""
    if exponent < 0:
        return ""
    if exponent + 1 <= max_chars:
        return "1" + "0" * exponent
    head = "1" + "0" * (max_chars - 25)
    return f"{head} … ({exponent:,} Nullen insgesamt)"
