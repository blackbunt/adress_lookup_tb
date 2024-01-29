import viewMap
import address_ally
import tempfile
#import weasyprint
import os

def print_pdf(file_path):
    os.startfile(file_path, "print")


if __name__ == '__main__':
    origin_adress = 'Schopfheimer Str. 8 76227 Karlsruhe'
    origin_coord = address_ally.get_origin_coordinates(origin_adress)[0]
    print(origin_coord)
    map_html = viewMap.map(origin_coord, 15)

    # Erstellen einer temporären HTML-Datei
    temp_html = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.html')
    temp_html.write(map_html)
    temp_html.close()
    print(temp_html.name)
    # Erstellen einer temporären PDF-Datei
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_pdf.close()

    # Konvertieren von HTML in PDF
    #weasyprint.HTML(filename=temp_html.name).write_pdf(temp_pdf.name)

    # Drucken der PDF-Datei
    #print_pdf(temp_pdf.name)

    # Optional: Löschen der temporären Dateien
    #os.remove(temp_html.name)
    #os.remove(temp_pdf.name)