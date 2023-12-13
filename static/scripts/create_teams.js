'use strict';

document.addEventListener('DOMContentLoaded', (event) => {

    // Event listener for checking/unchecking all checkboxes
    document.getElementById('checkAll').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('#peopleContainer .member input[type="checkbox"]');
        const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);

        checkboxes.forEach((checkbox) => {
            checkbox.checked = !allChecked;
        });

        this.textContent = allChecked ? "Check All" : "Uncheck All";
    });



    // Function to filter and search people based on input
    window.searchPeople = function () {

        // Declare variables for input field, filter text, list of people, individual people entries, and loop index
        var input, filter, peopleList, peopleEntries, i, personName, txtValue;

        // Get the search input by its ID
        input = document.getElementById('searchPeople');
        // Get the search term and convert it to uppercase for case-insensitive comparison
        filter = input.value.toUpperCase();
        // Get the container that holds all people entries
        peopleList = document.getElementById("peopleContainer");
        // Get all people entry elements within the container
        peopleEntries = peopleList.getElementsByClassName('member');

        // Loop through all people entries in the list
        for (i = 0; i < peopleEntries.length; i++) {
            // For each entry, get the text content directly inside the label element
            personName = peopleEntries[i].textContent || peopleEntries[i].innerText;
            // Trim and convert the text content to uppercase for comparison
            txtValue = personName.trim().toUpperCase();
            // Check if the person's name contains the search term
            if (txtValue.indexOf(filter) > -1) {
                // If the name contains the search term, display the entry
                peopleEntries[i].style.display = "";
            } else {
                // If the name does not contain the search term, hide the entry
                peopleEntries[i].style.display = "none";
            }
        }
    };

    var durationInput = document.getElementById('eventDuration');

    durationInput.addEventListener('input', function (e) {
        var value = parseInt(e.target.value, 10);

        if (isNaN(value)) {
            e.target.setCustomValidity("Please enter a valid number.");
        } else {
            e.target.setCustomValidity("");
        }

        // This is important for some browsers to ensure the message shows
        e.target.reportValidity();
    });

});

/**
 * Toggles the visibility of a specified HTML element.
 * 
 * @param {string} elementId - The ID of the HTML element whose visibility is to be toggled.
 * 
 * This function first tries to find an element by its ID. If the element is found,
 * its display style is toggled between 'none' (hidden) and 'block' (visible).
 * If the element is not found, a warning is logged to the console.
 */
function toggleVisibility(elementId) {
    var element = document.getElementById(elementId);
    console.log(elementId)
    if (element) {
        element.style.display = element.style.display === 'block' ? 'none' : 'block';
    } else {
        console.warn('Element not found:', elementId);
    }
}

/**
 * Creates a custom event and adds it to the event display area.
 * 
 * This function retrieves event details from input fields, performs basic validation,
 * and then creates a new event div to display the event information. It also includes
 * a delete button for each event that allows the event to be removed from the display area.
 * After creating an event, the input fields are optionally cleared.
 */
function createCustomEvent() {
    // Retrieve event details from input fields and trim whitespace
    var eventName = document.getElementById('eventName').value.trim();
    var eventDescription = document.getElementById('eventDescription').value.trim();
    var duration = parseInt(document.getElementById('eventDuration').value, 10);

    // Retrieve the selected event type from the dropdown
    var typeSelect = document.getElementById('type');
    var eventType = typeSelect.options[typeSelect.selectedIndex].value;

    var createdEventsContainer = document.getElementById('createdEvents');

    // Perform basic validation on input fields
    if (!eventName) {
        alert("Please enter an event name.");
        return;
    }
    if (!eventDescription) {
        alert("Please enter an event description.");
        return;
    }
    if (isNaN(duration)) {
        alert("Please enter a valid duration in minutes");
        return;
    }

    // Make the container for created events visible
    createdEventsContainer.style.display = 'block';

    // Create a new div element to display the event details
    var newEventDiv = document.createElement('div');
    newEventDiv.className = 'event';
    newEventDiv.innerHTML = `<strong>${eventName}</strong><br>Description: ${eventDescription}<br>Duration: ${duration} minutes<br>Type: ${eventType}`;

    // Set data attributes for each event detail
    newEventDiv.setAttribute('data-name', eventName);
    newEventDiv.setAttribute('data-description', eventDescription);
    newEventDiv.setAttribute('data-duration', duration);
    newEventDiv.setAttribute('data-type', eventType);

    // Create and configure a delete button for each event
    var deleteBtn = document.createElement('span');
    deleteBtn.textContent = 'X';
    deleteBtn.className = 'delete-btn';
    deleteBtn.onclick = function () {
        this.parentElement.remove();
        if (createdEventsContainer.children.length === 0) {
            createdEventsContainer.style.display = 'none';
        }
    };

    // Append the delete button and the event div to the events container
    newEventDiv.appendChild(deleteBtn);
    createdEventsContainer.appendChild(newEventDiv);

    // Clear the input fields after creating the event
    document.getElementById('eventName').value = '';
    document.getElementById('eventDescription').value = '';
    document.getElementById('eventDuration').value = '';
    document.getElementById('type').selectedIndex = 0; // Reset dropdown to the first option
    toggleVisibility('createEvent');
}




