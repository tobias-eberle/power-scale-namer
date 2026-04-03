"""
Power Scale Namer – Zeige den deutschen Zahlennamen zu beliebigen Zehnerpotenzen.
Basiert auf dem deutschen Zahlennamen-System (lange Skala).
Quelle: mathetreff-online.de
"""

import customtkinter as ctk

# ---------------------------------------------------------------------------
# Datenbank: Potenz (Anzahl Nullen) → deutscher Zahlenname
# ---------------------------------------------------------------------------
POWER_NAMES: dict[int, str] = {
    0: "Eins",
    1: "Zehn",
    2: "Hundert",
    3: "Tausend",
    4: "Zehntausend",
    5: "Hunderttausend",
    6: "Million",
    9: "Milliarde",
    12: "Billion",
    15: "Billiarde",
    18: "Trillion",
    21: "Trilliarde",
    24: "Quadrillion",
    27: "Quadrilliarde",
    30: "Quintillion",
    33: "Quintilliarde",
    36: "Sextillion",
    39: "Sextilliarde",
    42: "Septillion",
    45: "Septilliarde",
    48: "Oktillion",
    51: "Oktilliarde",
    54: "Nonillion",
    57: "Nonilliarde",
    60: "Dekillion",
    63: "Dekilliarde",
    66: "Undezillion",
    69: "Undezilliarde",
    72: "Duodezillion",
    75: "Duodezilliarde",
    78: "Tredezillion",
    81: "Tredezilliarde",
    84: "Quattuordezillion",
    86: "Quattuordezilliarde",
    90: "Quindezillion",
    93: "Quindezilliarde",
    96: "Sexdezillion",
    99: "Sexdezilliarde",
    100: "Googol",
    102: "Septendezillion",
    108: "Oktodezillion",
    114: "Novendezillion",
    120: "Vigintillion",
    180: "Trigintillion",
    240: "Quadragintillion",
    300: "Quinquagintillion",
    360: "Sexagintillion",
    420: "Septuagintillion",
    480: "Oktogintillion",
    540: "Nonagintillion",
    600: "Zentillion",
    1_200: "Duzentillion",
    1_800: "Trezentillion",
    2_400: "Quadringentillion",
    3_000: "Quingentillion",
    3_600: "Seszentillion",
    4_200: "Septingentillion",
    4_800: "Oktingentillion",
    5_400: "Nongentillion",
    6_000: "Milliatillion",
    12_000: "Billinillion",
    18_000: "Trillinillion",
    24_000: "Quadrillinillion",
    30_000: "Quintillinillion",
    36_000: "Sextillinillion",
    42_000: "Septillinillion",
    48_000: "Oktillinillion",
    54_000: "Nonillinillion",
    60_000: "Dezillinillion",
    66_000: "Undezillinillion",
    6_000_000: "Millinillinillion",
    6_000_000_000: "Millinillinillinillion",
}

# Sortierte Liste für die Nachbar-Suche
_SORTED_POWERS = sorted(POWER_NAMES.keys())


def lookup_power(exponent: int) -> str:
    """Gibt den Zahlennamen für 10^exponent zurück, oder die nächsten Nachbarn."""
    if exponent < 0:
        return "Bitte eine nicht-negative Zahl eingeben."

    if exponent in POWER_NAMES:
        return POWER_NAMES[exponent]

    # Nächst-kleinere und nächst-größere bekannte Potenz finden
    lower = None
    upper = None
    for p in _SORTED_POWERS:
        if p < exponent:
            lower = p
        elif p > exponent:
            upper = p
            break

    parts = [f"Kein exakter Name für 10^{exponent} bekannt."]
    if lower is not None:
        parts.append(f"  ↓ 10^{lower:,} = {POWER_NAMES[lower]}")
    if upper is not None:
        parts.append(f"  ↑ 10^{upper:,} = {POWER_NAMES[upper]}")
    return "\n".join(parts)


