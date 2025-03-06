const expenseTableBody = document.getElementById('expense-table-body');
const addBtn = document.getElementById('add-btn');
const categorySelect = document.getElementById('category-select');
const amountInput = document.getElementById('amount-input');
const dateInput = document.getElementById('date-input');
const showAllBtn = document.getElementById('show-all-btn');

let expenses = [];

function renderExpenses() {
    expenseTableBody.innerHTML = '';  // Clear the table body before rendering

    expenses.forEach(expense => {
        const row = expenseTableBody.insertRow();

        const categoryCell = row.insertCell();
        const amountCell = row.insertCell();
        const dateCell = row.insertCell();
        const actionsCell = row.insertCell();

        categoryCell.textContent = expense.category;
        amountCell.textContent = expense.amount;
        dateCell.textContent = expense.date;

        // Create edit and delete buttons
        const editBtn = document.createElement('button');
        const deleteBtn = document.createElement('button');

        editBtn.textContent = 'Edit';
        deleteBtn.textContent = 'Delete';

        editBtn.classList.add('edit-btn');
        deleteBtn.classList.add('delete-btn');

        // Delete expense
        deleteBtn.addEventListener('click', function() {
            fetch(`http://localhost:5000/expenses/${expense.id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Expense deleted:', data);
                expenses = expenses.filter(exp => exp.id !== expense.id); // Remove from local state
                renderExpenses(); // Re-render the table
            })
            .catch(error => console.error('Error deleting expense:', error));
        });

        // Edit expense
        editBtn.addEventListener('click', function() {
            categorySelect.value = expense.category;
            amountInput.value = expense.amount;
            dateInput.value = expense.date;

            // Change the button to "Update"
            addBtn.textContent = 'Update';
            addBtn.onclick = function() {
                const newCategory = categorySelect.value;
                const newAmount = amountInput.value;
                const newDate = dateInput.value;

                if (newAmount <= 0 || isNaN(newAmount)) {
                    alert('Please enter a valid amount');
                    return;
                }

                fetch(`http://localhost:5000/expenses/${expense.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ category: newCategory, amount: newAmount, date: newDate })
                })
                .then(response => response.json())
                .then(updatedData => {
                    console.log('Expense updated:', updatedData);
                    // Update the expense in the local state
                    const index = expenses.findIndex(exp => exp.id === expense.id);
                    expenses[index] = updatedData; 
                    renderExpenses(); // Re-render the table
                    addBtn.textContent = 'Add'; // Change the button text back
                })
                .catch(error => console.error('Error updating expense:', error));
            };
        });

        actionsCell.appendChild(editBtn);
        actionsCell.appendChild(deleteBtn);
    });
}

// Fetch expenses from the backend when the page loads
window.onload = function() {
    // You can either load expenses directly here or wait for user interaction (Show All Expenses button)
};

// Add or update an expense
addBtn.addEventListener('click', function() {
    const category = categorySelect.value;
    const amount = Number(amountInput.value);
    const date = dateInput.value;

    if (!category || !amount || !date) {
        alert('Please fill in all fields');
        return;
    }

    const newExpense = { category, amount, date };

    if (addBtn.textContent === 'Add') {
        // Add new expense to backend
        fetch('http://localhost:5000/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newExpense)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Expense added:', data);
            expenses.push(data);  // Add the new expense to the local state
            renderExpenses(); // Re-render the table
        })
        .catch(error => console.error('Error adding expense:', error));
    } else {
        // Updating existing expense (handled in edit button)
        console.log('Updating expense is handled through the Edit button');
    }
});

// Show all expenses when the "Show All Expenses" button is clicked
showAllBtn.addEventListener('click', function() {
    fetch('http://localhost:5000/expenses')
        .then(response => response.json())
        .then(data => {
            expenses = data;  // Save expenses to local state
            renderExpenses(); // Render expenses to the table
        })
        .catch(error => console.error('Error fetching expenses:', error));
});
