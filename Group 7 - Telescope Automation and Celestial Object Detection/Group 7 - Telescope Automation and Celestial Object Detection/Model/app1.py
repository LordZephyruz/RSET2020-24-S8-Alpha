from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u

# Function to fetch current longitude and latitude
def get_current_location():
    location = EarthLocation.of_site('greenwich')
    current_longitude = location.lon.to(u.deg).value
    current_latitude = location.lat.to(u.deg).value
    return current_longitude, current_latitude

# Function to fetch RA and Dec values for a celestial object
def get_ra_dec(celestial_object, current_longitude, current_latitude):
    obj_coord = SkyCoord.from_name(celestial_object)
    obj_ra = obj_coord.ra.to(u.deg).value
    obj_dec = obj_coord.dec.to(u.deg).value

    # Calculate offset
    offset_ra = obj_ra - current_longitude
    offset_dec = obj_dec - current_latitude

    return obj_ra, obj_dec, offset_ra, offset_dec

# Main function
def main():
    current_longitude, current_latitude = get_current_location()
    print(f"Current longitude: {current_longitude}, Current latitude: {current_latitude}")

    celestial_objects = ["bootes", "canis_major", "canis_minor", "cassiopeia", 
                         "cygnus", "gemini", "leo", "lyra", "moon", "orion", 
                         "pleiades", "sagittarius", "scorpius", "taurus", "ursa_major"]

    for celestial_object in celestial_objects:
        obj_ra, obj_dec, offset_ra, offset_dec = get_ra_dec(celestial_object, current_longitude, current_latitude)
        print(f"\nCelestial Object: {celestial_object}")
        print(f"RA: {obj_ra}, Dec: {obj_dec}")
        print(f"Offset RA: {offset_ra}, Offset Dec: {offset_dec}")

if __name__ == "__main__":
    main()