def format_number_preview(exponent: int, max_digits: int = 80) -> str:
    """Zeigt 1 gefolgt von Nullen, ggf. abgekürzt."""
    if exponent <= max_digits:
        return "1" + "0" * exponent
    return "1" + "0" * 20 + f" … ({exponent:,} Nullen insgesamt)"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Zehnerpotenzen – Zahlennamen")
        self.geometry("750x620")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Header
        ctk.CTkLabel(
            self, text="Zahlennamen für Zehnerpotenzen",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(18, 4))

        ctk.CTkLabel(
            self,
            text="Gib einen Exponenten ein (10^n) und sieh den deutschen Zahlennamen.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 12))

        # Input frame
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=4)

        ctk.CTkLabel(input_frame, text="10 ^", font=ctk.CTkFont(size=18)).pack(
            side="left", padx=(0, 6)
        )

        self.entry = ctk.CTkEntry(
            input_frame, width=180, font=ctk.CTkFont(size=18),
            placeholder_text="z.B. 6"
        )
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", lambda _: self._on_lookup())

        ctk.CTkButton(
            input_frame, text="Nachschlagen", command=self._on_lookup,
            font=ctk.CTkFont(size=14),
        ).pack(side="left")

        # Result area
        self.result_name = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=28, weight="bold"),
            wraplength=680,
        )
        self.result_name.pack(pady=(20, 4))

        self.result_details = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=14),
            text_color="gray", wraplength=680, justify="left",
        )
        self.result_details.pack(pady=(0, 10))

        self.result_number = ctk.CTkTextbox(
            self, height=60, font=ctk.CTkFont(family="Courier", size=13),
            wrap="char", state="disabled",
        )
        self.result_number.pack(padx=20, fill="x")

        # Table of all known names
        ctk.CTkLabel(
            self, text="Alle bekannten Zahlennamen",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(16, 4))

        table_frame = ctk.CTkScrollableFrame(self, height=220)
        table_frame.pack(padx=20, pady=(0, 14), fill="both", expand=True)

        # Column headers
        header_font = ctk.CTkFont(size=12, weight="bold")
        ctk.CTkLabel(table_frame, text="Potenz", font=header_font, width=120, anchor="w").grid(
            row=0, column=0, padx=4, sticky="w"
        )
        ctk.CTkLabel(table_frame, text="Nullen", font=header_font, width=80, anchor="w").grid(
            row=0, column=1, padx=4, sticky="w"
        )
        ctk.CTkLabel(table_frame, text="Zahlenname", font=header_font, width=300, anchor="w").grid(
            row=0, column=2, padx=4, sticky="w"
        )

        row_font = ctk.CTkFont(size=12)
        for i, exp in enumerate(_SORTED_POWERS, start=1):
            ctk.CTkLabel(table_frame, text=f"10^{exp:,}", font=row_font, anchor="w").grid(
                row=i, column=0, padx=4, sticky="w"
            )
            ctk.CTkLabel(table_frame, text=f"{exp:,}", font=row_font, anchor="w").grid(
                row=i, column=1, padx=4, sticky="w"
            )
            ctk.CTkLabel(table_frame, text=POWER_NAMES[exp], font=row_font, anchor="w").grid(
                row=i, column=2, padx=4, sticky="w"
            )

    def _on_lookup(self) -> None:
        raw = self.entry.get().strip().replace(".", "").replace(",", "")
        if not raw:
            return

        try:
            exponent = int(raw)
        except ValueError:
            self.result_name.configure(text="Ungültige Eingabe")
            self.result_details.configure(text="Bitte eine ganze Zahl eingeben.")
            return

        result = lookup_power(exponent)

        if exponent in POWER_NAMES:
            self.result_name.configure(text=POWER_NAMES[exponent])
            self.result_details.configure(
                text=f"10^{exponent:,}  –  eine Zahl mit {exponent:,} Nullen"
            )
        else:
            self.result_name.configure(text="—")
            self.result_details.configure(text=result)

        # Number preview
        preview = format_number_preview(exponent)
        self.result_number.configure(state="normal")
        self.result_number.delete("1.0", "end")
        self.result_number.insert("1.0", preview)
        self.result_number.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()
