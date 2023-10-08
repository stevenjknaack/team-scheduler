'use strict';

// create new frontend-backend connection object
var xhr = null;
let getXmlHttpRequestObject = function () {
    if (!xhr) {
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

// updates date on webpage
function getDate() { 
    let date = new Date().toString();
    document.getElementById('time-container').textContent
        = date;
}
(function () {
    getDate();
})();

// sends message to backend requesting data for given username
function sendData() { 
    let dataToSend = document.getElementById('data-input').value;
    if (!dataToSend) {
        console.log("Data is empty.");
        return;
    }
    console.log("Sending data: " + dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/users", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": dataToSend}));
}

// recieves response from backend and puts data on webpage
function sendDataCallback() { 
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        getDate();
        let dataDiv = document.getElementById('sent-data-container');
        // Set current data text
        let user_data = JSON.parse(xhr.responseText)
        dataDiv.innerHTML = user_data['message'];
    }
}


