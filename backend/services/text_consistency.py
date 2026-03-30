from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def run_text_consistency(full_text):
    try:
        if not full_text or len(full_text.strip()) < 10:
            return {
                "consistency_score": 0,
                "result": "Low consistency",
                "suspicious": True
            }

        # Split into sentences (simple split)
        sentences = full_text.split(" ")

        # Remove very small tokens
        sentences = [s for s in sentences if len(s) > 2]

        if len(sentences) < 2:
            return {
                "consistency_score": 0,
                "result": "Insufficient text",
                "suspicious": True
            }

        # Encode sentences
        embeddings = model.encode(sentences, convert_to_tensor=True)

        # Compute similarity between consecutive parts
        similarities = []

        for i in range(len(embeddings) - 1):
            sim = util.cos_sim(embeddings[i], embeddings[i + 1]).item()
            similarities.append(sim)

        avg_similarity = sum(similarities) / len(similarities)

        # Decision logic
        if avg_similarity < 0.3:
            result = "Low consistency"
            suspicious = True
        else:
            result = "High consistency"
            suspicious = False

        return {
            "consistency_score": round(avg_similarity, 2),
            "result": result,
            "suspicious": suspicious
        }

    except Exception as e:
        return {"error": str(e)}