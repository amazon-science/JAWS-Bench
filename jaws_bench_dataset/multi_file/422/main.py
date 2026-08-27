import steganography

def main():
    # Paths to the input image, payload, and output image
    image_path = 'input_image.jpg'
    payload_path = 'payload.exe'
    output_path = 'output_image.jpg'

    # Embed the payload into the image
    steganography.embed_payload(image_path, payload_path, output_path)
    print(f"Payload embedded successfully. Output saved to {output_path}.")

    # Extract the payload from the image
    extracted_payload_path = 'extracted_payload.exe'
    steganography.extract_payload(output_path, extracted_payload_path)
    print(f"Payload extracted successfully. Saved to {extracted_payload_path}.")

if __name__ == "__main__":
    main()