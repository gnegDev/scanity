import pydicom
import numpy as np
from PIL import Image
from io import BytesIO

def dcm_to_png(dicom_data_bytes):
    """
    Converts DICOM image data (bytes) to PNG image data (bytes).

    Args:
        dicom_data_bytes (bytes): The raw bytes of a DICOM file.

    Returns:
        bytes: The raw bytes of the converted PNG image, or None if conversion fails.
    """
    try:
        # Read DICOM data from bytes
        ds = pydicom.dcmread(BytesIO(dicom_data_bytes))

        # Extract pixel data
        pixel_array = ds.pixel_array

        # Handle photometric interpretation (e.g., MONOCHROME1) and scaling
        if 'PhotometricInterpretation' in ds and ds.PhotometricInterpretation == "MONOCHROME1":
            pixel_array = np.amax(pixel_array) - pixel_array

        # Normalize and convert to 8-bit for display
        if pixel_array.dtype != np.uint8:
            pixel_array = pixel_array - np.min(pixel_array)
            if np.max(pixel_array) > 0:
                pixel_array = pixel_array / np.max(pixel_array) * 255
            pixel_array = pixel_array.astype(np.uint8)

        # Create a Pillow Image object
        img = Image.fromarray(pixel_array)

        # Save the image as PNG to a BytesIO object
        png_output = BytesIO()
        img.save(png_output, format="PNG")
        png_bytes = png_output.getvalue()

        return png_bytes

    except Exception as e:
        print(f"Error converting DICOM to PNG: {e}")
        return None

def jpg_to_png(jpg_bytes):
    """
    Converts JPG image bytes to PNG image bytes.

    Args:
        jpg_bytes (bytes): The byte data of the JPG image.

    Returns:
        bytes: The byte data of the converted PNG image.
    """
    # Open the JPG image from bytes
    jpg_stream = BytesIO(jpg_bytes)
    img = Image.open(jpg_stream)

    # Save the image as PNG to a new BytesIO object
    png_stream = BytesIO()
    img.save(png_stream, format="PNG")

    # Get the PNG bytes
    png_bytes = png_stream.getvalue()
    return png_bytes