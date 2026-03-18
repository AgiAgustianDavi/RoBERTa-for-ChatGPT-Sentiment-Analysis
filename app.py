from flask import Flask, render_template, request, flash, send_file
from model_handler import SentimentAnalyzer
import pandas as pd
import os

class FlaskApp:
    def __init__(self):
        # Inisialisasi aplikasi Flask dan kunci rahasia untuk sesi/flash message
        self.app = Flask(__name__)
        self.app.secret_key = '*'
        # Memuat model analisis sentimen
        self.analyzer = SentimentAnalyzer()
        self._register_routes()

    def _register_routes(self):
        # Mendaftarkan rute URL: halaman utama dan rute untuk proses prediksi
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/predict', 'predict', self.predict, methods=['POST'])

    def validate_input(self, req):
        # Mengambil input dari form, baik berupa file maupun teks
        file = req.files.get('file')
        text = req.form.get('input_text')

        # Cek jika ada file yang diunggah dan formatnya sesuai
        if file and file.filename != '':
            if file.filename.endswith(('.csv', '.xlsx')):
                return 'file', file
            return 'invalid_extension', None
        
        # Cek jika ada input teks manual
        if text and text.strip():
            return 'text', text

        # Jika tidak ada input sama sekali
        return None, None

    def index(self):
        # Menampilkan halaman utama aplikasi
        return render_template('index.html')

    def predict(self):
        # Validasi jenis input yang dikirim pengguna
        input_type, data = self.validate_input(request)

        # Jika input berupa teks tunggal
        if input_type == 'text':
            result = self.analyzer.analyze_text(data)
            return render_template('index.html', result=result, mode='text')

        # Jika input berupa file (batch processing)
        elif input_type == 'file':
            try:
                # Proses file dan simpan hasilnya ke CSV
                result_df = self.analyzer.analyze_file(data)
                result_df.to_csv('sentiment_result.csv', index=False)

                # Menghitung statistik jumlah sentimen untuk grafik (chart)
                stats = result_df['Sentiment'].value_counts().to_dict()
                chart_data = [
                    stats.get('Negative', 0), 
                    stats.get('Neutral', 0), 
                    stats.get('Positive', 0)
                ]
                
                # Mengirimkan hasil 10 baris pertama dan data grafik ke template
                return render_template(
                    'index.html', 
                    file_results=result_df.head(10).to_dict(orient='records'),
                    chart_data=chart_data, 
                    mode='file'
                )
            except Exception as e:
                # Menangani error jika proses file gagal
                flash(f"Error memproses file: {str(e)}", "danger")
                return render_template('index.html', mode='file')

        # Pesan peringatan jika ekstensi file salah
        elif input_type == 'invalid_extension':
            flash("Format file harus .csv atau .xlsx", "warning")
            return render_template('index.html', mode='file')

        # Pesan peringatan jika tombol ditekan tanpa input apa pun
        else:
            flash("Harap masukkan teks atau unggah file terlebih dahulu", "warning")
            return render_template('index.html')

if __name__ == '__main__':
    # Menjalankan server Flask dalam mode debug
    web = FlaskApp()
    web.app.run(debug=True)