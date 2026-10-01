
<script setup>
import { ref } from "vue";

const emit = defineEmits(["submit", "batal"]);

/* ============================================================
   Daftar opsi kategori & lokasi gudang
   (sesuaikan dengan seed_barang.json di backend)
   ============================================================ */
const opsiKategori = [
  "Rack & Enclosure",
  "Server Blade",
  "Prosesor",
  "Memori",
  "Penyimpanan",
  "Power Supply",
  "Jaringan",
  "Pendingin",
];

const opsiLokasi = [
  "DC-Rak A-01",
  "DC-Rak A-02",
  "DC-Rak B-01",
  "DC-Rak B-02",
  "DC-Rak C-01",
  "DC-Rak C-02",
  "DC-Rak C-03",
  "DC-Rak D-01",
  "DC-Rak D-02",
  "DC-Rak E-01",
  "DC-Rak E-02",
  "DC-Rak F-01",
];

/* ============================================================
   State lokal
   ============================================================ */
const nama = ref("");
const kategori = ref("");
const jumlahStok = ref(0);
const lokasiGudang = ref("");
const pesanValidasi = ref("");

/* ============================================================
   Handler submit
   ============================================================ */
function kirim() {
  pesanValidasi.value = "";

  if (!nama.value.trim()) {
    pesanValidasi.value = "Nama barang wajib diisi.";
    return;
  }
  if (!kategori.value) {
    pesanValidasi.value = "Kategori wajib dipilih.";
    return;
  }
  if (!lokasiGudang.value) {
    pesanValidasi.value = "Lokasi gudang wajib dipilih.";
    return;
  }
  if (jumlahStok.value < 0) {
    pesanValidasi.value = "Jumlah stok tidak boleh negatif.";
    return;
  }

  emit("submit", {
    nama: nama.value.trim(),
    kategori: kategori.value,
    jumlah_stok: Number(jumlahStok.value),
    lokasi_gudang: lokasiGudang.value,
  });

  /* Reset form */
  nama.value = "";
  kategori.value = "";
  jumlahStok.value = 0;
  lokasiGudang.value = "";
}
</script>

<template>
  <div class="form-card">
    <h2>Tambah Barang Baru</h2>

    <div class="form-grid">
      <!-- Nama: input teks bebas -->
      <input
        v-model="nama"
        type="text"
        placeholder="Nama barang (contoh: Kabel UTP Cat6)"
      />

      <!-- Kategori: dropdown -->
      <select v-model="kategori">
        <option value="" disabled>-- Pilih Kategori --</option>
        <option v-for="kat in opsiKategori" :key="kat" :value="kat">
          {{ kat }}
        </option>
      </select>

      <!-- Jumlah stok: input angka -->
      <input
        v-model.number="jumlahStok"
        type="number"
        placeholder="Jumlah stok"
        min="0"
      />

      <!-- Lokasi gudang: dropdown -->
      <select v-model="lokasiGudang">
        <option value="" disabled>-- Pilih Lokasi Gudang --</option>
        <option v-for="lok in opsiLokasi" :key="lok" :value="lok">
          {{ lok }}
        </option>
      </select>
    </div>

    <p
      v-if="pesanValidasi"
      class="status-msg error"
      style="padding: 0.5rem; margin-top: 0.5rem"
    >
      {{ pesanValidasi }}
    </p>

    <div class="form-actions">
      <button class="btn btn-outline" @click="emit('batal')">Batal</button>
      <button class="btn btn-primary" @click="kirim">Simpan</button>
    </div>
  </div>
</template>
