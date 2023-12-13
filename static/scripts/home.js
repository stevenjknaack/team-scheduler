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
     * @todo look into making the notification bar a flask template
     * handle:
     * 0. get notifications from backend
     * 1. display the dropdown when click 
     * 2. hide the drop down if clicking outside of it
     */

    // handle 1: display the dropdown when click 
    $(".notification-btn").on("click", function () {
        // make HTTP request to the Flask backend
        fetch(`/get-notifications`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // get notificiation bar and empty it
            let notificationBar = document.querySelector('.notification-dropdown')
            notificationBar.innerHTML = '';
            
            // display empty message if there are no notifications
            if (data.length === 0) {
                notificationBar.innerHTML = `<div class="notification-item">\n`
                + `<p>No notifications yet!</p>`
                + '</div>'
            }

            // populate the bar 
            for (let key in data) {
                let group = data[key]
                console.log(group)
                notificationBar.innerHTML += `<div class="notification-item">\n`
                    + `<p>You're invited to ${group['name'] || 'Unnamed Group'}</p>\n`
                    + `<p class="notify-id">Id: <span class="group_id_box">${group['id']}</span></p>`
                    + `<button class="accept-btn" onclick="handleInvite(${group['id']}, this.parentElement)">Accept</button>\n`
                    + `<button class="decline-btn" onclick="handleInvite(${group['id']}, this.parentElement, false)">Decline</button>\n`
                    + '</div>'
            }

            // toggles the display of the dropdown between hide and show
            $(".notification-dropdown").toggle();
        })
        .catch(error => {
            console.error('Error: ', error); // if error, print out error
        });
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
     * Functionality for handling delete button on groups
     */
    function deleteGroup(groupId) {
        fetch(`/delete-group/${groupId}`, {
            method: "DELETE",
        })
        .then(function(response) {
            if (response.ok) {
                // Reload the page to reflect the changes
                location.reload();
            } else {
                console.log("Failed to delete the group.");
            }
        })
        .catch(function(error) {
            console.error("Error:", error);
        });
    }

    // Event delegation for dynamically added delete buttons
    $(document).on("click", ".delete-group-btn", function(event) {
        event.preventDefault();
        var groupId = $(this).data("group-id");
        deleteGroup(groupId);
    });
    /**
     * Functionality redirect to group page when group box clicked
     */

    // Get all admin group divs
    var adminGroups = document.querySelectorAll('.admin-group');

    // Add click event listener to each admin group div
    adminGroups.forEach(function (group) {
        group.addEventListener('click', function (event) {
            // Check if the clicked element is the delete button
            if (!event.target.classList.contains('delete-group-btn')) {
                // Redirect to the group's page
                var groupUrl = group.getAttribute('data-group-url');
                window.location.href = groupUrl;
            }
        });
    });
});

/**
  * Handles a group invite
  * 
  * @param group_id id of the group to make the user a participant of
  * @param notificationItem the item containing the invite
  * @param acceptInvite true means accept, false means decline
  */
function handleInvite(group_id, notificationItem, acceptInvite = true) {
    // decide route
    let route = `/change_group_role/${group_id}/participant`;
    if (!acceptInvite) route = `/delete_from_group/${group_id}`
    
    // complete POST
    fetch(route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .catch(error => {
        console.error('Error: ', error); // if error, print out error
    });

    // remove invite from notifications
    notificationItem.style.display = 'none';
}
