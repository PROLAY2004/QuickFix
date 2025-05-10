// Toggle mobile menu
const mobileMenu = document.getElementById('mobile-menu');
const nav = document.getElementById('nav');

mobileMenu.addEventListener('click', () => {
  nav.classList.toggle('active');
});



//Search Bar efferct
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input"); // Target input field
  const textArray = ["Search Products ...", "Search Services ..."];
  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function typeEffect() {
      const currentText = textArray[textIndex];

      if (isDeleting) {
          searchInput.setAttribute("placeholder", currentText.substring(0, charIndex - 1));
          charIndex--;
      } else {
          searchInput.setAttribute("placeholder", currentText.substring(0, charIndex + 1));
          charIndex++;
      }

      let typingSpeed = isDeleting ? 50 : 100;

      if (!isDeleting && charIndex === currentText.length) {
          typingSpeed = 2000; // Pause before deleting
          isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
          isDeleting = false;
          textIndex = (textIndex + 1) % textArray.length;
          typingSpeed = 500; // Pause before typing new text
      }

      setTimeout(typeEffect, typingSpeed);
  }

  typeEffect(); // Start effect
});



// Offer section
document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".slider");
    const slides = document.querySelectorAll(".slide");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");

    let currentIndex = 0;
    const totalSlides = slides.length;

    function updateSlider() {
        const offset = -currentIndex * 100 + "%";
        slider.style.transform = `translateX(${offset})`;
        prevBtn.style.display = "block";
    }

    nextBtn.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
    });

    prevBtn.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlider();
    });

    // Auto-slide every 3 seconds
    setInterval(() => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
    }, 3000);

    prevBtn.style.display = "block";
});
