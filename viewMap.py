import folium
import address_ally
import io


def map(coordinates, zoom):

    interactive_map = folium.Map(
        location = coordinates,
        zoom_start=zoom,
        control_scale=True
    )

    # Speichern der Karte in einem BytesIO Objekt
    data = io.BytesIO()
    interactive_map.save(data, close_file=False)

    return data.getvalue().decode()

def map_with_marker(coordinates, zoom, marker_text):
    street = marker_text[0]
    number = marker_text[1]
    zipcode = marker_text[2]
    city = marker_text[3]
    interactive_map = folium.Map(
        location = coordinates,
        zoom_start=zoom,
        control_scale=True
    )

    # Erstellen eines Popups mit permanent sichtbarem Text
    popup = folium.Popup(f"{street} {number}, {zipcode} {city}", permanent=True)

    # Hinzufügen eines Markers mit dem Popup
    folium.Marker(
        location=coordinates,
        popup=popup
    ).add_to(interactive_map)

    # Speichern der Karte in einem BytesIO Objekt
    data = io.BytesIO()
    interactive_map.save(data, close_file=False)

    return data.getvalue().decode()

if __name__ == '__main__':
    origin_adress = 'Schopfheimer Str. 8 76227 Karlsruhe'
    origin_coord = address_ally.get_origin_coordinates(origin_adress)
    print(origin_coord)