document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 0;  // Başlangıç görseli
    const images = document.querySelectorAll('.carousel-item');  // Görselleri alıyoruz
    const totalImages = images.length;
    const carouselImages = document.querySelector('.carousel-images');  // Görsellerin bulunduğu container

    // Sol kaydırma (geri gitme)
    document.querySelector('.carousel-btn.left').addEventListener('click', function () {
        currentIndex = (currentIndex === 0) ? totalImages - 1 : currentIndex - 1;
        carouselImages.style.transform = `translateX(-${currentIndex * 100}%)`; // Görselleri kaydırır
    });

    // Sağ kaydırma (ileri gitme)
    document.querySelector('.carousel-btn.right').addEventListener('click', function () {
        currentIndex = (currentIndex === totalImages - 1) ? 0 : currentIndex + 1;
        carouselImages.style.transform = `translateX(-${currentIndex * 100}%)`; // Görselleri kaydırır
    });
});
// Arka plana tıklanma olayı ekle
document.getElementById("background-image").addEventListener("click", function() {
    // Sayfayı başka bir sayfaya yönlendirmek için window.location.href kullanılır.
    window.location.href = "https://www.siteniz.com"; // Buraya gitmek istediğiniz URL'yi yazın.
});




// Open modal on button click
aboutButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const doctor = e.target.previousElementSibling.textContent; // Get doctor name
        doctorName.textContent = doctor;
        doctorInfo.textContent = doctorData[doctor] || 'No information available for this doctor.';
        modal.style.display = 'block';
    });
});

// Close modal when clicking the close button
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close modal when clicking outside of the modal content
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});



// Modal functionality
const aboutButtons = document.querySelectorAll('.about-btn');
const modal = document.getElementById('doctor-modal');
const closeBtn = document.querySelector('.close-btn');
const doctorName = document.getElementById('doctor-name');
const doctorInfo = document.getElementById('doctor-info');

// Data for doctors
const doctorData = {
    'Dr. John Doe': 'Dr. John Doe is a highly experienced cardiologist with over 20 years in the field.',
    'Dr. Jane Smith': 'Dr. Jane Smith specializes in pediatrics and has a deep passion for children\'s health.',
    'Dr. Emily White': 'Dr. Emily White is known for her expertise in orthopedics and sports medicine.',
    'Dr. Michael Black': 'Dr. Michael Black focuses on neurology and is a leader in brain research.',
    'Dr. Sarah Brown': 'Dr. Sarah Brown is a renowned dermatologist, specializing in skin conditions and treatments.',
    'Dr. Robert Green': 'Dr. Robert Green is a family physician with a holistic approach to healthcare.'
};

// Open modal on button click
aboutButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const doctor = e.target.parentElement.querySelector('img').alt; // Get doctor name from alt attribute
        doctorName.textContent = doctor;
        doctorInfo.textContent = doctorData[doctor] || 'No information available for this doctor.';
        modal.style.display = 'flex';
    });
});

// Close modal when clicking the close button
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close modal when clicking outside of the modal content
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

//pencere açılması
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.style.display = 'flex';
    }
  }
  
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.style.display = 'none';
    }
  }

  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show'); // Modal'i görünür yap
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show'); // Modal'i gizle
    }
}


document.getElementById("randevuForm")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const doktorId = document.getElementById("doktorId").value; // Doktor ID'sini alın
    const hastaAd = document.getElementById("hastaAdi").value; // Hasta adı
    const hastaSoyad = document.getElementById("hastaSoyadi").value; // Hasta soyadı
    const tarih = document.getElementById("tarih").value; // Tarih

    fetch("http://127.0.0.1:5000/randevu-ekle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            doktor_id: doktorId,
            hasta_ad: hastaAd,
            hasta_soyad: hastaSoyad,
            tarih: tarih,
            durum: "Beklemede" // Varsayılan durum
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("API isteği başarısız oldu!");
        }
        return res.json();
    })
    .then(data => alert("Randevu alındı: " + JSON.stringify(data)))
    .catch(error => console.error("Hata oluştu:", error));
});


