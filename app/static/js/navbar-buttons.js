"use strict";

$(document).ready(function () {
  /** functionality for logout function  
       * handle:
       * 1. when welcome is click, the function will become logut
       * 2. when user clicks anywhere outside the logout button, it switch back to welcome 
      */

      // handle 1: when welcome is click 
      $("#welcomeButton").on("click", function () {
        // hide welcome
        // show logout
        $(this).hide();
        $("#logoutForm").show();
    });

    // handle 2: switch back to the Welcome button 
    $(document).on("click", function (event) {
        // if the current button is logout
        // hide logout and show welcome
        if (
            !$(event.target).closest("#logoutForm").length &&
            !$(event.target).closest("#welcomeButton").length
        ) {
            $("#logoutForm").hide();
            $("#welcomeButton").show();
        }
    });
});