# Document Manager

**Autor:** Lucciano Campassi (D4rkDr4g0n)
**Plataformas:** Arch Linux + Windows 11
**Propósito:** Procesamiento de documentos — PDF, metadatos, OCR, imágenes, conversión de formatos.

---

## Descripción general

Skill especializada en el manejo y transformación de documentos para informes técnicos, evidencia forense, documentación de pentesting y notas de estudio. Cubre herramientas CLI multiplataforma para manipulación de PDFs, extracción/edición de metadatos EXIF, OCR, procesamiento de imágenes y conversión entre formatos de documentos.

---

## Manipulación de PDF

### Merge / Unir PDFs

```bash
# pdftk — unir varios PDFs en uno
pdftk archivo1.pdf archivo2.pdf archivo3.pdf cat output combinado.pdf

# qpdf — alternativa moderna
qpdf --empty --pages archivo1.pdf archivo2.pdf -- combinado.pdf

# Ghostscript — útil cuando hay problemas de compatibilidad
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=combinado.pdf archivo1.pdf archivo2.pdf
```

### Split / Dividir PDF

```bash
# pdftk — extraer páginas específicas
pdftk documento.pdf cat 1-5 output primeras5.pdf
pdftk documento.pdf cat 7-end output desde_pag7.pdf

# qpdf — dividir rango de páginas
qpdf --pages documento.pdf 1-5 -- documento.pdf primeras5.pdf

# Separar cada página en un archivo individual
pdftk documento.pdf burst output pagina_%02d.pdf
```

### Extraer páginas

```bash
# pdftk — extraer páginas sueltas
pdftk documento.pdf cat 3 7 11 output paginas_seleccionadas.pdf

# qpdf
qpdf --pages documento.pdf 3,7,11 -- documento.pdf seleccion.pdf
```

### Compresión

```bash
# Ghostscript — compresión agresiva (screen quality)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=comprimido.pdf original.pdf

# Perfiles de compresión: /screen (mínima), /ebook (media), /printer (alta), /prepress (máxima)

# qpdf — linealización y optimización
qpdf --linearize --optimize-images entrada.pdf salida.pdf
```

### Metadata del PDF

```bash
# exiftool — ver metadatos
exiftool documento.pdf

# exiftool — editar título y autor
exiftool -Title="Nuevo Título" -Author="Lucciano Campassi" documento.pdf

# exiftool — eliminar metadatos
exiftool -all= documento.pdf
```

### PDF a texto

```bash
# pdftotext (poppler) — extraer texto plano
pdftotext documento.pdf salida.txt

# pdftotext — mantener layout
pdftotext -layout documento.pdf salida.txt

# pdftotext — rango de páginas
pdftotext -f 3 -l 10 documento.pdf paginas_3_10.txt
```

### PDF a imágenes

```bash
# pdftoppm (poppler) — cada página a PNG
pdftoppm -png documento.pdf pagina

# ImageMagick — PDF a imágenes (más lento pero más control)
convert -density 300 documento.pdf -quality 90 pagina.png

# pdfimages (poppler) — extraer imágenes incrustadas
pdfimages -all documento.pdf imagenes_extraidas
```

### Herramientas auxiliares

| Herramienta | Instalación Arch | Instalación Win | Uso principal |
|---|---|---|---|
| pdftk | `pdftk` (AUR) | `winget install pdftk` | Merge/split/estampado |
| qpdf | `qpdf` | `choco install qpdf` | Manipulación eficiente |
| poppler | `poppler` | `choco install poppler` | pdftotext, pdftoppm, pdfimages |
| ghostscript | `ghostscript` | `winget install ghostscript` | Compresión, conversión |

---

## EXIF y metadatos

### ExifTool — herramienta universal

```bash
# Ver todos los metadatos
exiftool imagen.jpg

# Ver solo EXIF
exiftool -EXIF:All imagen.jpg

# Ver GPS
exiftool -GPSPosition -GPSLatitude -GPSLongitude imagen.jpg

# Ver metadata de audio/video
exiftool audio.mp3
exiftool video.mp4
```

### Editar metadatos

```bash
# Modificar fecha de captura
exiftool -DateTimeOriginal="2024-01-15 14:30:00" imagen.jpg

# Agregar comentario
exiftool -Comment="Evidencia capturada durante reconocimiento" imagen.jpg

# Modificar autor y copyright
exiftool -Artist="D4rkDr4g0n" -Copyright="Lucciano Campassi 2024" imagen.jpg

# Editar GPS
exiftool -GPSLatitude="40.4168" -GPSLongitude="-3.7038" -GPSLatitudeRef=S -GPSLongitudeRef=W imagen.jpg
```

### Eliminar metadatos

