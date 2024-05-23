document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("post-modal");
    const createPostBtn = document.querySelector(".create-post-btn");
    const closeBtn = document.querySelector(".close-btn");

    createPostBtn.onclick = function() {
        modal.style.display = "block";
    }

    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
