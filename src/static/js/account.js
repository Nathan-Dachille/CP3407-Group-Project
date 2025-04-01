document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the last focused date from sessionStorage or default to today
    let storedDate = sessionStorage.getItem("focusDate");
    let focusDate = storedDate ? new Date(storedDate) : new Date(); // Start with the user's current date

    document.getElementById("prev-week").addEventListener("click", () => {
        focusDate.setDate(focusDate.getDate() - 7);
        sessionStorage.setItem("focusDate", focusDate.toISOString());
        updateWeekInfo(focusDate);
    });

    document.getElementById("next-week").addEventListener("click", () => {
        focusDate.setDate(focusDate.getDate() + 7);
        sessionStorage.setItem("focusDate", focusDate.toISOString());
        updateWeekInfo(focusDate);
    });

    // Trigger the AJAX request when the page loads
    updateWeekInfo(focusDate);
});

function updateWeekInfo(focusDate = null) {
    if (!focusDate) {
        let storedDate = sessionStorage.getItem("focusDate");
        focusDate = storedDate ? new Date(storedDate) : new Date();
    }

    // Ensure the date is stored properly in sessionStorage
    sessionStorage.setItem("focusDate", focusDate.toISOString().split('T')[0]);

    // Get today's date (you can change this to any date logic you prefer)
    const formatDate = focusDate.toISOString().split('T')[0]; // Formats date as YYYY-MM-DD

    // Send the new date via AJAX to the server
    fetch(`/profile/?user_date=${formatDate}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data || !data.current_date || !data.week_dates
            || !data.week_number || !data.ava_data) {
            console.error("Invalid data received:", data);
            return;
        }
        console.log("Current Date:", data.current_date);
        console.log("Week Number:", data.week_number);
        console.log("Week Dates:", data.week_dates);
        console.log("Availability Data:", data.ava_data);

        // Subheader Section:
        document.getElementById("week-number").textContent = ` ${data.week_number} `;
        // Apply the ordinal formatting
        const formattedStartDate = formatDateWithOrdinal(data.week_dates[0]);
        const formattedEndDate = formatDateWithOrdinal(data.week_dates[6]);

        document.getElementById("week-range").textContent =
            `${formattedStartDate} - ${formattedEndDate}`;

        const startYear = new Date(Date.parse(data.week_dates[0])).getFullYear();
        const endYear = new Date(Date.parse(data.week_dates[6])).getFullYear();

        document.getElementById("year-display").textContent =
            (startYear !== endYear) ? ` ${startYear} - ${endYear} ` : ` ${startYear} `;

        // Table Section:
        const timetableContainer = document.getElementById("timetable")
        let timetableHTML = '<table class="timetable">';

        // Add table headers
        timetableHTML += `<tr><th><button class="toggle_set" ` +
            `onClick="toggleAvailable({togType:1, target_days:'${data.week_dates}'.split(','), target_hours:[]})">+` +
            `</button></th>`;

        data.week_dates.forEach((date) => {
            // Create a Date object from the date string
            const date_d = new Date(date);
            console.log(date)

            // Get the day name from the Date object
            const dayName = date_d.toLocaleString('en-US', { weekday: 'short' });
            timetableHTML += `<th><button class="toggle_set"` +
            ` onClick="toggleAvailable({togType:1, target_days:'${date}'.split(','), target_hours:[]})">${dayName}`
                +`</button></th>`;
        });

        timetableHTML += `</tr>`;

        // Add table content

        for (let i = 0, weekDates = data.week_dates, avail = data.ava_data; i < 24; i++) {
            let t_string = convertToTimeString(i)

            timetableHTML += `<tr><th><button class="toggle_set" ` +
            `onClick="toggleAvailable({togType:1,target_days:'${weekDates}'.split(','),target_hours:[${[i]}]})">
            ${t_string}</button></th>`;

            for (let j = 0; j < weekDates.length; j++) {
                let currentDate = weekDates[j]; // Get the current date from the week
                // Find availability for this date and time
                let dayAvailability = avail.find(entry => entry.ava_date === currentDate);
                let isAvailable = dayAvailability && dayAvailability.available_hours.includes(i);

                let buttonClass = isAvailable ? "ava" : "n_ava";

                timetableHTML += `<th><button class="toggle_set fields ${buttonClass}"` +
                ` onClick="toggleAvailable({togType:2, target_days:'${weekDates[j]}'.split(','),
                target_hours:[${i}]})">‎</button></th>`;
            }

            timetableHTML += `</tr>`;
        }

        // Insert the HTML into the timetable container
        timetableContainer.innerHTML = timetableHTML;
    })
    .catch(error => console.error("Error fetching data:", error));
}

function convertToTimeString(hour) {
    // Handle hour 0 as 12am, and 12 as 12pm
    if (hour === 0) {
        return "12am";
    } else if (hour === 12) {
        return "12pm";
    }

    // Convert hour to 12-hour format
    const hour12 = hour > 12 ? hour - 12 : hour;

    // Determine AM or PM
    const period = hour >= 12 ? "pm" : "am";

    // Return the formatted time string
    return `${hour12}${period}`;
}

function formatDateWithOrdinal(dateString) {
    const date = new Date(dateString);
    const day = date.getDate();
    const month = date.toLocaleString("en-US", { month: "short" });

    // Function to get ordinal suffix (st, nd, rd, th)
    function getOrdinal(n) {
        if (n > 3 && n < 21) return "th"; // Covers 11th, 12th, 13th
        switch (n % 10) {
            case 1: return "st";
            case 2: return "nd";
            case 3: return "rd";
            default: return "th";
        }
    }

    return `${day}${getOrdinal(day)} of ${month}`;
}

function openModel(modelId) {
    document.getElementById(modelId).style.display = "flex";
}

function closeModel(modelId) {
    document.getElementById(modelId).style.display = "none";
}

function toggleAvailable({togType=0, target_days=[""], target_hours=[]}) {
    const request_data = {
            type: togType,
            days: Array.isArray(target_days) ? target_days : [target_days],
            hours: Array.isArray(target_hours) ? target_hours : [target_hours],
    }
    console.log("Request body:", JSON.stringify(request_data))
    fetch("/toggle_availability/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Needed for Django security
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response", data);
        if (data.success) {
            updateWeekInfo();
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Request failed:", error));
}

function toggleEdit() {
    let displaySpan = document.getElementById("phone_display");
    let inputField = document.getElementById("phone_input");
    let button = document.querySelector(".toggle_edit");

    if (displaySpan.style.display === "none") {
        // Validate the input
        let phoneValue = inputField.value.trim();
        let phoneRegex = /^[\d\s\-\+\(\)]*$/; // Allows digits, spaces, dashes, plus, and parentheses

        if (phoneValue === "" || phoneRegex.test(phoneValue)) {
            // Valid input or blank, save and switch back to text mode
            displaySpan.textContent = phoneValue || "No phone number"; // Fallback text
            displaySpan.style.display = "inline";
            inputField.style.display = "none";
            button.textContent = "⇄"; // Reset button text
        } else {
            alert("Please enter a valid phone number.");
            inputField.focus();
        }
    } else {
        // Switching to edit mode
        inputField.style.display = "inline";
        inputField.focus();
        displaySpan.style.display = "none";
        button.textContent = "✔"; // Change button text to indicate save
    }
}

// Utility function to get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return "";
}