```bash
# Eliminar TODOS los metadatos (EXIF, XMP, IPTC)
exiftool -all= imagen.jpg

# Eliminar solo EXIF (dejar XMP/IPTC)
exiftool -EXIF:All= imagen.jpg

# Eliminar solo GPS
exiftool -GPS:All= imagen.jpg

# Limpiar varios archivos a la vez (crea backups .bak)
exiftool -all= *.jpg *.png
```

### Bulk processing

```bash
# Procesar directorio completo recursivamente
exiftool -r -all= -overwrite_original ./fotos/

# Renombrar por fecha
exiftool '-FileName<${DateTimeOriginal}_${Filename}' -d "%Y%m%d_%H%M%S" *.jpg

# Exportar metadatos a CSV
exiftool -csv -r -DateTimeOriginal -Model -GPSPosition *.jpg > metadatos.csv

# Importar metadatos desde CSV
exiftool -csv=metadatos.csv *.jpg
```

### Forense de metadatos

```bash
# Ver historial de ediciones (Photoshop)
exiftool -History -DocumentHistory imagen.jpg

# Extraer todas las cadenas de texto de metadatos (útil para esteganografía)
exiftool -b -AllDates imagen.jpg | strings

# Diferencia entre metadatos originales y actuales
exiftool -a -u -G1 imagen.jpg | grep -E "Warning|Error|Unknown"

# Detectar manipulación de fecha
exiftool -validate imagen.jpg
```

### Instalación

```bash
# Arch Linux
sudo pacman -S perl-image-exiftool

# Windows
winget install exiftool
choco install exiftool
```

---

## OCR

### Tesseract — motor OCR

```bash
# OCR básico imagen -> texto
tesseract captura.png salida

# Especificar idioma
tesseract captura.png salida -l spa

# Múltiples idiomas
tesseract captura.png salida -l spa+eng

# Especificar PSM (Page Segmentation Mode)
tesseract captura.png salida -l spa --psm 6

# PSM comunes: 3 (automático), 4 (columna), 6 (bloque), 7 (línea), 11 (texto completo)
```

### Idiomas disponibles

```bash
# Listar idiomas instalados
tesseract --list-langs

# Instalar idiomas adicionales en Arch
sudo pacman -S tesseract-data-spa tesseract-data-eng tesseract-data-fra

# Instalar en Windows
winget install Tesseract-OCR --override "/AdditionalLanguages=spa+eng+fra"
```

### Formato de salida

```bash
# Texto plano (default)
tesseract captura.png salida

# PDF con capa de texto oculta (searchable PDF)
tesseract captura.png salida pdf

# TSV (con coordenadas)
tesseract captura.png salida tsv

# HOCR (con bounding boxes)
tesseract captura.png salida hocr

# ALTO XML
tesseract captura.png salida alto
```

### Preprocesamiento para mejorar OCR

```bash
# ImageMagick — umbralizar (binarizar)
convert captura.png -threshold 50% captura_procesada.png

# ImageMagick — aumentar contraste
convert captura.png -contrast-stretch 10% captura_procesada.png

# ImageMagick — redimensionar (300 DPI mínimo)
convert captura.png -resize 200% captura_procesada.png

# ImageMagick — eliminar ruido
convert captura.png -despeckle captura_procesada.png

# Pipeline completo
convert captura.png -colorspace Gray -resize 200% -threshold 50% -despeckle proc.png
tesseract proc.png salida -l spa
```

### OCR en PDFs

```bash
# PDF -> imágenes -> OCR -> PDF con texto
convert -density 300 documento.pdf -quality 100 pagina_%d.png
for f in pagina_*.png; do tesseract "$f" "${f%.png}" pdf; done
qpdf --empty --pages pagina_*.pdf -- documento_ocr.pdf

# OCRmyPDF — PDF a searchable PDF directamente
ocrmypdf --language spa entrada.pdf salida.pdf

# OCRmyPDF — forzar re-OCR
ocrmypdf --force-ocr --language spa entrada.pdf salida.pdf

# OCRmyPDF — mantener metadatos originales
ocrmypdf --preserve-metadata --language spa entrada.pdf salida.pdf
```

### Captura de pantalla con OCR

```bash
# Tomar captura con import (ImageMagick)
import captura.png
tesseract captura.png portapapeles -l spa | xclip -selection clipboard

# Captura con maim en Linux
maim -s captura.png && tesseract captura.png stdout -l spa | xclip -selection clipboard
```

### Instalación de herramientas OCR

```bash
# Arch Linux
sudo pacman -S tesseract tesseract-data-spa tesseract-data-eng
yay -S ocrmypdf

# Windows
winget install Tesseract-OCR
pip install ocrmypdf
```

---

