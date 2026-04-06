"""
Power Scale Namer – UI für den generischen Zahlennamen-Generator.
Logik siehe ``zahlennamen.py``.
"""

import customtkinter as ctk

from zahlennamen import (
    SPECIAL_ALIASES,
    build_latin_prefix,
    explain_construction,
    number_preview,
    power_to_name,
)

# Beispiele für die Referenztabelle (werden generisch berechnet)
REFERENCE_EXPONENTS = [
    0, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11,
    12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57,
    60, 63, 66, 72, 78, 84, 90, 96, 100, 102, 108, 114, 120,
    180, 240, 300, 360, 420, 480, 540, 600,
    1_200, 1_800, 3_000, 6_000,
    12_000, 60_000, 600_000,
    6_000_000, 6_000_000_000,
    10**12, 10**18,  # extrem große Beispiele
]


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Zehnerpotenzen – Zahlennamen-Generator")
        self.geometry("860x780")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Header
        ctk.CTkLabel(
            self, text="Zahlennamen für Zehnerpotenzen",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            self,
            text="Generischer Konstrukteur nach dem System der langen Skala "
                 "(Chuquet/Conway-Wechsler) – beliebige Exponenten möglich.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        ).pack(pady=(0, 12))

        # Input
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=4)

        ctk.CTkLabel(input_frame, text="10 ^", font=ctk.CTkFont(size=20)).pack(
            side="left", padx=(0, 6)
        )
        self.entry = ctk.CTkEntry(
            input_frame, width=240, font=ctk.CTkFont(size=18),
            placeholder_text="z.B. 42  oder  1337133713371337",
        )
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", lambda _: self._on_lookup())
        ctk.CTkButton(
            input_frame, text="Nachschlagen", command=self._on_lookup,
            font=ctk.CTkFont(size=14), width=130,
        ).pack(side="left")

        # Result name
        self.result_name = ctk.CTkLabel(
            self, text="Million", font=ctk.CTkFont(size=30, weight="bold"),
            wraplength=820,
        )
        self.result_name.pack(pady=(18, 2))

        self.result_alias = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#7ab8ff",
        )
        self.result_alias.pack()

        # Construction breakdown
        self.breakdown = ctk.CTkTextbox(
            self, height=150, font=ctk.CTkFont(family="Courier", size=12),
            wrap="word", state="disabled",
        )
        self.breakdown.pack(padx=20, pady=(10, 6), fill="x")

        # Number preview
        ctk.CTkLabel(
            self, text="Zahlenvorschau:", font=ctk.CTkFont(size=12),
            text_color="gray", anchor="w",
        ).pack(padx=20, fill="x")
        self.result_number = ctk.CTkTextbox(
            self, height=55, font=ctk.CTkFont(family="Courier", size=12),
            wrap="char", state="disabled",
        )
        self.result_number.pack(padx=20, pady=(0, 8), fill="x")

        # Reference table
        ctk.CTkLabel(
            self, text="Referenz-Tabelle (generisch berechnet)",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(8, 4))

        table_frame = ctk.CTkScrollableFrame(self, height=200)
        table_frame.pack(padx=20, pady=(0, 14), fill="both", expand=True)

        header_font = ctk.CTkFont(size=12, weight="bold")
        ctk.CTkLabel(table_frame, text="Potenz", font=header_font, width=160, anchor="w").grid(
            row=0, column=0, padx=4, sticky="w"
        )
        ctk.CTkLabel(table_frame, text="Nullen", font=header_font, width=140, anchor="w").grid(
            row=0, column=1, padx=4, sticky="w"
        )
        ctk.CTkLabel(table_frame, text="Zahlenname", font=header_font, anchor="w").grid(
            row=0, column=2, padx=4, sticky="w"
        )
        row_font = ctk.CTkFont(size=12)
        for i, exp in enumerate(REFERENCE_EXPONENTS, start=1):
            try:
                name = power_to_name(exp)
            except Exception as e:
                name = f"<Fehler: {e}>"
            ctk.CTkLabel(
                table_frame, text=f"10^{exp:,}", font=row_font, anchor="w",
            ).grid(row=i, column=0, padx=4, sticky="w")
            ctk.CTkLabel(
                table_frame, text=f"{exp:,}", font=row_font, anchor="w",
            ).grid(row=i, column=1, padx=4, sticky="w")
            ctk.CTkLabel(
                table_frame, text=name, font=row_font, anchor="w", wraplength=460,
                justify="left",
            ).grid(row=i, column=2, padx=4, sticky="w")

        # Initial display
        self.entry.insert(0, "6")
        self._on_lookup()

    def _set_textbox(self, box: ctk.CTkTextbox, text: str) -> None:
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")

    def _on_lookup(self) -> None:
        raw = self.entry.get().strip().replace(".", "").replace(",", "").replace(" ", "")
        if not raw:
            return
        try:
            exponent = int(raw)
        except ValueError:
            self.result_name.configure(text="Ungültige Eingabe")
            self.result_alias.configure(text="")
            self._set_textbox(self.breakdown, "Bitte eine ganze Zahl ≥ 0 eingeben.")
            self._set_textbox(self.result_number, "")
            return

        if exponent < 0:
            self.result_name.configure(text="—")
            self.result_alias.configure(text="")
            self._set_textbox(self.breakdown, "Negativer Exponent nicht unterstützt.")
            self._set_textbox(self.result_number, "")
            return

        try:
            name = power_to_name(exponent)
            breakdown = explain_construction(exponent)
        except Exception as e:
            self.result_name.configure(text="<Fehler>")
            self._set_textbox(self.breakdown, f"Fehler: {e}")
            return

        self.result_name.configure(text=name)
        alias = SPECIAL_ALIASES.get(exponent, "")
        self.result_alias.configure(text=f"≈ {alias}" if alias else "")
        self._set_textbox(self.breakdown, breakdown)
        self._set_textbox(self.result_number, number_preview(exponent))


if __name__ == "__main__":
    App().mainloop()
