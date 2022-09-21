# sihalal-crawler

Script untuk menjelajah dan menarik data produsen/produk halal yang terdaftar di http://info.halal.go.id/cari/ secara otomatis berbasis python (selenium & beautifulsoup)

Langkah-langkah:
1. Install package yang dibutuhkan dalam requirements.txt (pip install -r requirements.txt)
2. Pastikan untuk menggunakan chromedriver dengan versi yang sama dengan browser Chrome yang dipakai (chromedriver bisa diunduh di sini: https://chromedriver.chromium.org/downloads)
3. Jalankan dengan menggunakan command pyhton main.py --jenis <Pilihan jenis produk pada web Sihalal> --bisnis <Pencarian berdasarkan nama pelaku usaha pada web Sihalal> --provinsi <Pilihan provinsi pada web Sihalal> --produk <Pencarian berdasarkan nama produk pada web Sihalal>