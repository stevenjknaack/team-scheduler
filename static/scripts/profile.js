'use strict';

document.getElementById("createEvent").addEventListener("click", function() {
  // Use JavaScript to navigate to the profile page
  window.location.href = "../create-event";
});

$(document).ready(function () {
    $("#welcomeButton").on("click", function () {
        $("#logoutForm").toggle();
    });
});