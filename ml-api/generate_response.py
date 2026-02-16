import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    parser = argparse.ArgumentParser(
        description="Generate a response using the Conversational AI Fine-Tuned Model"
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input text for the model"
    )
    args = parser.parse_args()

    # Load the model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        "bniladridas/conversational-ai-fine-tuned"
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "bniladridas/conversational-ai-fine-tuned"
    )

    # Tokenize input
    inputs = tokenizer(args.input, return_tensors="pt")

    # Generate response
    outputs = model.generate(**inputs)

    # Decode and print the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(response)


if __name__ == "__main__":
    main()
