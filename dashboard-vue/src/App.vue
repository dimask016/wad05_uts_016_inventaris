
<script setup>
import { ref, computed, onMounted } from "vue";
import RingkasanTiles from "./components/RingkasanTiles.vue";
import TambahBarangForm from "./components/TambahBarangForm.vue";
import BarangCard from "./components/BarangCard.vue";

/* ============================================================
   Konfigurasi API — IP publik EC2 port 8000
   ============================================================ */
const API_URL = "http://3.24.168.188:8000/barang";

/* ============================================================
   State utama
   ============================================================ */
const barangList = ref([]);
const keadaan = ref("idle"); // idle | loading | error | empty | success
const pesanError = ref("");

/* ============================================================
   State pencarian & urutan
   ============================================================ */
const queryPencarian = ref("");
const urutan = ref("asc"); // "asc" | "desc"
const tampilForm = ref(false);

/* ============================================================
   Fetch data dari backend FastAPI
   ============================================================ */
async function muatBarang() {
  keadaan.value = "loading";
  pesanError.value = "";
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      barangList.value = [];
      keadaan.value = "empty";
      return;
    }

    barangList.value = data;
    keadaan.value = "success";
  } catch (err) {
    console.error("Gagal memuat data:", err);
    pesanError.value = err.message || "Gagal memuat data";
    keadaan.value = "error";
  }
}

/* ============================================================
   Computed #1: filter berdasarkan nama atau kategori
   ============================================================ */
const barangTersaring = computed(() => {
  const q = queryPencarian.value.toLowerCase().trim();
  if (!q) return barangList.value;
  return barangList.value.filter(
    (b) =>
      b.nama.toLowerCase().includes(q) ||
      b.kategori.toLowerCase().includes(q)
  );
});

/* ============================================================
   Computed #2: urutkan A-Z / Z-A di atas hasil filter
   ============================================================ */
const barangTampil = computed(() => {
  const list = [...barangTersaring.value];
  list.sort((a, b) => a.nama.localeCompare(b.nama));
  return urutan.value === "asc" ? list : list.reverse();
});

/* ============================================================
   Handler: tambah barang
   ============================================================ */
async function tambahBarang(payload) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail?.[0]?.msg || `HTTP ${response.status}`);
    }
    await muatBarang();
    tampilForm.value = false;
  } catch (err) {
    alert("Gagal menambah barang: " + err.message);
  }
}

/* ============================================================
   Handler: hapus barang
   ============================================================ */
async function hapusBarang(id, nama) {
  if (!confirm(`Hapus barang "${nama}"?`)) return;
  try {
    const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    await muatBarang();
  } catch (err) {
    alert("Gagal menghapus: " + err.message);
  }
}

/* ============================================================
   Helper: badge status stok
   ============================================================ */
function statusStok(jumlah) {
  if (jumlah === 0) return { kelas: "badge-habis", label: "Habis" };
  if (jumlah <= 5) return { kelas: "badge-menipis", label: "Menipis" };
  return { kelas: "badge-aman", label: "Aman" };
}

/* ============================================================
   Lifecycle: muat data saat halaman dibuka
   ============================================================ */
onMounted(muatBarang);
</script>

<template>
  <header class="app-header">
    <h1>Dashboard Inventaris — UTS WAD05</h1>
  </header>

  <main class="app-main">
    <!-- ===== 4 Tile Ringkasan ===== -->
    <RingkasanTiles :barang-list="barangList" />

    <!-- ===== Toolbar ===== -->
    <div class="toolbar">
      <input
        v-model="queryPencarian"
        type="text"
        placeholder="Cari nama atau kategori..."
      />
      <button
        class="btn btn-outline"
        :class="{ active: urutan === 'asc' }"
        @click="urutan = 'asc'"
      >
        A → Z
      </button>
      <button
        class="btn btn-outline"
        :class="{ active: urutan === 'desc' }"
        @click="urutan = 'desc'"
      >
        Z → A
      </button>
      <button class="btn btn-primary" @click="tampilForm = !tampilForm">
        {{ tampilForm ? "Tutup Form" : "+ Tambah Barang" }}
      </button>
    </div>

    <!-- ===== Form Tambah ===== -->
    <TambahBarangForm
      v-if="tampilForm"
      @submit="tambahBarang"
      @batal="tampilForm = false"
    />

    <!-- ===== State Messages ===== -->
    <p v-if="keadaan === 'loading'" class="status-msg">Memuat data...</p>
    <p v-else-if="keadaan === 'error'" class="status-msg error">
      Gagal memuat data: {{ pesanError }}
    </p>
    <p v-else-if="keadaan === 'empty'" class="status-msg">
      Belum ada data barang.
    </p>
    <p
      v-else-if="keadaan === 'success' && barangTampil.length === 0"
      class="status-msg"
    >
      Tidak ada barang yang cocok dengan pencarian "{{ queryPencarian }}".
    </p>

    <!-- ===== Tabel (desktop) ===== -->
    <div
      v-else-if="keadaan === 'success' && barangTampil.length > 0"
      class="table-wrapper"
    >
      <table class="barang-table">
        <thead>
          <tr>
            <th>Nama Barang</th>
            <th>Kategori</th>
            <th>Stok</th>
            <th>Lokasi Gudang</th>
            <th>Status</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="barang in barangTampil" :key="barang.id">
            <td>{{ barang.nama }}</td>
            <td>{{ barang.kategori }}</td>
            <td>{{ barang.jumlah_stok }}</td>
            <td>{{ barang.lokasi_gudang }}</td>
            <td>
              <span
                class="badge"
                :class="statusStok(barang.jumlah_stok).kelas"
              >
                {{ statusStok(barang.jumlah_stok).label }}
              </span>
            </td>
            <td>
              <button
                class="btn btn-danger"
                @click="hapusBarang(barang.id, barang.nama)"
              >
                Hapus
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ===== Kartu (mobile) ===== -->
    <div
      v-if="keadaan === 'success' && barangTampil.length > 0"
      class="kartu-list"
    >
      <BarangCard
        v-for="barang in barangTampil"
        :key="barang.id"
        :barang="barang"
        :status="statusStok(barang.jumlah_stok)"
        @hapus="hapusBarang(barang.id, barang.nama)"
      />
    </div>
  </main>
</template>