/**
 * Confirms the selected participants and displays them in a designated container.
 * 
 * This function retrieves all selected checkboxes within the 'peopleContainer',
 * creates a div element for each selected participant, and appends it to the
 * 'selectedParticipants' container. If no participants are selected, the container
 * is hidden. The function also toggles the visibility of the member selection panel.
 */
function confirmParticipants() {
    // Retrieve all checked checkboxes in the 'peopleContainer'
    var checkboxes = document.querySelectorAll('#peopleContainer input[type="checkbox"]:checked');
    var selectedContainer = document.getElementById('selectedParticipants');

    // Clear the container to remove any previous selections
    selectedContainer.innerHTML = '';
    selectedContainer.style.display = 'flex';

    // Iterate over each checked checkbox
    checkboxes.forEach(function (checkbox) {
        // Create a new div element for each selected participant
        var participantDiv = document.createElement('div');
        participantDiv.className = 'participant';
        participantDiv.textContent = checkbox.value; // Set the participant's name as text

        // Append the participant div to the selected container
        selectedContainer.appendChild(participantDiv);
    });

    // If no checkboxes are checked, hide the 'selectedParticipants' container
    if (checkboxes.length === 0) {
        selectedContainer.style.display = 'none';
    }

    // Toggle the visibility of the member selection panel
    toggleVisibility('memberSelection');
}


/**
 * Confirms the selected range of people and displays it in a designated container.
 * 
 * This function retrieves the values for minimum and maximum number of people from
 * input fields, performs validation checks, and then displays the confirmed range
 * in the 'confirmedRange' container. It also toggles the visibility of the range
 * selection panel.
 */
function confirmRange() {
    // Retrieve values for minimum and maximum number of people
    var minPeople = document.getElementById('minPeople').value;
    var maxPeople = document.getElementById('maxPeople').value;

    // Validation: Check if both minimum and maximum values are filled out
    if (!minPeople || !maxPeople) {
        alert("Please fill out both the minimum and maximum number of people.");
        return; // Exit the function if either field is missing
    }

    // Validation: Check if the maximum is greater than the minimum
    if (parseInt(maxPeople) <= parseInt(minPeople)) {
        alert("The maximum number of people must be greater than the minimum.");
        return; // Exit the function if max is not greater than min
    }

    // Get the container for displaying the confirmed range
    var confirmedRangeContainer = document.getElementById('confirmedRange');
    confirmedRangeContainer.innerHTML = ''; // Clear the container of previous ranges
    confirmedRangeContainer.style.display = 'block';

    // Create a new div element to display the confirmed range
    var rangeDiv = document.createElement('div');
    rangeDiv.className = 'range';
    rangeDiv.textContent = `Team Size Range: ${minPeople} to ${maxPeople}`;

    // Append the range div to the confirmed range container
    confirmedRangeContainer.appendChild(rangeDiv);

    // Toggle the visibility of the range selection panel
    toggleVisibility('rangeSelection');
}



/**
 * Gathers data for team creation, including selected participants, created events, and confirmed people range.
 * 
 * This function compiles a list of selected participants, checks if any events have been created,
 * and confirms the range of people per team. If any of these criteria are not met, it alerts the user
 * and stops the execution. Finally, it logs the gathered data for team creation.
 */
function createTeams() {
    // Find all elements representing selected participants
    var selectedParticipantElements = document.querySelectorAll('#selectedParticipants .participant');

    // Convert NodeList to an array and extract text content from each element
    var selectedParticipants = [];
    selectedParticipantElements.forEach(function (element) {
        selectedParticipants.push(element.textContent);
    });

    // Check if any participants are selected and alert if none are found
    if (selectedParticipants.length === 0) {
        alert("Please select at least one participant.");
        return; // Exit the function if no participants are selected
    }

    // Gather data from all created event elements
    var createdEventsElems = document.querySelectorAll('#createdEvents .event');
    var createdEvents = {};
    createdEventsElems.forEach((eventElem, index) => {
        var eventDetails = {
            duration: eventElem.getAttribute('data-duration'),
            eventName: eventElem.getAttribute('data-name'),
            eventDescription: eventElem.getAttribute('data-description'),
        };
        createdEvents['event' + (index + 1)] = eventDetails;
    });

    // Check if any events have been created and alert if none are found
    if (Object.keys(createdEvents).length === 0) {
        alert("Please create at least one event.");
        return; // Exit the function if no events are created
    }

    // Gather the confirmed range of people per team
    var minPeople = document.getElementById('minPeople').value;
    var maxPeople = document.getElementById('maxPeople').value;
    var confirmedRange = [minPeople, maxPeople];

    // Check if a range of people has been confirmed and alert if not
    if (!minPeople || !maxPeople) {
        alert("Please confirm the range of people per team.");
        return; // Exit the function if range is not confirmed
    }

    // Log the gathered data for review or further processing
    console.log("Selected Participants:", selectedParticipants);
    console.log("Created Events:", createdEvents);
    console.log("Confirmed People Range:", confirmedRange);
}


// Conditionally export the module for testing
if (typeof module !== "undefined" && module.exports) {
    module.exports = { toggleVisibility, createCustomEvent, confirmParticipants, confirmRange, createTeams};
}
