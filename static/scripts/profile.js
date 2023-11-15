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

    
    /** 
    * Funcionality: Make each element with class 'day' a droppable dayBox area for availBlocks
    * {jQuery object} dayBox
    * {jQuery object} availBlocks 
    */
    $(".day").droppable({
        accept: ".avail-block", // Only accept elements with class 'avail-block'
        hoverClass: "over", // Add 'over' class when a draggable is hovered over the droppable

        // Function when a avail block is dropped on a day element
        // {jQuery object} dayBox 
        // {jQuery object} newAvailBlock is a clone of avail block
        drop: function (event, ui) {

            // get the day element that received the drop
            const $dayBox = $(this);

            //  Clone a new avail block from the original avail block to append
            var $newAvailBlock = $(ui.helper).clone().css({
                position: "relative",
                top: "auto",
                left: "auto",
            });

            // Append the cloned avail block to the day box
            $dayBox.append($newAvailBlock);

            // Sort the avails within the day box after the drop
            sortAvails($dayBox);

            // Give draggable functionality on the new avail block
            initDraggable($newAvailBlock);

            // Remove the original dragged item
            $(ui.draggable).remove();
        },
    });

    /** 
     * Functionality for create avail button
    */
    // Click event for opening the create avail modal
    $("#create-avail-btn").on("click", function () {
        $("#avail-modal").show();
    });
    // Click event for closing the avail modal
    $(".close").on("click", function () {
        $("#avail-modal").hide();
    });

    /*
    * Functionality for handling avail form submission
    */
    $("#avail-form").on("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission


        // Retrieve input values from the form
        const startTime = $("#avail-start").val();
        const endTime = $("#avail-end").val();

        // Create and append the new avail block to the container
        // {jQuery object} $availBlock 
        const $availBlock = $("<div></div>", {
            class: "avail-block",
            html:
                '<span class="delete-btn">&times;</span>' +
                " (" +
                startTime +
                " - " +
                endTime +
                ")",
            "data-start-time": startTime,
            style:
                "background-color: #555; border-radius: 5px; padding: 5px; margin-bottom: 5px; cursor: move;",
        }).appendTo("#avail-blocks");

        // Hide the modal after creating the avail block
        $("#avail-modal").hide();

        // Reset the form fields
        $("#avail-form")[0].reset();

        // Initialize draggable functionality for the new avail block
        initDraggable($availBlock);
    });

    // Functionality for delete avail block button
    $(document).on("click", ".delete-btn", function () {
        if (confirm("Are you sure you want to delete this avail?")) {
            $(this).parent().remove();
        }
    });

    /* Function to initialize draggable elements
    * @param {jQuery object} $availBlock 
    */

    function initDraggable($availBlock) {
        $availBlock.draggable({
            revert: "invalid", // avail block will return to its start position when dragging is stopped
            start: function () {
                // Add 'dragging' class when drag starts
                $(this).addClass("dragging");
            },
            stop: function () {
                // Remove 'dragging' class when drag stops
                $(this).removeClass("dragging");
            },
        });
    }

    /* Function to sort avails block inside a given day box
    * @param {jQuery object} $dayBox 
    */

    function sortAvails($dayBox) {
        // Get all the avail blocks within the day box
        var $avails = $dayBox.find(".avail-block").detach();

        // Sort the avail blocks based on the data-start-time attribute
        $avails.sort(function (a, b) {
            var timeA = $(a).data("start-time");
            var timeB = $(b).data("start-time");
            return (
                new Date("1970/01/01 " + timeA) - new Date("1970/01/01 " + timeB)
            );
        });

        // Append the sorted avail blocks back into the day box
        $avails.each(function () {
            $dayBox.append(this);
        });
    }


    /**
     * TODO get availability and display on profile page
     * @param username 
     * @return response as an json
     * 
     */

    function getAvailBlocks(username) {
        // Make request to server 
        // fetch user avail blocks based on username
        // return avail blocks as an json 
    }
    

    /**
     * Fucntionality for save schedule 
     * 1. Get all the {object} availBlocks: {string} day, {string} startTime, {string} endTime
     * 2. pushed it into an array that display all the availBlocks
     * 3. TODO send the array to the backend and insert or update it in availability table through AJAX
     */
    $("#saveScheduleButton").on("click", function () {
        var availBlocks = $('.day .avail-block');
        var scheduleData = [];
        var usernameText = $('#welcomeButton').text(); // Get the text of the welcome button
        var username = usernameText.replace('Welcome, ', '').trim(); // Remove "Welcome," from the text to isolate the username

        availBlocks.each(function () {
            var block = $(this);
            var day = block.closest('.day').attr('id');
            var startTime = block.data('start-time') || 'No start time set';
            var timeText = block.text().trim();
            var timeMatch = timeText.match(/\(([^)]+)\)/);

            var endTime = 'No end time';
            if (timeMatch && timeMatch[1]) {
                var times = timeMatch[1].split(' - ');
                if (times.length === 2) {
                    endTime = times[1]; 
                }
            }

            scheduleData.push({ day, startTime, endTime });
        });

        // Log the collected data to the console
        console.log('Username:', username);
        console.log('Schedule Data:', scheduleData);


        // AJAX request to the server
        $.ajax({
            url: '/save_schedule', // The URL to the Flask route
            type: 'POST',          // Usually, data is sent with POST
            contentType: 'application/json;charset=UTF-8', // The type of content being sent
            data: JSON.stringify({ username, schedule: scheduleData }), // The actual data
            dataType: 'json',      // The type of data we're expecting in return from the server
            success: function (response) {
                // Handle success - perhaps notifying the user that the data was saved
                console.log(response); // Log the response from the server
                alert('Schedule saved successfully.');
            },
            error: function (xhr, status, error) {
                // Handle errors
                console.error(error); // Log the error
                alert('An error occurred while saving the schedule.');
            }
        });


    });



});

// link profile button to profile page
$("#goHome").on("click", function (event) {
    // Hide the dropdown if clicking outside of it
    window.location.href = '/home';
});


