document.addEventListener("DOMContentLoaded", function () {
    // Carousel
    let carouselIndex = 0;
    const carouselItems = document.querySelectorAll(".carousel-item");
    const totalItems = carouselItems.length;

    function showCarouselItem(index) {
        carouselItems.forEach((item, i) => {
            item.style.display = i === index ? "block" : "none";
        });
    }

    function nextCarouselItem() {
        carouselIndex = (carouselIndex + 1) % totalItems;
        showCarouselItem(carouselIndex);
    }

    function prevCarouselItem() {
        carouselIndex = (carouselIndex - 1 + totalItems) % totalItems;
        showCarouselItem(carouselIndex);
    }

    document.querySelector(".next").addEventListener("click", nextCarouselItem);
    document.querySelector(".prev").addEventListener("click", prevCarouselItem);

    // Automatically change carousel item every 10 seconds
    setInterval(nextCarouselItem, 10000);

    showCarouselItem(carouselIndex);

    // Scroll to top button
    const scrollTopBtn = document.getElementById("scrollTopBtn");

    window.addEventListener("scroll", () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add("show");
        } else {
            scrollTopBtn.classList.remove("show");
        }
    });

    scrollTopBtn.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
