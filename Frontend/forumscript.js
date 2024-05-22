// forumscript.js

// Get the modal
var modal = document.getElementById("thread-modal");

// Get the button that opens the modal
var btn = document.getElementById("create-thread-btn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Optional: Add a sort function for the dropdown
document.getElementById("sort-threads").onchange = function() {
    var sortBy = this.value;
    // Implement sorting logic based on sortBy
    console.log("Sorting threads by: " + sortBy);
}
