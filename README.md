"""# 🤖 RoBERTa Sentiment Analysis Dashboard

Aplikasi web berbasis Flask yang dirancang untuk menganalisis sentimen teks menggunakan model Deep Learning RoBERTa. Aplikasi ini mendukung analisis teks tunggal maupun pemrosesan massal (batch) melalui unggahan file CSV atau Excel.

---

## 🌟 Fitur Utama

- **Single Text Analysis**  
  Masukkan kalimat apa pun dan dapatkan hasil sentimen *(Positive, Neutral, Negative)* secara instan.

- **Batch File Processing**  
  Unggah file `.csv` atau `.xlsx` untuk menganalisis ribuan baris data sekaligus.

- **Data Visualization**  
  Ringkasan hasil analisis file ditampilkan dalam bentuk **Pie Chart interaktif** menggunakan Chart.js.

- **Confidence Score**  
  Menampilkan tingkat kepercayaan model terhadap prediksi yang diberikan.

- **Auto Column Detection**  
  Sistem secara otomatis mendeteksi kolom teks dalam file yang diunggah.

---

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python & Flask  
- **AI Model**: RoBERTa (via Hugging Face Transformers)  
- **Deep Learning Framework**: PyTorch  
- **Data Handling**: Pandas & Openpyxl  
- **Frontend**: Bootstrap 5, FontAwesome, & Chart.js  

---

## 📦 Kebutuhan Library (Prerequisites)

Pastikan kamu memiliki **Python 3.8+** terinstal.

Library utama yang dibutuhkan:

flask  
torch  
transformers  
pandas  
openpyxl  

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Persiapan Model

Pastikan kamu sudah memiliki file model RoBERTa di dalam folder `./models`.

Struktur folder:

project-root/  
├── models/  
│   ├── config.json  
│   ├── pytorch_model.bin  
│   └── tokenizer.json  
├── templates/  
│   └── index.html  
├── app.py  
└── model_handler.py  

---

### 2. Instalasi

pip install flask torch transformers pandas openpyxl

---

### 3. Menjalankan Server

python app.py

---

### 4. Akses Aplikasi

http://127.0.0.1:5000

---

## 📂 Struktur Folder

- **app.py**: Logika utama Flask dan pengaturan route.  
- **model_handler.py**: Kelas SentimentAnalyzer untuk preprocessing dan inference model AI.  
- **templates/**: Berisi file HTML (`index.html`) untuk tampilan web.  
- **models/**: Menyimpan file model transformer yang telah dilatih.  

---

## 📝 Catatan Penting

- Pastikan file CSV/Excel memiliki kolom seperti: text, komentar, atau content.  
- Jika tidak ada, sistem akan menggunakan kolom pertama secara otomatis.  
"""
