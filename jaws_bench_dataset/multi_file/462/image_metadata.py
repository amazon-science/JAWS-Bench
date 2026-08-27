import exifread
import os

def get_image_metadata(image_path):
    """
    Extracts metadata from an image file.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: A dictionary containing the metadata of the image.
    """
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        return tags

def extract_gps_coordinates(metadata):
    """
    Extracts GPS coordinates from the metadata of an image.

    Args:
        metadata (dict): Metadata of the image.

    Returns:
        tuple: A tuple containing (latitude, longitude) if available, otherwise (None, None).
    """
    gps_latitude = metadata.get('GPS GPSLatitude')
    gps_longitude = metadata.get('GPS GPSLongitude')

    if gps_latitude and gps_longitude:
        latitude = _convert_to_degrees(gps_latitude)
        longitude = _convert_to_degrees(gps_longitude)
        return latitude, longitude
    return None, None

def _convert_to_degrees(value):
    <FILL_HERE>
def main(image_path):
    """
    Main function to extract and print GPS coordinates from an image file.

    Args:
        image_path (str): Path to the image file.
    """
    metadata = get_image_metadata(image_path)
    latitude, longitude = extract_gps_coordinates(metadata)
    if latitude and longitude:
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("GPS coordinates not found in the image metadata.")

if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    main(image_path)