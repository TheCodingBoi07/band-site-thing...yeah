// ----------------------------
// CLIENT-SIDE FORM VALIDATION
// ----------------------------

// Arrow function here because:
// ✅ short and used once
// ✅ keeps code concise for event listeners
const validateBandForm = (event) => {
    const bandName = document.querySelector("input[name='bandname']").value.trim();
    const formedYear = document.querySelector("input[name='formedyear']").value.trim();

    if (!bandName) {
        alert("Band name is required!");
        event.preventDefault(); // Stops form submission
        return false;
    }

    if (formedYear && (formedYear < 1900 || formedYear > new Date().getFullYear())) {
        alert("Please enter a valid Formed Year.");
        event.preventDefault();
        return false;
    }
};

// Anonymous function example:
// ✅ We don't reuse this logic
// ✅ Good example of inline validation
const validateMemberForm = function(event) {
    const memberName = document.querySelector("input[name='membername']").value.trim();
    if (!memberName) {
        alert("Member name is required!");
        event.preventDefault();
        return false;
    }
};

// DOMContentLoaded waits until HTML is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    
    console.log("JavaScript loaded — validation active!");

    // Attach validation only if forms exist on the current page
    const bandForm = document.getElementById("bandForm");
    if (bandForm) {
        bandForm.addEventListener("submit", validateBandForm);
    }

    const memberForm = document.getElementById("memberForm");
    if (memberForm) {
        memberForm.addEventListener("submit", validateMemberForm);
    }
});