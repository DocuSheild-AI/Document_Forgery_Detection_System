import cv2
import numpy as np
from sklearn.cluster import DBSCAN

def run_copy_move(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Image not loaded"}

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create(nfeatures=1500)
        keypoints, descriptors = orb.detectAndCompute(gray, None)

        if descriptors is None or len(keypoints) < 10:
            return {"result": "No features detected", "clusters": 0}

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors, descriptors)

        matches = sorted(matches, key=lambda x: x.distance)

        filtered_matches = []
        for m in matches:
            if m.queryIdx != m.trainIdx:
                filtered_matches.append(m)

        good_matches = filtered_matches[:200]

        points = []
        for m in good_matches:
            pt = keypoints[m.queryIdx].pt
            points.append(pt)

        if len(points) < 10:
            return {"result": "No suspicious regions", "clusters": 0}

        points = np.array(points)

        clustering = DBSCAN(eps=30, min_samples=5).fit(points)
        labels = clustering.labels_

        unique_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        # ✅ FIX: convert to int
        unique_clusters = int(unique_clusters)

        if unique_clusters > 5:
            result = "Forgery Detected"
        else:
            result = "No Forgery Detected"

        return {
            "result": result,
            "clusters": unique_clusters
        }

    except Exception as e:
        return {"error": str(e)}