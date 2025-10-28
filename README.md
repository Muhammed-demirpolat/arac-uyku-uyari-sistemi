# arac-uyku-uyari-sistemi

# 🚗 Göz Takipli Uykuya Kalma Uyarı Sistemi

Bu proje, araç sürücülerinin yorgunluk veya uyku durumunu tespit etmek için **yapay zekâ tabanlı yüz ve göz takibi** kullanır.  
Kamera üzerinden gözlerin açık/kapalı durumunu analiz eder ve sürücü uzun süre gözlerini kapatırsa **ekranda uyarı** verir ve **sesli alarm çalar** 🔊

---

## 🧩 Özellikler
- Gerçek zamanlı yüz ve göz tespiti (MediaPipe FaceMesh ile)
- Göz açıklık oranı (EAR) ile yorgunluk tespiti
- Uzun süre göz kapalıysa:
  - Ekranda `"UYKUYA KALDIN!"` uyarısı
  - Sesli alarm (winsound)
- Yanlış pozitifleri azaltmak için esnek parametre ayarları

---


 


---

## ⚙️ Kurulum

### 1️⃣ Gerekli Kütüphaneler
```bash
pip install opencv-python mediapipe
3.10.x sürümleri de çalışır 
