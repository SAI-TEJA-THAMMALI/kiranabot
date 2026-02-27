from PIL import Image
import io

def preflight_check(image_bytes: bytes) -> dict:
    """
    Checks image quality before sending to Gemini API.
    Saves API calls on bad images.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size

        errors = []

        # Resolution check
        if width < 400 or height < 400:
            errors.append(
                f"Image too small ({width}x{height}). "
                f"Minimum 400x400 pixels required."
            )

        # File size check
        if len(image_bytes) < 5000:
            errors.append("Image file too small. May be corrupted.")

        if len(image_bytes) > 20 * 1024 * 1024:
            errors.append("Image too large. Maximum 20MB allowed.")

        # Format check
        if img.format not in ['JPEG', 'JPG', 'PNG', 'WEBP']:
            errors.append(
                f"Format {img.format} not supported. "
                f"Use JPEG or PNG."
            )

        # Aspect ratio check
        ratio = width / height
        if ratio < 0.3 or ratio > 4.0:
            errors.append(
                "Unusual image dimensions. "
                "Please photograph the invoice straight on."
            )

        if errors:
            return {
                "passed": False,
                "errors": errors,
                "message": errors[0],
                "width": width,
                "height": height
            }

        return {
            "passed": True,
            "errors": [],
            "message": "Image quality check passed",
            "width": width,
            "height": height,
            "format": img.format
        }

    except Exception as e:
        return {
            "passed": False,
            "errors": [str(e)],
            "message": "Could not read image file. Please try again."
        }
