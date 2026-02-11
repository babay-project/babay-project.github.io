<?php
// 1. PENTING: Izinkan akses dari mana saja (agar game/Charles tidak diblokir)
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json; charset=utf-8');

// 2. Setting URL folder sesuai domain kamu
// Karena file ini ada di dalam folder "lib", kita set path-nya ke situ.
$baseUrl = "/lib/"; 
// OPSI LAIN: Jika game minta https, ganti baris atas jadi:
// $baseUrl = "https://babayproject.my.id/lib/";

// 3. Ambil semua file berakhiran .bin di folder tempat file php ini berada
$fileList = glob("*.bin");
$dataFiles = [];

// 4. Loop untuk membaca detail setiap file
foreach ($fileList as $filename) {
    // Cek apakah file benar-benar ada untuk menghindari error
    if (file_exists($filename)) {
        $dataFiles[] = [
            "name" => pathinfo($filename, PATHINFO_FILENAME), // Nama file tanpa .bin
            "url"  => $baseUrl . $filename,                   // URL gabungan (/lib/nama.bin)
            "size" => filesize($filename),                    // Ukuran file otomatis
            "modified" => filemtime($filename)                // Tanggal update otomatis
        ];
    }
}

// 5. Susun struktur akhir sesuai format Ninja Saga
$output = [
    "files" => $dataFiles,
    "count" => count($dataFiles)
];

// 6. Tampilkan hasilnya
echo json_encode($output, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
?>
