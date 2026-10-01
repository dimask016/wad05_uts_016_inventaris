<script setup>
import { ref } from "vue";

const emit = defineEmits(["submit", "batal"]);

/* State lokal — spec 3.1: "Form tambah data baru memakai state lokal (ref)" */
const nama = ref("");
const kategori = ref("");
const jumlahStok = ref(0);
const lokasiGudang = ref("");
const pesanValidasi = ref("");

function kirim() {
  pesanValidasi.value = "";

  if (
    !nama.value.trim() ||
    !kategori.value.trim() ||
    !lokasiGudang.value.trim()
  ) {
    pesanValidasi.value = "Semua field wajib diisi.";
    return;
  }
  if (jumlahStok.value < 0) {
    pesanValidasi.value = "Jumlah stok tidak boleh negatif.";
    return;
  }

  emit("submit", {
    nama: nama.value.trim(),
    kategori: kategori.value.trim(),
    jumlah_stok: Number(jumlahStok.value),
    lokasi_gudang: lokasiGudang.value.trim(),
  });

  // reset form
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
      <input v-model="nama" type="text" placeholder="Nama barang" />
      <input v-model="kategori" type="text" placeholder="Kategori" />
      <input v-model.number="jumlahStok" type="number" placeholder="Jumlah stok" min="0" />
      <input v-model="lokasiGudang" type="text" placeholder="Lokasi gudang" />
    </div>
    <p v-if="pesanValidasi" class="status-msg error" style="padding:0.5rem; margin-top:0.5rem">
      {{ pesanValidasi }}
    </p>
    <div class="form-actions">
      <button class="btn btn-outline" @click="emit('batal')">Batal</button>
      <button class="btn btn-primary" @click="kirim">Simpan</button>
    </div>
  </div>
</template>
