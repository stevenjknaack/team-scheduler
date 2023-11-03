"use strict";
/** creating a draggable calendar feature we need to handle it in 3 different stages.
 * 1. when the mouse is pressed on a time slot
 * 2. when the mouse is drag over the time slot
 * 3. when the mouse is release
 * 
 */
let isDragging = false;
let startTimeBox = null;
let initialState = false; // Store the initial state of the cell

/** stage 1: Start drag when mouse is pressed on a time slot.
 * call addEventListener(type: mousedown)
*/
document.addEventListener("mousedown", (e) => {
    // if mouse is click on the time-slot
    // set is dragging = true, startCell to the starting cell and set initialState to the true or false depends on if it is previous selected
    // call toggleSelection function
    if (e.target.matches(".time-slot")) {
        isDragging = true;
        startTimeBox = e.target;
        initialState = !startTimeBox.classList.contains("drag-selecting");
        toggleSelection(startTimeBox);
    }
});

/** stage 2: Handle drag over other time slots
 * call addEventListener(type: mouseover)
*/
document.addEventListener("mouseover", (e) => {
    // if is dragging and is drag toward the time-slot
    // call toggleSelection function
    if (isDragging && e.target.matches(".time-slot")) {
        // since the initial state is set at the when mouse is click, selectedtime slot will still be selected
        toggleSelection(e.target);
    }
});

/** stage 3: End drag on mouse release
 * call addEventListener(type: mouseup)
*/
document.addEventListener("mouseup", () => {
    // set isDragging to false and start cell to null
    if (isDragging) {
        isDragging = false;
        startTimeBox = null;
    }
});

/**
 * helper function called to add and remove drag-selecting
 * @param timeBox the time slot
 */
function toggleSelection(timeBox) {
    // if the box is not selected, it will be selected
    // else it will no be selected
    if (initialState) {
        timeBox.classList.add("drag-selecting");
    } else {
        timeBox.classList.remove("drag-selecting");
    }
}