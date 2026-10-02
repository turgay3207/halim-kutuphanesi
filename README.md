# Halim Kütüphanesi

1.052 ciltlik özel koleksiyonun aranabilir web dizini. Tek dosyalık, statik,
sunucu gerektirmez — GitHub Pages'te doğrudan çalışır.

İki tema arasında geçiş yapılabilir:

- **Orta Dünya** — Moria taşı, mithril ve yüzük ateşi. Koyu.
- **Hogwarts** — mum ışığında parşömen ve sepya mürekkep. Açık.

Seçim tarayıcıda hatırlanır.

## Dosyalar

```
index.html              sayfanın tamamı (stil + kod + veri)
arac/excelden-uret.py   Excel dizininden veriyi yeniler
README.md
```

## GitHub Pages'te yayına alma

1. Yeni bir depo aç (örn. `halim-kutuphanesi`) ve `index.html` dosyasını köke koy.

   ```bash
   git init
   git add index.html README.md arac/
   git commit -m "Halim Kütüphanesi"
   git branch -M main
   git remote add origin git@github.com:KULLANICI/halim-kutuphanesi.git
   git push -u origin main
   ```

2. Depoda **Settings → Pages** sayfasını aç.
3. *Source* için **Deploy from a branch**, *Branch* için `main` / `/ (root)` seç, kaydet.
4. Bir iki dakika sonra sayfa şurada olur:
   `https://KULLANICI.github.io/halim-kutuphanesi/`

Özel alan adı kullanacaksan Pages ayarlarındaki *Custom domain* alanına yaz;
depoya `CNAME` dosyası otomatik eklenir.

## Özellikler

| Ne | Nasıl |
| --- | --- |
| Arama | Kitap adı, yazar, yayınevi, kategori ve tür içinde birlikte arar. Türkçe duyarlı: `gazali` → *İmam Gazâlî*, `evliya celebi` → *Evliyâ Çelebi*. Birden çok kelime yazarsan hepsini birden arar. |
| Kategori süzgeci | Üstteki renkli şeritten ya da bir kartın kategori rozetine tıklayarak. |
| Yazar / yayınevi süzgeci | Denetim çubuğundaki açılır listelerden; her seçeneğin yanında kaç cilt olduğu yazar. |
| Sıralama | Kayıt sırası, kitap adı (A→Z / Z→A), yazar, kategori, önce eklenenler. |
| Kitap ekle | Sağ üstteki **Kitap ekle**. Kategori, yazar, yayınevi ve tür alanları mevcut değerlerden öneri verir. |
| Düzenle / sil | Kartın üzerine gelince beliren kalem ve çöp kutusu simgeleri. Silme sonrası **Geri al** çıkar. |
| Görünüm | Kart ızgarası ya da tek satırlık liste. |
| Dışa aktarma | Alt bilgideki **JSON indir** / **CSV indir**. CSV, Excel'de Türkçe karakterlerle doğru açılır. |
| İçe aktarma | **JSON yükle** — aynı kitap-yazar ikilisi zaten varsa atlanır. |
| Klavye | `/` arama alanına atlar, `Esc` aramayı veya pencereyi kapatır. |

## Eklediklerin nerede duruyor?

Eklediğin, sildiğin ve düzenlediğin kayıtlar **yalnızca o tarayıcıda**
(`localStorage`) saklanır. Sayfa statik olduğu için ziyaretçilerin yaptığı
değişiklikler birbirini etkilemez ve sunucuya gitmez.

Değişikliği kalıcı yapmak — yani siteyi açan herkesin görmesi için:

1. Alt bilgiden **JSON indir**.
2. İnen `halim-kutuphanesi.json` dosyasını kaynak olarak kullanıp aşağıdaki
   gibi `index.html` içine gömebilir ya da Excel'i güncelleyip yenileme
   aracını çalıştırabilirsin.
3. `index.html`'i depoya push et.

**Değişiklikleri geri al** düğmesi, o tarayıcıdaki tüm yerel değişiklikleri
siler ve dizini gömülü hâline döndürür.

## Veriyi Excel'den yenileme

Koleksiyona toplu ekleme yaptıysan Excel'i güncelle ve şunu çalıştır:

```bash
pip install pandas openpyxl
python3 arac/excelden-uret.py halim_kutuphanesi_dizin.xlsx
```

Araç yalnızca `index.html` içindeki `/*VERI-BASI*/ ... /*VERI-SONU*/`
işaretleri arasındaki veri bloğunu değiştirir; tasarıma ve koda dokunmaz.

Beklenen Excel yapısı — `Kitap dizini` sayfası, şu sütunlarla:

```
No | Kategori | Tür / dizi | Yazar | Kitap adı / cilt | Yayınevi
```

## Teknik notlar

- Bağımlılık yok. Tek dış kaynak Google Fonts (Cinzel + EB Garamond);
  yüklenemezse sistem serif yazı tipine düşer.
- Veri, dosya boyutu için dizi-of-dizi olarak gömülüdür; sütun sırası koddaki
  `SUTUNLAR` sabitinde tanımlıdır.
- Kategori renkleri ada göre karma (hash) ile üretilir, yani yeni bir kategori
  eklediğinde elle renk tanımlaman gerekmez.
- Kayıtlar 60'arlı yüklenir (`IntersectionObserver`); 1.000+ kartta sayfa
  takılmaz.
- Erişilebilirlik: klavyeyle tam gezinme, odak halkaları, `aria-live` sonuç
  sayacı, pencere içinde odak hapsi, `prefers-reduced-motion` desteği.
- Yazdırma stili var: süzgeçler gizlenir, kartlar sayfa arasında bölünmez.
