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

    // Initialize Flatpickr for Event Start Time
    flatpickr("#eventStartTime", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "h:i K", // 12-hour format with AM/PM
        time_24hr: false, // Use 12-hour format
        defaultHour: 9, // Default start time at 9 AM
        minuteIncrement: 30 // Change as per your requirement
    });

    // Initialize Flatpickr for Event End Time
    flatpickr("#eventEndTime", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "h:i K", // 12-hour format with AM/PM
        time_24hr: false, // Use 12-hour format
        defaultHour: 18, // Default end time at 6 PM
        minuteIncrement: 30 // Change as per your requirement
    });
        

});

// Function to toggle member selection panel visibility
function toggleMemberSelection() {
    var memberSelection = document.getElementById('memberSelection');
    memberSelection.style.display = memberSelection.style.display === 'block' ? 'none' : 'block';
}

// Function to toggle event creation panel visibility
function toggleCreateEvents(){
    var createEvent = document.getElementById('createEvent')
    createEvent.style.display = createEvent.style.display === 'block' ? 'none' : 'block';

}

// Function to toggle the range of people selection panel
function toggleRangeOfPeople() {
    var rangeSelectionDiv = document.getElementById('rangeSelection');
    rangeSelectionDiv.style.display = rangeSelectionDiv.style.display === 'block' ? 'none' : 'block';
}

// Function to toggle project options panel
function toggleProjectOptions() {
    var projectOptions = document.getElementById('projectOptions');
    projectOptions.style.display = projectOptions.style.display === 'block' ? 'none' : 'block';
}

// TO DO: if wanted include name and description, should include year start and end.
// Function to create a custom event and display it
function createCustomEvent() {
    // Get event details from input fields
    var duration = document.getElementById('eventDuration').value;
    var startDay = document.getElementById('eventStartDay').value;
    var endDay = document.getElementById('eventEndDay').value;
    var startTime = document.getElementById('eventStartTime').value;
    var endTime = document.getElementById('eventEndTime').value;
    var createdEventsContainer = document.getElementById('createdEvents');
    createdEventsContainer.style.display = 'block';

    // Create a new div element to display the event
    var newEventDiv = document.createElement('div');
    newEventDiv.className = 'event';
    newEventDiv.textContent = `Duration: ${duration} minutes, From: ${startDay} ${startTime} to ${endDay} ${endTime}`;

    // Set data attributes for each detail
    newEventDiv.setAttribute('data-duration', duration);
    newEventDiv.setAttribute('data-start-day', startDay);
    newEventDiv.setAttribute('data-end-day', endDay);
    newEventDiv.setAttribute('data-start-time', startTime);
    newEventDiv.setAttribute('data-end-time', endTime);

    // Create and configure a delete button for the event
    var deleteBtn = document.createElement('span');
    deleteBtn.textContent = 'X';
    deleteBtn.className = 'delete-btn';
    deleteBtn.onclick = function() {
        this.parentElement.remove();
    };

    // Append the delete button and event div to the container
    newEventDiv.appendChild(deleteBtn);
    createdEventsContainer.appendChild(newEventDiv);  
}



function confirmParticipants() {
    var checkboxes = document.querySelectorAll('#peopleContainer input[type="checkbox"]:checked');
    var selectedContainer = document.getElementById('selectedParticipants');

    // Clear previous selections
    selectedContainer.innerHTML = '';
    selectedContainer.style.display = 'flex';

    checkboxes.forEach(function(checkbox) {
        var participantDiv = document.createElement('div');
        participantDiv.className = 'participant';
        participantDiv.textContent = checkbox.value;

        selectedContainer.appendChild(participantDiv);
    });

    // Hide the container if no participants are selected
    if (checkboxes.length === 0) {
        selectedContainer.style.display = 'none';
    }
    toggleMemberSelection();
}

function confirmRange() {
    var minPeople = document.getElementById('minPeople').value;
    var maxPeople = document.getElementById('maxPeople').value;

    // Validation: Check if both min and max are filled out and max is greater than min
    if (!minPeople || !maxPeople) {
        alert("Please fill out both the minimum and maximum number of people.");
        return; // Stop the function if either field is missing
    }

    if (parseInt(maxPeople) <= parseInt(minPeople)) {
        alert("The maximum number of people must be greater than the minimum.");
        return; // Stop the function if max is not greater than min
    }

    var confirmedRangeContainer = document.getElementById('confirmedRange');
    confirmedRangeContainer.innerHTML = ''; // Clear previous range
    confirmedRangeContainer.style.display = 'block';

    var rangeDiv = document.createElement('div');
    rangeDiv.className = 'range';
    rangeDiv.textContent = `Team Size Range: ${minPeople} to ${maxPeople}`;

    confirmedRangeContainer.appendChild(rangeDiv);
    toggleRangeOfPeople();
}


