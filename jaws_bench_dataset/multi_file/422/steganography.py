import os
from PIL import Image

def embed_payload(image_path, payload_path, output_path):
    # Open the image file
        # Convert the image to RGB mode
        # Get the pixel data
        # Flatten the pixel data
    # Read the payload file
    # Ensure the payload fits into the image
    # Embed the payload into the image
            # Embed one byte of the payload into the pixel
            # No more payload to embed, keep the original pixel value
    # Reshape the embedded data back into pixel format
    # Save the output image
    <FILL_HERE>
def extract_payload(image_path, output_path):
    """
    Extracts the embedded payload from a JPG image.

    :param image_path: Path to the input image file with embedded payload.
    :param output_path: Path to save the extracted payload.
    """
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to RGB mode
        img = img.convert('RGB')
        # Get the pixel data
        pixels = list(img.getdata())
        # Flatten the pixel data
        flat_pixels = [pixel for sublist in pixels for pixel in sublist]

    # Extract the payload from the image
    payload_data = bytearray()
    for pixel in flat_pixels:
        # Extract one byte of the payload from the pixel
        payload_byte = pixel & 0x03
        payload_data.append(payload_byte)

    # Write the extracted payload to a file
    with open(output_path, 'wb') as payload_file:
        payload_file.write(payload_data)