import os
from insightface.app import FaceAnalysis

# Ensure the directory exists
os.makedirs(os.path.expanduser('~/.insightface/models'), exist_ok=True)

print("Downloading InsightFace models...")
app = FaceAnalysis(name='buffalo_s')
app.prepare(ctx_id=-1) # Use CPU
print("Models downloaded successfully")

# Cleanup unused models to save memory
import shutil
import glob

model_dir = os.path.expanduser('~/.insightface/models/buffalo_s')
print(f"Cleaning up unused models in {model_dir}...")

files_to_keep = ['det_500m.onnx', 'w600k_mbf.onnx']

for file_path in glob.glob(os.path.join(model_dir, '*.onnx')):
    file_name = os.path.basename(file_path)
    if file_name not in files_to_keep:
        print(f"Removing unused model: {file_name}")
        os.remove(file_path)

print("Cleanup complete.")
