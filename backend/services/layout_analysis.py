import numpy as np

def run_layout_analysis(ocr_data):
    try:
        if not ocr_data or len(ocr_data) < 3:
            return {
                "layout_score": 0,
                "result": "Insufficient data",
                "suspicious": True
            }

        y_positions = []

        for item in ocr_data:
            bbox = item.get("bbox", None)

            if bbox:
                y_positions.append(bbox[0][1])

        if len(y_positions) < 3:
            return {
                "layout_score": 0,
                "result": "Insufficient layout data",
                "suspicious": True
            }

        y_positions = sorted(y_positions)
        spacings = np.diff(y_positions)

        if len(spacings) == 0:
            return {
                "layout_score": 0,
                "result": "No spacing data",
                "suspicious": True
            }

        # ✅ FIX: convert to float
        std_dev = float(np.std(spacings))

        if std_dev > 15:
            result = "Irregular Layout"
            suspicious = True
        else:
            result = "Consistent Layout"
            suspicious = False

        return {
            "layout_score": round(std_dev, 2),
            "result": result,
            "suspicious": suspicious
        }

    except Exception as e:
        return {"error": str(e)}