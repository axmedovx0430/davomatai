import os
from insightface.app import FaceAnalysis

# Ensure the directory exists
os.makedirs(os.path.expanduser('~/.insightface/models'), exist_ok=True)

print("Downloading InsightFace models...")
app = FaceAnalysis(name='buffalo_s')
app.prepare(ctx_id=-1) # Use CPU
print("Models downloaded successfully")
