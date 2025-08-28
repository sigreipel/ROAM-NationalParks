document.addEventListener('DOMContentLoaded', function () {
    const removeButtons = document.querySelectorAll('.remove-button');

    removeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            console.log(`Removing item with ID: ${itemId}`);

            // Send a POST request to the server to delete the item
            fetch('/remove_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ item_id: itemId })
            })
                .then(response => {
                    if (response.ok) {
                        // Remove the item from the DOM
                        console.log(`Item with ID ${itemId} removed from server.`);
                        const itemElement = document.getElementById(`item-${itemId}`);
                        if (itemElement) {
                            itemElement.remove();
                        }
                    } else {
                        console.error('Failed to remove item');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});



