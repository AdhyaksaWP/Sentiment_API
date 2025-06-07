# 📘 Sentiment\_API

**Final Project for Cloud Computing Class**

This project provides a sentiment analysis API built using Django and Hugging Face Transformers. 
---

## 🛠️ Requirements

* Python 3.10
* Docker
* Internet connection (for initial model and dependency downloads)

---

## 🖊️ Training

To train the model yourself:

1. Install the required dependencies:

   ```bash
   cd ai_model_train
   pip install -r training_requirements.txt
   ```

2. The dataset was collected manually from BPJS Yogyakarta Google Maps reviews using:

   ```bash
   python dataset_scraping.py
   ```

3. Fine-tuning was performed using `finetune.py`. The resulting model was then pushed to Hugging Face at:
   [`LxngT/indonesian-sentiment-model`](https://huggingface.co/LxngT/indonesian-sentiment-model)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AdhyaksaWP/Sentiment_API.git
cd Sentiment_API
```

### 2. Download the Hugging Face Model

```bash
python download_model.py
```

> This script downloads the `bert-base-indonesian-1.5G-sentiment-analysis-smsa` model into the `./model` directory.

### 3. Download PyTorch Wheel for Linux (Optional for Docker Build)

```bash
pip download torch==2.6.0 --platform manylinux2014_x86_64 --python-version 310 --only-binary=:all: --no-deps
```

> Downloads the appropriate PyTorch wheel for Python 3.10 and Linux, required when installing dependencies inside Docker.

### 4. Build the Docker Image

```bash
docker build -t sentiment-app .
```

> Builds the Docker image using the provided Dockerfile.

### 5. Run the Docker Container

```bash
docker run -p 8000:8000 sentiment-app
```

> Starts the Docker container and maps port 8000 inside the container to port 8000 on your host machine.

---

## 📡 API Usage

### Endpoint

`POST /api/sentiment/analyze/`

### Request Format

* **Content-Type:** `application/json`
* **Body Example:**

```json
{
  "message": "Pelayanan OpenIMIS kurang dapat diandalkan"
}
```

### Response Example

```json
{
  "original_text": "Pelayanan OpenIMIS kurang dapat diandalkan",
  "clean_text": "Pelayanan OpenIMIS kurang diandalkan",
  "sentiment": "Negative"
}
```

> This endpoint processes the input text and returns a cleaned version along with the predicted sentiment: `Positive`, `Neutral`, or `Negative`.

---

## 🧪 Testing the API

You can test the API using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/sentiment/analyze/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Pelayanan OpenIMIS kurang dapat diandalkan"}'
```

---

## 🗂️ Project Structure

```
Sentiment_API/
├── sentiment/                  # Django app (views, URLs, etc.)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── sentiment_project/          # Django project settings
│   ├── model/                  # Directory containing the Hugging Face model
│   │   └── ...                 # Model files
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── download_model.py           # Script to fetch model from Hugging Face
├── manage.py                   # Django management script
├── requirements.txt            # API dependency list
├── Dockerfile                  # Docker build instructions
└── README.md                   # Project documentation
```

---

## ⚙️ Additional Notes

* **Model Loading:** The model is loaded locally from the `./model` directory to avoid downloading at runtime, which is ideal for Dockerized environments.
* **PyTorch Wheel:** Ensure the PyTorch wheel matches your Python version and target platform (e.g., Python 3.10, manylinux2014).
* **Docker Considerations:** The Dockerfile installs Python dependencies and includes the model and wheel files for an efficient, offline-capable deployment.
