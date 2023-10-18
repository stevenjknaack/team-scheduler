'use strict';

document.getElementById("save").addEventListener("click", function() {
  // Use JavaScript to navigate to the profile page
  window.location.href = "{{ url_for('profile') }}";
});