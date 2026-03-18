import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        # Menentukan lokasi folder model dan label kategori sentimen
        self.model_path = "agiagustiandavi/Fine_tuned_RoBERTa_base_for_Sentiment_Analysis_of_ChatGPT/models" 
        self.labels = {0: "Negative", 1: "Neutral", 2: "Positive"}

        # Memuat tokenizer (pemecah kata) dan model AI dari folder lokal
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        # Mengatur model ke mode evaluasi (bukan training)
        self.model.eval()

    def cleaning_text(self, text):
        # Menghapus link (URL) dan mention (@user) dari teks agar tidak mengganggu prediksi
        text = re.sub(r'http\S+', '', str(text))
        text = re.sub(r'@\w+', '', text)
        # Menghapus spasi berlebih dan merapikan teks
        clean = re.sub(r'\s+', ' ', text).strip()
        return clean

    def inference(self, cleaned_text):
        # Mengonversi teks menjadi format angka (tensor) yang dimengerti model
        inputs = self.tokenizer(
            cleaned_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=64
        )
        # Melakukan prediksi tanpa menghitung gradien (lebih cepat dan hemat memori)
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mengubah hasil mentah model (logits) menjadi nilai probabilitas (0-1)
        probs = F.softmax(outputs.logits, dim=1)
        # Mengambil indeks dengan probabilitas tertinggi
        idx = torch.argmax(probs, dim=1).item()
        return self.labels[idx], probs[0][idx].item()

    def analyze_text(self, text):
        # Alur lengkap: bersihkan teks -> lakukan prediksi -> kembalikan hasil rapi
        cleaned = self.cleaning_text(text)
        sentiment, confidence_score = self.inference(cleaned)
        return {
            "original_text": text,
            "sentiment": sentiment,
            "confidence": f"{confidence_score * 100:.2f}%"
        }

    def read_file(self, file_obj):
        # Membaca file berdasarkan formatnya (.csv atau .xlsx)
        if file_obj.filename.endswith('.csv'):
            df = pd.read_csv(file_obj)
        else:
            df = pd.read_excel(file_obj)
        
        # Mencoba mencari kolom mana yang berisi teks komentar secara otomatis
        potential_names = ['text', 'Text', 'TEXT', 'teks', 'Teks', 'content', 'komentar', 'comment']
        target_column = None

        for col in df.columns:
            if str(col).strip().lower() in [p.lower() for p in potential_names]:
                target_column = col
                break
        
        # Jika tidak ditemukan nama kolom yang cocok, gunakan kolom pertama
        if target_column is None:
            target_column = df.columns[0]
            
        return df, target_column

    def analyze_file(self, file_obj):
        # Membaca file dan menentukan kolom teksnya
        df, text_column = self.read_file(file_obj)
        
        sentiments = []
        confidences = []

        # Melakukan analisis satu per satu untuk setiap baris di kolom teks
        for text in df[text_column]:
            result = self.analyze_text(text)
            sentiments.append(result['sentiment'])
            confidences.append(result['confidence'])

        # Menambahkan kolom hasil analisis baru ke tabel asli
        df['Sentiment'] = sentiments
        df['Confidence'] = confidences
        return df
