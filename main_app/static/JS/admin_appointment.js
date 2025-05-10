// booking.js

document.addEventListener('DOMContentLoaded', function () {
    let selectedDate = null;
    let selectedTime = null;
    let currentStartDate;

    const DATE_LIMIT_DAYS = parseInt(document.querySelector('.advance_booking').textContent.trim(), 10);;
    const today = new Date();
    const maxAllowedDate = new Date(today);
    maxAllowedDate.setDate(today.getDate() + DATE_LIMIT_DAYS);
    maxAllowedDate.setHours(0, 0, 0, 0);

    const visibleDays = getVisibleDays();
    currentStartDate = visibleDays >= 7 ? getStartOfWeek(today) : new Date();

    updateCalendarDisplay();

    document.querySelector('.prev-week').addEventListener('click', function (e) {
        e.preventDefault();
        const days = getVisibleDays();
        currentStartDate.setDate(currentStartDate.getDate() - days);
        updateCalendarDisplay();
        clearSelection();
    });

    document.querySelector('.next-week').addEventListener('click', function (e) {
        e.preventDefault();
        const days = getVisibleDays();
        const potentialStartDate = new Date(currentStartDate);
        potentialStartDate.setDate(potentialStartDate.getDate() + days);
        if (potentialStartDate <= maxAllowedDate) {
            currentStartDate = potentialStartDate;
        }
        updateCalendarDisplay();
        clearSelection();
    });

    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.addEventListener('click', function () {
            if (slot.classList.contains('booked') || slot.classList.contains('past') || slot.classList.contains('past-time') || slot.classList.contains('disabled')) return;

            document.querySelectorAll('.time-slot.selected').forEach(el => el.classList.remove('selected'));
            slot.classList.add('selected');

            const dayIndex = Array.from(slot.closest('.time-slots-container').children).indexOf(slot.parentElement);
            const dayHeaders = document.querySelectorAll('.day-header');
            const dayDate = dayHeaders[dayIndex].querySelector('.day-date').textContent;
            const dayName = dayHeaders[dayIndex].querySelector('.day-name').textContent;

            const timeDisplay = slot.textContent;

            selectedDate = `${dayName}, ${formatDate(currentStartDate, dayDate)}`;
            selectedTime = timeDisplay;

            document.getElementById('appointment-date').value = selectedDate;
            document.getElementById('appointment-time').value = selectedTime;

            let selectedTimeText = document.querySelector('.selected-time');
            if (selectedTimeText) {
                selectedTimeText.textContent = `${selectedDate} at ${selectedTime}`;
                selectedTimeText.classList.remove('empty');
            }
            let confirmBtn = document.querySelector('.confirm-btn');
            if (confirmBtn) confirmBtn.disabled = false;
        });
    });

    window.addEventListener('resize', function () {
        const newVisible = getVisibleDays();
        if (newVisible >= 7) {
            currentStartDate = getStartOfWeek(new Date());
        }
        updateCalendarDisplay();
    });

    function updateCalendarDisplay() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const now = new Date();
        const currentTime = now.getHours() * 60 + now.getMinutes();
        const visibleDays = getVisibleDays();

        const dayHeaders = document.querySelectorAll('.day-header');
        const daySlotsContainers = document.querySelectorAll('.day-slots');

        for (let i = 0; i < 7; i++) {
            const date = new Date(currentStartDate);
            date.setDate(date.getDate() + i);
            date.setHours(0, 0, 0, 0);

            const header = dayHeaders[i];
            const slotContainer = daySlotsContainers[i];

            const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
            const dayDate = date.getDate();

            header.querySelector('.day-name').textContent = dayName;
            header.querySelector('.day-date').textContent = dayDate;
            header.classList.toggle('today', isSameDay(date, today));

            const timeSlots = slotContainer.querySelectorAll('.time-slot');
            timeSlots.forEach(slot => {
                slot.classList.remove('past', 'past-time', 'selected', 'disabled');
            });

            // Disable if day is in the past
            if (date < today) {
                timeSlots.forEach(slot => slot.classList.add('past'));
            }
            // Disable past time for today
            else if (isSameDay(date, today)) {
                timeSlots.forEach(slot => {
                    const timeString = slot.dataset.time;


                    let [timePart, modifier] = timeString.trim().split(' ');
                    let [hours, minutes] = timePart.split(':').map(Number);
                    modifier = modifier.toUpperCase();

                    if (modifier === 'PM' && hours !== 12) {
                        hours += 12;
                    }
                    if (modifier === 'AM' && hours === 12) {
                        hours = 0;
                    }
                    const slotTime = hours * 60 + minutes;




                    if (slotTime < currentTime) {
                        slot.classList.add('past-time');
                    }
                });
            }

            // Disable if beyond allowed date
            if (date > maxAllowedDate) {
                timeSlots.forEach(slot => slot.classList.add('disabled'));
                header.style.display = 'none';
                slotContainer.style.display = 'none';
                continue;
            }

            const show = i < visibleDays;
            header.style.display = show ? 'block' : 'none';
            slotContainer.style.display = show ? 'flex' : 'none';
        }

        const endDate = new Date(currentStartDate);
        endDate.setDate(endDate.getDate() + visibleDays - 1);
        document.querySelector('.current-week-range').textContent =
            `${formatDate(currentStartDate)} - ${formatDate(endDate)}, ${endDate.getFullYear()}`;
    }

    function getVisibleDays() {
        const width = window.innerWidth;
        if (width < 400) return 1;
        if (width < 576) return 2;
        if (width < 768) return 3;
        if (width < 992) return 4;
        if (width < 1200) return 5;
        if (width < 1400) return 7;
        return 7;
    }

    function clearSelection() {
        selectedDate = null;
        selectedTime = null;
        document.querySelectorAll('.time-slot.selected').forEach(el => el.classList.remove('selected'));
        let selectedTimeText = document.querySelector('.selected-time');
        if (selectedTimeText) {
            selectedTimeText.textContent = 'No slot selected';
            selectedTimeText.classList.add('empty');
        }
        let confirmBtn = document.querySelector('.confirm-btn');
        if (confirmBtn) confirmBtn.disabled = true;
    }

    function getStartOfWeek(date) {
        const d = new Date(date);
        const day = d.getDay();
        const diff = d.getDate() - day;
        return new Date(d.setDate(diff));
    }

    function formatDate(date, day) {
        if (day) {
            const month = date.toLocaleDateString('en-US', { month: 'short' });
            return `${month} ${day}`;
        } else {
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }
    }

    function isSameDay(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getDate() === date2.getDate();
    }
});







