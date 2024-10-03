// equipmentSearch.js
document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('searchEquipment');

    if (searchInput) {
      searchInput.addEventListener('input', function(e) {
        var searchTerm = e.target.value.toLowerCase();
        var equipmentItems = document.querySelectorAll('.equipment-item');

        equipmentItems.forEach(function(item) {
          var title = item.querySelector('h2').textContent.toLowerCase();
          if (title.includes(searchTerm)) {
            item.style.display = '';
          } else {
            item.style.display = 'none'; 
          }
        });
      });
    }
  });
