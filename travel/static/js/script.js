document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar.fixed-top');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Handle the cancellation modal
    const cancelBookingModal = document.getElementById('cancelBookingModal');
    if (cancelBookingModal) {
        cancelBookingModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const bookingUrl = button.getAttribute('data-booking-url');
            const confirmBtn = cancelBookingModal.querySelector('#confirmCancelBtn');
            confirmBtn.setAttribute('href', bookingUrl);
        });
    }

    // Live total price calculation on booking page
    const seatsInput = document.querySelector('form input[name="number_of_seats"]');
    const pricePerSeatElement = document.getElementById('price-per-seat');
    const totalPriceElement = document.getElementById('total-price');

    if (seatsInput && pricePerSeatElement && totalPriceElement) {
        const pricePerSeat = parseFloat(pricePerSeatElement.getAttribute('data-price'));
        
        seatsInput.addEventListener('input', function() {
            const numberOfSeats = parseInt(this.value, 10) || 0;
            const total = (numberOfSeats * pricePerSeat).toFixed(2);
            totalPriceElement.textContent = '$' + total;
        });
        // Trigger on page load to set initial value if any
        seatsInput.dispatchEvent(new Event('input'));
    }
});