function createProject() {
    var projectName = document.getElementById('projectName').value;
    var projectDescription = document.getElementById('projectDescription').value;

    // Validation: Check if both name and description are filled out
    if (!projectName || !projectDescription) {
        alert("Please fill out both the project name and description.");
        return; // Stop the function if validation fails
    }

    var projectListContainer = document.getElementById('projectList');
    projectListContainer.style.display = 'flex';

    var projectDiv = document.createElement('div');
    projectDiv.className = 'project';

    var projectNameDiv = document.createElement('div');
    projectNameDiv.className = 'project-name';
    projectNameDiv.textContent = "Name: " + projectName;

    var projectDescriptionDiv = document.createElement('div');
    projectDescriptionDiv.className = 'project-description';
    projectDescriptionDiv.textContent = "Description: " + projectDescription;

    var deleteBtn = document.createElement('span');
    deleteBtn.textContent = 'X';
    deleteBtn.className = 'delete-btn';
    deleteBtn.onclick = function() {
        this.parentElement.remove();
    };

    projectDiv.appendChild(deleteBtn);
    projectDiv.appendChild(projectNameDiv);
    projectDiv.appendChild(projectDescriptionDiv);

    projectListContainer.appendChild(projectDiv);

    document.getElementById('projectName').value = '';
    document.getElementById('projectDescription').value = '';
}


function createTeams() {
    // Find all selected participant elements
    var selectedParticipantElements = document.querySelectorAll('#selectedParticipants .participant');

    // Convert NodeList to an array and extract text content from each element
    var selectedParticipants = [];
    selectedParticipantElements.forEach(function(element) {
        selectedParticipants.push(element.textContent);
    });
    

    // Check if any participants are selected
    if (selectedParticipants.length === 0) {
        alert("Please select at least one participant.");
        return; // Stop the function
    }
    // Gather all created events
    var createdEventsElems = document.querySelectorAll('#createdEvents .event');
    var createdEvents = {};
    createdEventsElems.forEach((eventElem, index) => {
        var eventDetails = {
            duration: eventElem.getAttribute('data-duration'),
            startDay: eventElem.getAttribute('data-start-day'),
            endDay: eventElem.getAttribute('data-end-day'),
            startTime: eventElem.getAttribute('data-start-time'),
            endTime: eventElem.getAttribute('data-end-time')
        };
        createdEvents['event' + (index + 1)] = eventDetails;
    });
    // Check if any events are created
    if (Object.keys(createdEvents).length === 0) {
        alert("Please create at least one event.");
        return; // Stop the function
    }
    // Gather confirmed range of people
    var minPeople = document.getElementById('minPeople').value;
    var maxPeople = document.getElementById('maxPeople').value;
    var confirmedRange = [minPeople, maxPeople];

    // Check if a range is confirmed
    if (!minPeople || !maxPeople) {
        alert("Please confirm the range of people per team.");
        return; // Stop the function
    }
    // Gathering added projects
    var addedProjects = [];
    var projectElements = document.querySelectorAll('#projectList .project');
    
    projectElements.forEach(function(projectElement) {
        var projectNameElement = projectElement.querySelector('.project-name');
        var projectDescriptionElement = projectElement.querySelector('.project-description');

        var projectName = projectNameElement.textContent.replace('Name: ', '').trim();
        var projectDescription = projectDescriptionElement.textContent.replace('Description: ', '').trim();

        addedProjects.push({
            name: projectName,
            description: projectDescription
        });
    });
    // Check if any projects are added
    if (addedProjects.length === 0) {
        alert("Please add at least one project.");
        return; // Stop the function
    }

    // Log the gathered data
    console.log("Selected Participants:", selectedParticipants);
    console.log("Created Events:", createdEvents);
    console.log("Confirmed People Range:", confirmedRange);
    console.log("Added Projects:", addedProjects);
}

