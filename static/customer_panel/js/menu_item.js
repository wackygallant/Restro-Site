document.addEventListener('DOMContentLoaded', function () {
    const minusBtn = document.getElementById('btn-minus');
    const plusBtn = document.getElementById('btn-plus');
    const qtyInput = document.getElementById('quantity-input');

    // Ensure initial value is valid
    if (!qtyInput.value || isNaN(qtyInput.value)) {
        qtyInput.value = 1;
    }

    minusBtn.addEventListener('click', () => {
        let currentValue = parseInt(qtyInput.value) || 1;
        if (currentValue > 1) {
            qtyInput.value = currentValue - 1;
        }
    });

    plusBtn.addEventListener('click', () => {
        let currentValue = parseInt(qtyInput.value) || 1;
        qtyInput.value = currentValue + 1;
    });

    // Remove readonly before form submission to ensure value is sent
    const form = qtyInput.closest('form');
    if (form) {
        form.addEventListener('submit', () => {
            qtyInput.removeAttribute('readonly');
        });
    }
});
