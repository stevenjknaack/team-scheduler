"use strict";

$(document).ready(function () {
    $(".event-box").hide();
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

    /** funtionality for switching between groups and events on the home page 
     * handle 
     * 1. when event is click 
     * 2. when group is click 
     */

    // handle 1: event is click
    $("#showEvents").click(function () {
        // add class to active and selected to event
        // remove class active and selected to group
        // hide group
        // show events
        $(this).addClass("active").addClass("selected");
        $("#showGroups").removeClass("active").removeClass("selected");
        $(".group").hide();
        $(".event-box").show();
    });
    // handle 2: group is click 
    $("#showGroups").click(function () {
        // add class to active and selected to group
        // remove class active and selected to event
        // hide event
        // show group
        $(this).addClass("active").addClass("selected");
        $("#showEvents").removeClass("active").removeClass("selected");
        $(".event-box").hide();
        $(".group").show();
    });

    /**
     * functionality for notification button 
     * handle:
     * 1. display the dropdown when click 
     * 2. hide the drop down if clicking outside of it
     */

    // handle 1: display the dropdown when click 
    $(".notification-btn").on("click", function () {
        // toggles the display of the dropdown between hide and show
        $(".notification-dropdown").toggle();
    });

    // handle 2: hide the drop down if clicking outside of it
    $(document).on("click", function (event) {
        // Hide the dropdown if clicking outside of it
        if (!$(event.target).closest(".notification-container").length) {
            $(".notification-dropdown").hide();
        }
    });

    // link profile button to profile page
    $("#editProfile").on("click", function (event) {
        // Hide the dropdown if clicking outside of it
        window.location.href = '/profile';
    });

    /** funtionality for create group button 
     * handle: 
     * 1. open up the modal when create group is clicked
     * 2. close the modal when (x) is click 
     * 3. close the modal click outside of mdal
     * 
    */

    // Get the modal
    var modal = document.getElementById("createGroupModal");

    // Get the button that opens the modal
    var btn = document.getElementById("createGroupButton"); // Change this line

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // handle 1: When the user clicks the button, open the modal
    btn.onclick = function () {
        modal.style.display = "block";
    };

    // handle 2: When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };

    // Get the modal for joining
    var jmodal = document.getElementById("joinGroupModal");

    // Get the button that opens the modal
    var jbtn = document.getElementById("joinGroupButton");

    // Get the <span> element that closes the modal
    var jspan = document.getElementsByClassName("jclose")[0];

    // handle 1: When the user clicks the button, open the modal
    jbtn.onclick = function () {
        jmodal.style.display = "block";
    };

    // handle 2: When the user clicks on <span> (x), close the modal
    jspan.onclick = function () {
        jmodal.style.display = "none";
    };
    
    // handle 3: When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == jmodal) {
            jmodal.style.display = "none";
        }
    };

    $("#joinGroup").on("click", function (event) {
        // Hide the dropdown if clicking outside of it
        location.reload();
    });

    /**
     * Functionality redirect to group page when group box clicked
     */

    // Get all admin group divs
    var adminGroups = document.querySelectorAll('.admin-group');

    // Add click event listener to each admin group div
    adminGroups.forEach(function (group) {
        group.addEventListener('click', function () {
            // Redirect to the group's page
            var groupUrl = group.getAttribute('data-group-url');
            window.location.href = groupUrl;
        });
    });
});



