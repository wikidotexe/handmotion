# Hand & Face Tracker Camera 🎥🖐️

Proyek ini adalah aplikasi kamera berbasis Python yang menggunakan **MediaPipe** dan **OpenCV** untuk:

- Mendeteksi tangan dan wajah secara real-time.
- Mengganti filter kamera hanya dengan gestur tangan terbuka.
- Melakukan zoom in/out menggunakan jarak antara ibu jari dan telunjuk.
- Melacak wajah dengan kotak deteksi otomatis.
- Menampilkan log eksekusi langsung di terminal.

## ✨ Fitur

✅ Deteksi tangan (Hand Landmarks)
✅ Deteksi wajah (Face Detection)
✅ Ganti filter kamera (Hand Open Gesture)
✅ Zoom in/out (Gesture Pinch)
✅ Kotak deteksi wajah (Face Bounding Box)
✅ Log aktivitas realtime di terminal

## 🖥️ Dependencies

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

## 📦 Installasi

1. **Clone repository**

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

2. **Buat virtual environment (opsional tapi direkomendasikan)**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Buat file `requirements.txt` seperti ini:

```
opencv-python
mediapipe
numpy
```

## 🚀 Cara Menjalankan

1. Jalankan file Python:

```bash
python handmotion.py
```

2. Aplikasi akan membuka kamera secara otomatis.
   Berikut gesture yang bisa digunakan:

| Gesture                            | Fungsi              |
| ---------------------------------- | ------------------- |
| Tangan terbuka (open palm)         | Ganti filter kamera |
| Tangan mengepal (closed fist)      | Tidak ganti filter  |
| Jarak ibu jari & telunjuk > 150 px | Zoom in             |
| Jarak ibu jari & telunjuk < 50 px  | Zoom out            |

3. Tekan `q` di keyboard untuk keluar dari aplikasi.

## 📍 Catatan

- Aplikasi menggunakan **kamera default (0)**. Jika punya multiple webcam, bisa ubah index di:

```python
cap = cv2.VideoCapture(0)
```

→ Misal, ganti `0` menjadi `1` untuk webcam eksternal.

- Zoom maksimal: **2.0x**
- Zoom minimal: **1.0x**

## 🙌 Kontributor

Dwiki Arlian Maulana
🤝 Pull request & saran fitur sangat diterima!
