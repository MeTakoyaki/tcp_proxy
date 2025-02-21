# tcp_proxy

TCP Proxy ini adalah sebuah program Python yang berfungsi sebagai perantara antara klien dan server. Program ini dapat digunakan untuk menganalisis, memodifikasi, dan meneruskan lalu lintas jaringan TCP secara real-time.

## 🔧 Fitur Utama
- **Intercept Traffic**: Mampu menangkap dan mencetak data yang dikirim antara klien dan server.
- **Modifikasi Paket Data**: Memungkinkan pengguna untuk mengubah permintaan dan respons sebelum diteruskan.
- **Hex Dumping**: Menampilkan data dalam format heksadesimal untuk debugging.
- **Multi-threaded**: Menggunakan threading untuk menangani banyak koneksi secara simultan.
- **Customizable**: Dapat dimodifikasi untuk berbagai keperluan seperti filtering, logging, atau reverse engineering.

## 📌 Cara Penggunaan
### **1. Menjalankan Server Tujuan**
Jalankan server di port tertentu, misalnya menggunakan `nc`:
```sh
nc -lvp 9001
```
Atau gunakan server Python sederhana:
```python
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9001))
server.listen(5)
print("Server listening on port 9001...")
while True:
    client_socket, addr = server.accept()
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")
    client_socket.send(b"Hello from server!")
    client_socket.close()
```

### **2. Menjalankan Proxy**
Gunakan perintah berikut untuk menjalankan proxy:
```sh
python tcp-proxy.py 127.0.0.1 9000 127.0.0.1 9001 True
```
- `127.0.0.1 9000` → Proxy mendengarkan koneksi di sini.
- `127.0.0.1 9001` → Koneksi diteruskan ke server tujuan.
- `True` → Proxy menerima data dari server sebelum meneruskan ke klien.

### **3. Menjalankan Klien**
Gunakan `nc` untuk mengirim pesan melalui proxy:
```sh
nc 127.0.0.1 9000
```
Ketik pesan dan lihat bagaimana proxy menangani lalu lintas.

## ✅ Keunggulan
- **Mudah digunakan** dan tidak memerlukan dependensi tambahan.
- **Dapat dimodifikasi** sesuai kebutuhan debugging atau analisis jaringan.
- **Memungkinkan manipulasi lalu lintas TCP** secara real-time.
- **Multi-threaded**, dapat menangani banyak koneksi secara bersamaan.

## ❌ Kekurangan
- **Tidak mendukung protokol selain TCP** (misalnya UDP tidak bisa digunakan).
- **Tidak memiliki enkripsi** sehingga tidak cocok untuk lalu lintas sensitif tanpa modifikasi.
- **Tidak otomatis menangani reconnect** jika koneksi terputus.

## 🎯 Modifikasi yang Bisa Dilakukan
- **Filter atau blokir paket tertentu.**
- **Tambahkan logging untuk analisis jaringan.**
- **Gunakan sebagai proxy HTTP dengan parsing header yang lebih kompleks.**
- **Tambahkan fitur otomatisasi dalam memodifikasi request atau response.**

## 📜 Lisensi
Proyek ini bebas digunakan dan dimodifikasi sesuai kebutuhan.

---
Selamat mencoba! 🚀

