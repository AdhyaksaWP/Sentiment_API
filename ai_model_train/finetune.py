import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
dataset = pd.read_csv("./dataset/bpjs_review.csv")

# Pretrained model and tokenizer
pretrained = "mdhugol/indonesia-bert-sentiment-classification"
tokenizer = AutoTokenizer.from_pretrained(pretrained)
model = AutoModelForSequenceClassification.from_pretrained(pretrained, num_labels=3)

# Convert ratings to sentiment labels
def ratings_to_sentiments(row):
    if row > 3:
        return "positive"
    elif row == 3:
        return "neutral"
    else:
        return "negative"

def preprocess(df):
    df["Sentiment"] = df["Rating"].map(ratings_to_sentiments)
    return df

dataset = preprocess(dataset)

# Encode sentiment labels as integers
label_encoder = LabelEncoder()
label_map = {"positive": 0, "neutral": 1, "negative": 2}
dataset["Label"] = dataset["Sentiment"].map(label_map)

# Tokenize and split dataset
def tokenize(reviews, labels):
    x_train, x_test, y_train, y_test = train_test_split(
        reviews.tolist(),
        labels.tolist(),
        test_size=0.2,
        random_state=42
    )
    train_encodings = tokenizer(x_train, truncation=True, padding=True, max_length=128)
    val_encodings = tokenizer(x_test, truncation=True, padding=True, max_length=128)
    return train_encodings, val_encodings, y_train, y_test

train_encodings, val_encodings, y_train, y_test = tokenize(dataset["Review"], dataset["Label"])

# Create custom Dataset class
class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        return {
            key: torch.tensor(val[idx]) for key, val in self.encodings.items()
        } | {"labels": torch.tensor(self.labels[idx])}

    def __len__(self):
        return len(self.labels)

train_dataset = SentimentDataset(train_encodings, y_train)
val_dataset = SentimentDataset(val_encodings, y_test)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train and evaluate
trainer.train()
trainer.evaluate()

trainer.push_to_hub()
