import yaml
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Load configuration
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Ensure learning rate is a float
config["training"]["learning_rate"] = float(config["training"]["learning_rate"])

# Load dataset
dataset = load_dataset("daily_dialog", cache_dir="./data")

# Split dataset into train and eval
train_dataset = dataset["train"]
eval_dataset = dataset["validation"]

# Limit dataset size if specified
if "max_samples" in config["dataset"]:
    train_dataset = train_dataset.select(range(config["dataset"]["max_samples"]))
    eval_dataset = eval_dataset.select(range(config["dataset"]["max_samples"]))

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(config["model"]["name"])
model = AutoModelForCausalLM.from_pretrained(config["model"]["name"])

# Add padding token if not already present
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    model.resize_token_embeddings(len(tokenizer))


# Preprocess dataset
def preprocess_function(examples):
    # Ensure the input is a list of strings
    dialogs = [
        dialog if isinstance(dialog, str) else " ".join(dialog)
        for dialog in examples["dialog"]
    ]
    # Tokenize the dialogs
    tokenized = tokenizer(
        dialogs,
        truncation=True,
        padding="max_length",
        max_length=config["model"]["max_length"],
        return_tensors="pt",
    )
    # Convert tensors to lists
    return {
        "input_ids": tokenized["input_ids"].tolist(),
        "attention_mask": tokenized["attention_mask"].tolist(),
        "labels": tokenized["input_ids"].tolist(),
    }


# Tokenize datasets
train_tokenized = train_dataset.map(preprocess_function, batched=True)
eval_tokenized = eval_dataset.map(preprocess_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir=config["training"]["output_dir"],
    evaluation_strategy="epoch",
    learning_rate=config["training"]["learning_rate"],
    per_device_train_batch_size=config["training"]["per_device_train_batch_size"],
    per_device_eval_batch_size=config["training"]["per_device_eval_batch_size"],
    num_train_epochs=config["training"]["num_train_epochs"],
    weight_decay=config["training"]["weight_decay"],
    save_total_limit=config["training"]["save_total_limit"],
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
)

# Fine-tune model
trainer.train()

# Save fine-tuned model
trainer.save_model(config["training"]["output_dir"])
tokenizer.save_pretrained(config["training"]["output_dir"])
