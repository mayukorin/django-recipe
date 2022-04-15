$(document).ready(function() {
    let imagesToLoad = document.querySelectorAll('img[data-src]');
    if('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((items, observer) => {
        items.forEach((item) => {
          if(item.isIntersecting) {
            // 1 ピクセルでも見えたら
            loadImages(item.target);
            observer.unobserve(item.target);
          }
        });
      });
      imagesToLoad.forEach((img) => {
        observer.observe(img);
      });
    } else {
      imagesToLoad.forEach((img) => {
        loadImages(img);
      });
    }
});

const loadImages = (image) => {
    image.setAttribute('src', image.getAttribute('data-src'));
    image.onload = () => {
      image.removeAttribute('data-src');
    };
};