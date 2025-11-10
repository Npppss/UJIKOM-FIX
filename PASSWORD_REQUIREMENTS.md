# 🔐 PASSWORD REQUIREMENTS

## Kriteria Password yang Valid

Password harus memenuhi **SEMUA** kriteria berikut:

1. ✅ **Minimal 8 karakter**
2. ✅ **Huruf kecil** (a-z) - minimal 1 karakter
3. ✅ **Huruf besar** (A-Z) - minimal 1 karakter
4. ✅ **Angka** (0-9) - minimal 1 karakter
5. ✅ **Karakter spesial** - minimal 1 karakter dari: `@$!%*?&#`

## Contoh Password Valid

✅ **Valid:**
- `Password123#`
- `MyPass123!`
- `Test123@`
- `Admin123$`

❌ **Tidak Valid:**
- `password123#` (tidak ada huruf besar)
- `PASSWORD123#` (tidak ada huruf kecil)
- `Password#` (tidak ada angka)
- `Password123` (tidak ada karakter spesial)
- `Pass1#` (kurang dari 8 karakter)

## Validasi

- **Frontend**: Validasi real-time saat mengetik
- **Backend**: Validasi saat submit form
- **Kedua validasi harus sinkron**

## Error Messages

Jika password tidak valid, akan muncul error:
- "Password minimal 8 karakter dan harus mengandung angka, huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)"

---

**Pastikan password memenuhi semua kriteria sebelum submit!**