document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("appointment-modal");
    const closeModalBtn = modal.querySelector(".modal-close");
    const closeFooterBtn = document.getElementById("close-details");
    const viewButtons = document.querySelectorAll(".action-btn[title='View Details']");
    const filterSelect = document.getElementById("filter-status");
    const tableRows = document.querySelectorAll(".appointments-table tbody tr");

    const detailFields = {
        customer: document.getElementById("detail-customer"),
        email: document.getElementById("detail-email"),
        phone: document.getElementById("detail-phone"),
        service: document.getElementById("detail-service"),
        time: document.getElementById("detail-time"),
        address: document.getElementById("detail-address"),
        notes: document.getElementById("detail-notes"),
        status: document.getElementById("detail-status")
    };

    // Modal open and content fill
    viewButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            const row = tableRows[index];
            const customerName = row.querySelector("td:nth-child(1) strong")?.textContent.trim() || "-";
            const email = row.querySelector("td:nth-child(1) small")?.textContent.trim() || "-";
            const service = row.querySelector("td:nth-child(2)")?.textContent.trim() || "-";
            const time = row.querySelector("td:nth-child(3)")?.textContent.trim() || "-";
            const statusSpan = row.querySelector("td:nth-child(4) .status-badge");
            const statusText = statusSpan?.textContent.trim() || "-";
            const statusClass = statusSpan?.classList[1] || "confirmed";
            const address = row.querySelector(".address")?.textContent.trim() || "Not available";
            const notes = row.querySelector(".notes")?.textContent.trim() || "No Instructions.";
            const id = row.getAttribute("data-id") || "";  // or row.dataset.id
            const aid = row.getAttribute("data-aid") || ""; // or row.dataset.aid

            // Populate modal fields
            detailFields.customer.textContent = customerName;
            detailFields.email.textContent = email;
            detailFields.service.textContent = service;
            detailFields.time.textContent = time;
            detailFields.status.textContent = statusText;
            detailFields.status.className = `status-badge ${statusClass}`;

            // Placeholder (can be fetched via backend in future)
            detailFields.phone.textContent = "+91 000 000 0000";
            html = `<a href='/Admin/Custom/Appointments/Map/${id}/${aid}/' style="color: var(--admin-primary);text-decoration:none">View on Map  <i class="fas fa-map-marker-alt"></i></a>`;
            console.log(html)
            detailFields.address.innerHTML = html;

            if (notes) {
                detailFields.notes.textContent = notes;
            }


            modal.classList.add("active");
        });
    });

    // Modal close
    function closeModal() {
        modal.classList.remove("active");
    }

    closeModalBtn.addEventListener("click", closeModal);
    closeFooterBtn.addEventListener("click", closeModal);

    window.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeModal();
    });

    window.addEventListener("click", function (e) {
        if (e.target === modal) closeModal();
    });

    // Filter logic
    filterSelect.addEventListener("change", function () {
        const selected = this.value;
        tableRows.forEach(row => {
            const badge = row.querySelector(".status-badge");
            const status = badge ? badge.classList[1] : "";
            row.style.display = (selected === "all" || selected === status) ? "" : "none";
        });
    });
});

