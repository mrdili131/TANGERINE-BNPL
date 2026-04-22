import os
import uuid
import time
def upload():
    os.system(f"git init . && git add . && git commit -m autocommit-{uuid.uuid4()} && git branch -M main && git push origin main")

print("Super git uploaded 1.0\n")

print("Loading...")
time.sleep(3)
print("Uploading...\n")
upload()
time.sleep(2)

print('\n\nUploaded successfully!')