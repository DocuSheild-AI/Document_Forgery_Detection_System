from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os

def run_ela(image_path):
    try:
        # Open original image
        original = Image.open(image_path).convert('RGB')

        # Save compressed version
        temp_path = "temp_ela.jpg"
        original.save(temp_path, 'JPEG', quality=90)

        compressed = Image.open(temp_path)

        # Compute difference
        diff = ImageChops.difference(original, compressed)

        # Enhance differences
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])

        if max_diff == 0:
            max_diff = 1

        scale = 255.0 / max_diff

        diff = ImageEnhance.Brightness(diff).enhance(scale)

        # Convert to numpy for scoring
        diff_np = np.array(diff)

        # Calculate score
        score = float(np.mean(diff_np))

        # Decision logic
        if score > 20:
            result = "Possible Forgery"
        else:
            result = "No Forgery Detected"

        # Save ELA image
        ela_output_path = "uploads/ela_" + os.path.basename(image_path)
        diff.save(ela_output_path)

        return {
            "result": result,
            "score": round(score, 2),
            "ela_image": ela_output_path
        }

    except Exception as e:
        return {"error": str(e)}