const { JSDOM } = require("jsdom");
const jquery = require("jquery");

// Set up a new JSDOM instance to simulate the DOM environment for testing
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<body>
    <!-- Mock HTML structure for sortAvails function -->
    <div id="dayBox">
        <div class="avail-block" data-start-time="08:00"></div>
        <div class="avail-block" data-start-time="09:00"></div>
        <div class="avail-block" data-start-time="07:00"></div>
    </div>
    <!-- Mock HTML structure for displayAvailBlocks function -->
    <div id="schedule-container">
        <div class="day" id="monday"></div>
        <!-- Add other day divs as needed -->
    </div>
    <div id="avail-blocks"></div>
</body>
</html>
`);

global.window = dom.window;
global.document = dom.window.document;
global.$ = global.jQuery = jquery(global.window);

// Mocking jQuery functions that may be used in the functions being tested
$.fn.droppable = jest.fn();

// Import the functions to test
global.sortAvails = require("./profile.js").sortAvails;
global.displayAvailBlocks = require("./profile.js").displayAvailBlocks;
global.getAvailBlocks = require("./profile.js").getAvailBlocks;
global.saveAvailBlocks = require("./profile.js").saveAvailBlocks;

describe("sortAvails function", () => {
  test("sorts avail blocks correctly", () => {
    // Setup the mock environment for the test
    const $dayBox = $("#dayBox");

    // Call the function with the mock environment
    sortAvails($dayBox);

    // Collect the start times of each avail block after sorting
    const times = $dayBox
      .find(".avail-block")
      .map(function () {
        return $(this).data("start-time");
      })
      .get();

    // Assert that the avail blocks are sorted correctly
    expect(times).toEqual(["07:00", "08:00", "09:00"]);
  });
});

console.error = jest.fn();
describe("displayAvailBlocks function", () => {
  test("creates and appends availability blocks to the DOM", () => {
    // Mock data to be used for testing
    const mockData = [
      { day: "monday", start_time: "08:00", end_time: "10:00" },
    ];

    // Call the function with the mock data
    displayAvailBlocks(mockData);

    // Check the DOM to see if the function correctly appended the blocks
    const scheduleContainer = document.getElementById("schedule-container");
    expect(scheduleContainer.children.length).toBe(1); // Expect one block to be added
  });
  afterEach(() => {
    // Restore the original console.error implementation
    console.error.mockRestore();
  });
});

describe("getAvailBlocks function", () => {
  let mockSuccessCallback;

  beforeEach(() => {
    // Mock jQuery's ajax function
    mockSuccessCallback = jest.fn();
    $.ajax = jest.fn().mockImplementation(({ success }) => {
      mockSuccessCallback = success;
    });

    console.log = jest.fn();
  });

  afterEach(() => {
    // Restore the original implementations
    jest.restoreAllMocks();
  });

  test("make an AJAX call and reach success callback", () => {
    // Call the function
    getAvailBlocks();

    // Mock response data
    const mockData = [
      { day: "monday", start_time: "08:00", end_time: "10:00" },
    ];

    // Manually invoke the success callback with mock data
    mockSuccessCallback(mockData);

    // Check if success callback was called with the expected data
    expect(console.log).toHaveBeenCalledWith("Availability blocks:", mockData);
  });
});

describe("saveSchedule function", () => {
  beforeEach(() => {
      // Set up a new JSDOM instance for each test to ensure isolation
      const localDom = new JSDOM(`
      <!DOCTYPE html>
      <html>
      <body>
          <div class="day" id="monday">
              <div class="avail-block" data-start-time="08:00">Some text (08:00 - 10:00)</div>
          </div>
          <button id="welcomeButton">Welcome, TestUser</button>
      </body>
      </html>
      `);

      global.window = localDom.window;
      global.document = localDom.window.document;
      global.$ = jquery(global.window);

      // Mock jQuery's ajax function
      $.ajax = jest.fn();
  });

  afterEach(() => {
      // Clean up the global DOM to ensure tests are isolated
      delete global.window;
      delete global.document;
      delete global.$;
  });

  test("sends correct data via AJAX when saving schedule", () => {
      // Call the function
      saveAvailBlocks();

      // Expected data to be sent in AJAX request
      const expectedData = JSON.stringify({
          schedule: [{ day: 'monday', startTime: '08:00', endTime: '10:00' }]
      });

      // Check if AJAX was called with correct parameters
      expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
          url: '/save_schedule',
          type: 'POST',
          contentType: 'application/json;charset=UTF-8',
          data: expectedData,
          dataType: 'json'
      }));
  });
});




