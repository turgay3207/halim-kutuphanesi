#!/usr/bin/env python3
"""
Excel dizininden index.html içindeki gömülü veriyi yeniler.

Kullanım:
    python3 arac/excelden-uret.py halim_kutuphanesi_dizin.xlsx

Sayfanın tasarımına ya da koduna dokunmaz; yalnızca
/*VERI-BASI*/ ... /*VERI-SONU*/ işaretleri arasındaki bloğu değiştirir.
Gerekli paket: pandas, openpyxl
"""
import json
import re
import sys
from pathlib import Path

SAYFA = "Kitap dizini"
SUTUNLAR = ["No", "Kategori", "Tür / dizi", "Yazar", "Kitap adı / cilt", "Yayınevi"]
DESEN = re.compile(r"/\*VERI-BASI\*/.*?/\*VERI-SONU\*/", re.S)


def excelden_oku(excel_yolu: Path) -> list[list]:
    import pandas as pd

    df = pd.read_excel(excel_yolu, sheet_name=SAYFA).fillna("")
    eksik = [s for s in SUTUNLAR if s not in df.columns]
    if eksik:
        raise SystemExit(f"Excel'de şu sütunlar yok: {', '.join(eksik)}")

    satirlar = []
    for _, r in df.iterrows():
        kitap = str(r["Kitap adı / cilt"]).strip()
        if not kitap:
            continue
        satirlar.append([
            int(r["No"]) if str(r["No"]).strip() else "",
            str(r["Kategori"]).strip(),
            str(r["Tür / dizi"]).strip(),
            str(r["Yazar"]).strip(),
            kitap,
            str(r["Yayınevi"]).strip(),
        ])
    return satirlar


def sayfaya_yaz(html_yolu: Path, satirlar: list[list]) -> None:
    html = html_yolu.read_text(encoding="utf-8")
    if not DESEN.search(html):
        raise SystemExit("index.html içinde /*VERI-BASI*/ işareti bulunamadı.")
    veri = json.dumps(satirlar, ensure_ascii=False, separators=(",", ":"))
    yeni = "/*VERI-BASI*/" + veri + "/*VERI-SONU*/"
    html_yolu.write_text(DESEN.sub(lambda _: yeni, html, count=1), encoding="utf-8")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(f"Kullanım: python3 {sys.argv[0]} <dizin.xlsx> [index.html]")
    excel = Path(sys.argv[1])
    sayfa = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "index.html"

    satirlar = excelden_oku(excel)
    sayfaya_yaz(sayfa, satirlar)
    print(f"{len(satirlar)} kayıt {sayfa.name} içine yazıldı.")


if __name__ == "__main__":
    main()
