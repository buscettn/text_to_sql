import json
import argparse
import os
import torch
from gliner import GLiNER
from gliner.training import Trainer, TrainingArguments
from gliner.data_processing.collator import SpanDataCollator

def main():
    parser = argparse.ArgumentParser(description="Fine-tune GLiNER model for bank entity recognition.")
    parser.add_argument("--test", action="store_true", help="Run in test mode (small data, 1 epoch).")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=10, help="Training batch size.")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate.")
    args = parser.parse_args()

    # Paths
    dataset_path = "data/semantic_input/entities/train/dataset.json"
    model_output_dir = "data/gliner/models/gliner_mfi_finetuned"
    base_model = "urchade/gliner_multi-v2.1"

    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}. Run generate_train_data.py first.")
        return

    # Load dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if args.test:
        print("Running in TEST mode...")
        data = data[:200]
        args.epochs = 1
        args.batch_size = 2
    
    # Randomly shuffle data before splitting
    import random
    random.shuffle(data)

    # Split data (90/10 split)
    split_idx = int(len(data) * 0.9)
    if split_idx == 0 and len(data) > 0:
        split_idx = 1
    
    train_data = data[:split_idx]
    eval_data = data[split_idx:]

    print(f"Total samples: {len(data)}")
    print(f"Train samples: {len(train_data)}")
    print(f"Eval samples: {len(eval_data)}")

    # Load model
    print(f"Loading base model: {base_model}")
    model = GLiNER.from_pretrained(base_model)

    # Training arguments
    # Note: TrainingArguments might have different fields depending on the gliner version
    training_args = TrainingArguments(
        output_dir=model_output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        save_steps=1000,
        save_total_limit=2,
        logging_steps=10,
        eval_steps=100,
        eval_strategy="steps" if not args.test else "no",
        learning_rate=args.lr,
        max_grad_norm=1.0,
        weight_decay=0.01,
        warmup_ratio=0.1,
    )

    # Initialize Data Collator
    data_collator = SpanDataCollator(model.config, data_processor=model.data_processor, prepare_labels=True)

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=eval_data if eval_data else None,
        data_collator=data_collator,
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving model to {model_output_dir}")
    model.save_pretrained(model_output_dir)
    print("Training completed successfully!")

if __name__ == "__main__":
    main()
