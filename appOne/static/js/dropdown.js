document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.dropdown > a');
    if (dropdown) {
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();  // Prevents the anchor link from navigating
            var dropdownContent = this.nextElementSibling;
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        });
    }
});
