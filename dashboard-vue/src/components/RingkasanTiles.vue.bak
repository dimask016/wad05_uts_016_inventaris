<script setup>
import { computed } from "vue";

const props = defineProps({
  barangList: {
    type: Array,
    required: true,
  },
});

/* 4 computed terpisah, semua dari data barang yang sama */
const totalBarang = computed(() => props.barangList.length);

const stokMenipisHabis = computed(
  () => props.barangList.filter((b) => b.jumlah_stok <= 5).length
);

const jumlahKategori = computed(
  () => new Set(props.barangList.map((b) => b.kategori)).size
);

const totalUnit = computed(
  () => props.barangList.reduce((sum, b) => sum + b.jumlah_stok, 0)
);
</script>

<template>
  <section class="tiles">
    <div class="tile">
      <span class="tile-label">Total Barang</span>
      <span class="tile-value">{{ totalBarang }}</span>
    </div>
    <div class="tile">
      <span class="tile-label">Stok Menipis + Habis</span>
      <span class="tile-value">{{ stokMenipisHabis }}</span>
    </div>
    <div class="tile">
      <span class="tile-label">Jumlah Kategori</span>
      <span class="tile-value">{{ jumlahKategori }}</span>
    </div>
    <div class="tile">
      <span class="tile-label">Total Unit</span>
      <span class="tile-value">{{ totalUnit }}</span>
    </div>
  </section>
</template>