## Procesamiento de imágenes

### ImageMagick — convert

```bash
# Redimensionar
convert entrada.png -resize 800x600 salida.png
convert entrada.png -resize 50% salida.png
convert entrada.png -resize 1920x1080^ -gravity center -extent 1920x1080 salida.png

# Cambiar formato
convert captura.bmp captura.png
convert imagen.heic imagen.jpg
convert documento.svg documento.pdf

# Calidad y compresión
convert entrada.jpg -quality 85 salida.jpg
convert entrada.png -compress jpeg -quality 90 salida.jpg

# Convertir a blanco y negro
convert entrada.png -colorspace Gray salida.png
convert entrada.png -threshold 50% salida.png
```

### ImageMagick — mogrify (bulk)

```bash
# Redimensionar todo un directorio
mogrify -resize 1920x1080 *.jpg

# Convertir formato en masa
mogrify -format png *.bmp

# Renombrar y redimensionar
mogrify -path ./salida -resize 800x600 -format jpg *.png
```

### ImageMagick — identify

```bash
# Información básica
identify imagen.png

# Información detallada
identify -verbose imagen.png

# Dimensiones de varias imágenes
identify -format "%f: %wx%h %dpi\n" *.jpg

# Listar todos los metadatos
identify -verbose imagen.png | grep -E "Resolution|Depth|Type|Channel"
```

### Anotaciones y marcas de agua

```bash
# Agregar texto (marca de agua)
convert entrada.png -pointsize 24 -fill "rgba(255,0,0,0.5)" \
        -annotate +30+30 "D4rkDr4g0n" salida.png

# Agregar texto alineado al centro
convert entrada.png -gravity center -pointsize 48 \
        -fill white -annotate 0 "CONFIDENCIAL" salida.png

# Superponer logo
convert entrada.png logo.png -gravity southeast -geometry +20+20 \
        -composite salida.png

# Borde y sombra
convert entrada.png -bordercolor black -border 2x2 \
        -bordercolor white -border 3x3 salida.png
```

### Screenshots

```bash
# import (ImageMagick) — captura completa
import -window root captura_pantalla.png

# import — captura de ventana (clic en la ventana)
import captura_ventana.png

# import — captura región (arrastrar selección)
import captura_region.png

# maim — captura rápida en Linux
maim ~/captura.png
maim -s ~/captura_region.png
maim -i $(xdotool getactivewindow) ~/captura_ventana.png

# flameshot — GUI con anotaciones (Linux)
flameshot gui
```

### Formatos comunes

| Formato | Uso | Ventaja | ImageMagick |
|---|---|---|---|
| PNG | Capturas, diagramas | Sin pérdida, transparencia | `convert x.png y.png` |
| JPEG | Fotos | Compresión pequeña | `convert x.jpg -quality 85 y.jpg` |
| HEIC | iOS moderno | Eficiente, Apple | `convert x.heic x.jpg` |
| WebP | Web | Moderno, Google | `convert x.png x.webp` |
| BMP | Raw | Sin compresión | `convert x.bmp x.png` |
| TIFF | Escaneo, OCR | Capas, RAW | `convert x.tiff x.png` |
| SVG | Vectorial | Escalable | `convert x.svg x.png` |

---

## Conversión de documentos

### Pandoc — convertidor universal

```bash
# Markdown -> PDF
pandoc informe.md -o informe.pdf

# Markdown -> DOCX
pandoc informe.md -o informe.docx

# Markdown -> HTML
pandoc informe.md -o informe.html

# Markdown -> EPUB
pandoc informe.md -o informe.epub
```

### Formatos de entrada/salida

```bash
# DOCX -> Markdown
pandoc documento.docx -o documento.md

# HTML -> Markdown
pandoc pagina.html -o documento.md

# EPUB -> Markdown
pandoc libro.epub -o libro.md

# Markdown -> PDF con template
pandoc informe.md -o informe.pdf --template=eisvogel --pdf-engine=xelatex

# Markdown -> PDF con lista de referencias
pandoc informe.md --bibliography=refs.bib --csl=ieee.csl -o informe.pdf
```

### Conversión con filtros

```bash
# Markdown con diagramas mermaid -> PDF
pandoc informe.md --filter pandoc-mermaid -o informe.pdf

# Markdown -> PDF con sintaxis highlight
pandoc informe.md --highlight-style=tango -o informe.pdf

# Extraer todas las imágenes de un DOCX
pandoc documento.docx -t plain --extract-media=./media -o texto.md
```

### Pipelines de conversión

