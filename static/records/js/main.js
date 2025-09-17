let overlayDiv = document.querySelector(".overlay_box")

const toggleOverlay = () => {
    overlayDiv.classList.toggle("active");
}

let hamburger = document.querySelector(".icon.hamburger")
let cancel = document.querySelector(".overlay_box .cancel")

hamburger.addEventListener('click', toggleOverlay)
cancel.addEventListener('click', toggleOverlay)
