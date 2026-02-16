from huggingface_hub import HfApi, login
import os

# Authenticate with Hugging Face
login()

# Initialize API
api = HfApi()

# Repository details
repo_id = "bniladridas/conversational-ai-fine-tuned"
model_path = "./fine_tuned_model"

# Create new repository
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# Upload model
api.upload_folder(
    folder_path=model_path,
    repo_id=repo_id,
    repo_type="model",
    commit_message="Upload fine-tuned conversational AI model",
)

print(f"Model successfully uploaded to {repo_id}")