```bash
# MD -> DOCX -> PDF (mejor output que MD->PDF directo)
pandoc informe.md -o informe.docx && pandoc informe.docx -o informe.pdf

# HTML -> MD -> TXT (extraer texto limpio)
pandoc pagina.html -o pagina.md && pandoc pagina.md -o pagina.txt

# Batch: convertir todos los MD de un directorio a DOCX
for f in *.md; do pandoc "$f" -o "${f%.md}.docx"; done

# Batch: DOCX a PDF con naming consistente
for f in *.docx; do pandoc "$f" -o "${f%.docx}.pdf"; done
```

### Tabla de formatos Pandoc

| Entrada | Salida | Comando ejemplo |
|---|---|---|
| Markdown | PDF | `pandoc doc.md -o doc.pdf` |
| Markdown | DOCX | `pandoc doc.md -o doc.docx` |
| Markdown | HTML | `pandoc doc.md -o doc.html` |
| Markdown | EPUB | `pandoc doc.md -o doc.epub` |
| Markdown | LaTeX | `pandoc doc.md -o doc.tex` |
| DOCX | Markdown | `pandoc doc.docx -o doc.md` |
| HTML | Markdown | `pandoc doc.html -o doc.md` |
| EPUB | Markdown | `pandoc doc.epub -o doc.md` |
| LaTeX | PDF | `pandoc doc.tex -o doc.pdf` |
| Markdown | PDF (con xelatex) | `pandoc doc.md --pdf-engine=xelatex -o doc.pdf` |

---

## Herramientas por plataforma

### Linux (Arch Linux — pacman/AUR)

| Herramienta | Paquete | Propósito |
|---|---|---|
| exiftool | `perl-image-exiftool` | Metadatos universales |
| tesseract | `tesseract` | OCR |
| tesseract-lang | `tesseract-data-spa` | Idiomas OCR |
| ocrmypdf | `ocrmypdf` (AUR) | PDF a searchable PDF |
| imagemagick | `imagemagick` | Procesamiento de imágenes |
| poppler | `poppler` | pdftotext, pdftoppm, pdfimages |
| qpdf | `qpdf` | Manipulación PDF |
| ghostscript | `ghostscript` | Compresión PDF |
| pdftk | `pdftk` (AUR) | Merge/split PDF |
| pandoc | `pandoc` | Conversión de documentos |
| pandoc-* | `pandoc-*` (AUR) | Filtros pandoc adicionales |
| maim | `maim` | Capturas de pantalla |
| flameshot | `flameshot` | Capturas con GUI |
| xclip | `xclip` | Portapapeles CLI |

### Windows (winget / chocolatey)

| Herramienta | winget | chocolatey | Propósito |
|---|---|---|---|
| exiftool | `exiftool` | `exiftool` | Metadatos |
| Tesseract | `Tesseract-OCR` | `tesseract` | OCR |
| ImageMagick | `ImageMagick` | `imagemagick` | Imágenes |
| ghostscript | `ghostscript` | `ghostscript` | PDF |
| pandoc | `pandoc` | `pandoc` | Conversión |
| qpdf | — | `qpdf` | PDF |
| poppler | — | `poppler` | PDF utils |

### Instalación rápida Arch

```bash
sudo pacman -S perl-image-exiftool tesseract tesseract-data-spa \
  tesseract-data-eng imagemagick poppler qpdf ghostscript pandoc maim xclip
yay -S pdftk ocrmypdf
```

### Instalación rápida Windows

```powershell
winget install exiftool Tesseract-OCR ImageMagick ghostscript pandoc
choco install qpdf poppler
pip install ocrmypdf
```

---

## Flujos de trabajo comunes

### Evidencia para informe de pentesting

```bash
# 1. Capturar pantalla
maim -s evidencia.png

# 2. Redimensionar y anotar
convert evidencia.png -resize 1200x -pointsize 20 \
  -fill red -annotate +10+10 "Vulnerabilidad X" evidencia_anotada.png

# 3. Sanitizar metadatos
exiftool -all= evidencia_anotada.png

# 4. Insertar en informe Markdown
echo "![Evidencia](./evidencia_anotada.png)" >> informe.md

# 5. Generar PDF con lista de evidencias
pandoc informe.md -o informe.pdf --pdf-engine=xelatex
```

### Pipeline OCR completo

```bash
# Escaneo -> texto -> informe
convert -density 300 escaneo.pdf -colorspace Gray -threshold 50% proc.png
tesseract proc.png stdout -l spa > texto_extraido.txt
pandoc texto_extraido.txt -o informe_ocr.pdf
```

### Batch de limpieza de metadatos

```bash
# Limpiar metadatos de todas las imágenes en un proyecto
exiftool -r -all= -overwrite_original ./evidencias/
# Verificar que quedaron limpios
exiftool -r -T -DateTimeOriginal ./evidencias/ 2>&1 | grep -v "unknown"
```
