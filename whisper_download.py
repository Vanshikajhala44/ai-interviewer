from huggingface_hub import snapshot_download

# Download whisper-small model
local_path = snapshot_download("openai/whisper-small")

print("Model downloaded to:", local_path)
