// Carousel init for the Paper Atlas hero figures.
document.addEventListener('DOMContentLoaded', function () {
  if (typeof bulmaCarousel !== 'undefined') {
    bulmaCarousel.attach('#results-carousel', {
      slidesToScroll: 1,
      slidesToShow: 1,
      autoplay: true,
      autoplaySpeed: 5000,
      pauseOnHover: true,
      loop: true,
      navigation: true,
      pagination: true
    });
  }
});
