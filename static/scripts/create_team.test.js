const { JSDOM } = require("jsdom");
const jquery = require("jquery");

// Set up the global JSDOM environment first
const dom = new JSDOM(`<!DOCTYPE html><html><body><div id="testElement" style="display: none;"></div></body></html>`);
global.window = dom.window;
global.document = dom.window.document;
global.$ = jquery(global.window);

// Now import your script that depends on the document object
global.toggleVisibility = require("./create_teams.js").toggleVisibility;
global.createCustomEvent = require("./create_teams.js").createCustomEvent;

// Mocking jQuery functions that may be used in the functions being tested
console.error = jest.fn();

describe("toggleVisibility function", () => {
    // Store original JSDOM setup for restoration
    let originalDom, originalDocument, originalWindow;

    beforeAll(() => {
        originalDom = dom;
        originalDocument = document;
        originalWindow = window;
    });

    beforeEach(() => {
        // Restore the JSDOM environment before each test
        global.window = originalWindow;
        global.document = originalDocument;
    });


    test("toggles element from visible to hidden", () => {
        document.getElementById("testElement").style.display = "block";
        toggleVisibility("testElement");
        expect(document.getElementById("testElement").style.display).toBe("none");
    });

    test("logs warning for non-existent element", () => {
        console.warn = jest.fn();
        toggleVisibility("nonExistentElement");
        expect(console.warn).toHaveBeenCalledWith("Element not found:", "nonExistentElement");
    });


    afterEach(() => {
        // Clean up the global DOM to ensure tests are isolated
        dom.window.close();
        delete global.window;
        delete global.document;
    });
});


afterAll(() => {
    // Clean up the global JSDOM environment
    dom.window.close();
    delete global.window;
    delete global.document;
});


