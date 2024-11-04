const date = new Date()
document.getElementById('reservation_date').value = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate().toString().padStart(2, "0")}`

console.log(document.getElementById('reservation_date').value)
getBookings()


/*  Step 10: Part two */
document.getElementById('reservation_date').addEventListener("change", getBookings);


function getBookings() {
    let reserved_slots = []
    const date = document.getElementById('reservation_date').value
    document.getElementById('today').innerHTML = date //today is a span element that was initially empty

    fetch(bookingsUrl + '?date=' + date) //Passing date as a query string (.GET in bookings() view)
        .then(r => r.json())
        .then(data => {
            reserved_slots = []
            bookings = ''

            /* Step 11: Part three */
            for (item of data) {
                // console.log(item);
                console.log(item.fields);
                reserved_slots.push(item.fields.reservation_slot);
                bookings += `<p>${item.fields.name} - ${formatTime(
                    item.fields.reservation_slot
                )}</p>`;
            }

            /* Step 12: Part four  */
            slot_options = '<option value="0" disabled>Select time</option>';
            // console.log("Slots: ", reservation_slot);
            for (let i = 11; i < 20; i++) {
                const label = formatTime(i);
                if (reserved_slots.includes(i)) {
                    slot_options += `<option value=${i} disabled>${label}</option>`;
                } else {
                    slot_options += `<option value=${i}>${label}</option>`;
                }
            }


            document.getElementById('reservation_slot').innerHTML = slot_options
            if (bookings == '') {
                bookings = "No bookings"
            }
            document.getElementById('bookings').innerHTML = bookings
        })
}

function formatTime(time) {
    const ampm = time < 12 ? 'AM' : 'PM'
    const t = time < 12 ? time : time > 12 ? time - 12 : time
    const label = `${t} ${ampm}`
    return label
}


document.getElementById('button').addEventListener('click', function (e) {
    const formdata = {
        name: document.getElementById('name').value,
        reservation_date: document.getElementById('reservation_date').value,
        reservation_slot: document.getElementById('reservation_slot').value,
    }

    fetch(bookingsUrl, { method: 'post', body: JSON.stringify(formdata) }) //must convert to a JSON string
        .then(r => r.text())
        .then(data => {
            getBookings()
        })
})