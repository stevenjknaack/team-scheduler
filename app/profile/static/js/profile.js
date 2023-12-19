"use strict";

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
    getAvailBlocks();

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

    // Onclick function for opening the create avail modal
    $("#create-avail-btn").on("click", function () {
        $("#avail-modal").show();
    });
    // Onclick function for closing the create avail modal
    $(".close").on("click", function () {
        $("#avail-modal").hide();
    });

    // Functionality for handling avail form submission
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

    // Onclick function for delete avail button
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

    // Onclick function for saveScheduleButton
    $("#saveScheduleButton").on("click", function () { 
        saveAvailBlocks()
    });
});

/**
 * Function to save the current schedule.
 * It collects availability blocks from the UI, constructs a data payload,
 * and sends it to the server using an AJAX POST request.
 */
function saveAvailBlocks() {
    // Collect all availability blocks from the UI
    var availBlocks = $(".day .avail-block");
    var scheduleData = [];

    // Iterate over each availability block to construct the schedule data
    availBlocks.each(function () {
        var block = $(this);
        var day = block.closest(".day").attr("id");
        var startTime = block.data("start-time") || "No start time set";
        var timeText = block.text().trim();
        var timeMatch = timeText.match(/\(([^)]+)\)/);

        var endTime = "No end time";
        if (timeMatch && timeMatch[1]) {
            var times = timeMatch[1].split(" - ");
            if (times.length === 2) {
                endTime = times[1];
            }
        }
        // Add the schedule block data to the scheduleData array
        scheduleData.push({ day, startTime, endTime });
    });

    // AJAX request to send the schedule data to the server
    $.ajax({
        url: "./save_schedule", // The URL to the Flask route
        type: "POST", // Usually, data is sent with POST
        contentType: "application/json;charset=UTF-8", // The type of content being sent
        data: JSON.stringify({ schedule: scheduleData }), // The actual data
        dataType: "json", // The type of data we're expecting in return from the server
        success: function (response) {
            // Handle success - perhaps notifying the user that the data was saved
            console.log(response); // Log the response from the server
            alert("Schedule saved successfully.");
            window.location.href = "/home";
        },
        error: function (xhr, status, error) {
            // Handle errors
            console.error(error); // Log the error
            alert("An error occurred while saving the schedule.");
        },
    });
}

/**
 * Fetches availability blocks for the current user and displays them on the profile page.
 */
function getAvailBlocks() {
    // Endpoint where the availability data is available, adjust the URL as needed
    const url = `./get_schedule`;

    // Make a GET request to the server using jQuery's Ajax
    $.ajax({
        url: url,
        type: "GET",
        dataType: "json", // Expecting JSON data in response
        success: function (data) {
            // Handle the data - this is where you would update the UI
            console.log("Availability blocks:", data);
            displayAvailBlocks(data); // Assuming this is a function you've written to update the UI
        },
        error: function (xhr, status, error) {
            console.error("Error fetching availability data:", error);
        },
    });
}

/**
 * Function to display availability blocks on the profile page.
 * @param {Object[]} availBlocks - An array of availability block objects.
 */
function displayAvailBlocks(availBlocks) {
    // Clear existing blocks
    const availBlocksContainer = document.getElementById("avail-blocks");
    availBlocksContainer.innerHTML = "";

    // Loop through each availability block and create an element for it
    availBlocks.forEach((block) => {
        // Create a new div element for the availability block
        const blockDiv = document.createElement("div");
        blockDiv.classList.add(
            "avail-block",
            "ui-draggable",
            "ui-draggable-handle"
        );

        // Set the data attribute for start time
        blockDiv.setAttribute("data-start-time", block.startTime);

        // Set the style attributes
        blockDiv.style.backgroundColor = "#555";
        blockDiv.style.borderRadius = "5px";
        blockDiv.style.padding = "5px";
        blockDiv.style.marginBottom = "5px";
        blockDiv.style.cursor = "move";
        blockDiv.style.position = "relative";
        blockDiv.style.left = "auto";
        blockDiv.style.top = "auto";

        // Create and append the delete button
        const deleteBtn = document.createElement("span");
        deleteBtn.classList.add("delete-btn");
        deleteBtn.textContent = "×";
        blockDiv.appendChild(deleteBtn);

        // Set the text content for the time interval
        blockDiv.appendChild(
            document.createTextNode(` (${block.startTime} - ${block.endTime})`)
        );

        // Append this block to the respective day div in the schedule-container
        const dayDiv = document.getElementById(block.day.toLowerCase());
        if (dayDiv) {
            dayDiv.appendChild(blockDiv);
        }
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
        return new Date("1970/01/01 " + timeA) - new Date("1970/01/01 " + timeB);
    });

    // Append the sorted avail blocks back into the day box
    $avails.each(function () {
        $dayBox.append(this);
    });
}

// Conditionally export the module for testing
if (typeof module !== "undefined" && module.exports) {
    module.exports = { sortAvails, displayAvailBlocks, getAvailBlocks, saveAvailBlocks };
}
