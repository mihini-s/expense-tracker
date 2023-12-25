// income donut chart
google.charts.load("current", {
    packages: ["corechart"]
});
google.charts.setOnLoadCallback(drawIncomeDonutChart);

function drawIncomeDonutChart() {
    fetch('/income_chart')
        .then(response => response.json())
        .then(data => {
            var chartData = new google.visualization.DataTable();
            chartData.addColumn('string', 'Category');
            chartData.addColumn('number', 'Total');

            data.forEach(item => {
                chartData.addRow([item.category, item.total]);
            });

            var options = {
                title: 'Income',
                pieHole: 0.4,
                chartArea: {
                    left: 10,
                    top: 50,
                    width: '100%',
                    height: '100%',
                    bottom: 10
                },
                titleTextStyle: {
                    fontSize: 18,
                    bold: true,
                    color: '#333',
                    textAlign: 'center'
                },
                colors: [

                    "#34495e",
                    "#e74c3c",
                    "#282c35",
                    "#bdc3c7",
                    "#3498db",
                    "#2ecc71",
                    "#3498db",
                    "#e67e22",
                    "#e74c3c"
                ],
            };

            var chart = new google.visualization.PieChart(document.getElementById('income_donutchart'));
            chart.draw(chartData, options);
        });
}


// income donut chart
google.charts.load("current", {
    packages: ["corechart"]
});
google.charts.setOnLoadCallback(drawExpensesDonutChart);

function drawExpensesDonutChart() {
    fetch('/expenses_chart')
        .then(response => response.json())
        .then(data => {
            var chartData = new google.visualization.DataTable();
            chartData.addColumn('string', 'Category');
            chartData.addColumn('number', 'Total');

            data.forEach(item => {
                chartData.addRow([item.category, item.total]);
            });

            var options = {
                title: 'Expenses',
                pieHole: 0.4,
                chartArea: {
                    left: 10,
                    top: 50,
                    width: '100%',
                    height: '100%',
                    bottom: 10
                },
                titleTextStyle: {
                    fontSize: 18,
                    bold: true,
                    color: '#333',
                    textAlign: 'center'
                },
                colors: ["#e74c3c", "#f39c12", "#9b59b6", "#34495e", "#2c3e50", "#27ae60", "#c0392b", "#7f8c8d"],
            };

            var chart = new google.visualization.PieChart(document.getElementById('expenses_donutchart'));
            chart.draw(chartData, options); // Use chartData instead of data
        });
}



// line chart
google.charts.load('current', {
    'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawLineChart);

function drawLineChart() {
    fetch('/line_chart_data')
        .then(response => response.json())
        .then(data => {
            var chartData = new google.visualization.arrayToDataTable(data);

            var options = {
                curveType: 'function',
                legend: {
                    position: 'bottom'
                },
                chartArea: {
                    left: 30,
                    top: 20,
                    width: '100%',
                    height: '70%',
                    bottom: 50
                },
                vAxis: {
                    viewWindow: {
                        min: 0
                    }
                },
                title: 'Expenses vs Income',
                titleTextStyle: {
                    fontSize: 15
                },
            };

            var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

            chart.draw(chartData, options);
        })
        .catch(error => {
            console.error('Error fetching line chart data:', error);
        });
}




// income bar chart
google.charts.load('current', {
    packages: ['corechart', 'bar']
});
google.charts.setOnLoadCallback(drawIncomeBarChart);

function drawIncomeBarChart() {
    fetch('/income_chart')
        .then(response => response.json())
        .then(data => {
            // Handle the received data and draw the chart
            var chartData = new google.visualization.DataTable();
            chartData.addColumn('string', 'Category');
            chartData.addColumn('number', 'Total');

            // Assuming data is a list of dictionaries with 'total' and 'category' properties
            data.forEach(item => {
                chartData.addRow([item.category, item.total]);
            });

            var options = {
                title: 'Income Breakdown',
                titleTextStyle: {
                    fontSize: 15
                },
                hAxis: {
                    title: 'Category',
                    format: 'h:mm a',
                    viewWindow: {
                        min: [7, 30, 0],
                        max: [17, 30, 0]
                    }
                },
                vAxis: {
                    title: 'Amount'
                },
                legend: {
                    position: 'none'
                },
                colors: ['#E64A19'],
                chartArea: {
                    width: '80%',
                    height: '80%'
                },
            };

            var chart = new google.visualization.ColumnChart(
                document.getElementById('income_column_chart'));

            chart.draw(chartData, options);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// expenses bar chart
google.charts.load('current', {
    packages: ['corechart', 'bar']
});
google.charts.setOnLoadCallback(drawExpensesBarchart);

function drawExpensesBarchart() {
    fetch('/expenses_chart')
        .then(response => response.json())
        .then(data => {
            // Handle the received data and draw the chart
            var chartData = new google.visualization.DataTable();
            chartData.addColumn('string', 'Category');
            chartData.addColumn('number', 'Total');

            // Assuming data is a list of dictionaries with 'total' and 'category' properties
            data.forEach(item => {
                chartData.addRow([item.category, item.total]);
            });

            var options = {
                title: 'Expenses Breakdown',
                titleTextStyle: {
                    fontSize: 15
                },
                hAxis: {
                    title: 'Category',
                    format: 'h:mm a',
                    viewWindow: {
                        min: [7, 30, 0],
                        max: [17, 30, 0]
                    }
                },
                vAxis: {
                    title: 'Amount'
                },
                legend: {
                    position: 'none'
                },
                colors: ['#2D033B'],
                chartArea: {
                    width: '80%',
                    height: '80%'
                },
            };

            var chart = new google.visualization.ColumnChart(
                document.getElementById('expenses_column_chart'));

            chart.draw(chartData, options);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



// Filter income/expenses table

$(document).ready(function() {
    $("#tableSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


// modal for changing password
function changePassword() {
    const new_password = document.getElementById('new_password').value;

    // Check if the trimmed new password is not empty
    if (new_password.trim() !== '') {
        // Send an AJAX request to the Flask route to handle the password change
        fetch('/change_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    new_password
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Check the response status
                if (data.status === 'success') {
                    // If the password change was successful, close the modal
                    $('#change_password').modal('hide');
                    // Optionally, display a success message to the user
                    console.log('Password changed successfully');
                } else {
                    // If the password change was not successful, display an error message
                    console.error('Password change failed:', data.message);
                    // Optionally, display an error message to the user
                }
            })
            .catch(error => {
                // Handle network errors or other issues
                console.error('Error:', error);
                // Optionally, display an error message to the user
            });
    } else {
        // Optionally, display an error message to the user for an empty password
        console.error('New password is empty. Please enter a valid password.');
    }
}

// modal for deleting account
function deleteAccount() {
    // Send an AJAX request to the Flask route to handle deleting the account
    fetch('/delete_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                delete_account
            }),
        })
        .then(response => {
            // Check if the response status is OK (200)
            if (!response.ok) {
                throw new Error('Failed to delete account');
            }
            return response.json();
        })
        .then(data => {
            // Check if the deletion was successful
            if (data.status === 'success') {
                // Redirect to the login page
                window.location.href = '/login';
            } else {
                // Optionally, display an error message to the user
                console.error('Account deletion failed:', data.message);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
}


// modal for changing the currency
function changeCurrency() {
    var dropdown = document.getElementById("currency");
    var selectedCurrency = dropdown.options[dropdown.selectedIndex].value;

    // Update the displayed currency in the <h6> element
    document.getElementById("displayCurrency").innerHTML = "<b>Currency:</b> " + selectedCurrency;

    if (selectedCurrency !== null) {
        fetch('/change_currency', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    currency: selectedCurrency
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Currency changed successfully');
                    $('#change_currency').modal('hide');
                } else {
                    console.error('Currency change failed:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        console.error('Selected currency is null or undefined');
    }
}


// modal for changing the budget
function budget() {
    const budget = document.getElementById('addbudget').value;

    // Update the displayed budget
    document.getElementById("displayBudget").innerHTML = budget;

    // Check if budget is not empty
    if (budget !== null) {
        // Send an AJAX request to the Flask route to handle the budget change
        fetch('/budget', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    budget
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Check the response status
                if (data.status === 'success') {
                    // If the budget change was successful, close the modal
                    $('#budget').modal('hide');
                    // Optionally, display a success message to the user
                    console.log('Budget changed successfully');
                    // Reload the page
                    window.location.reload();
                } else {
                    // If the budget change was not successful, display an error message
                    console.error('Budget change failed:', data.message);
                    // Optionally, display an error message to the user
                }
            })
            .catch(error => {
                // Handle network errors or other issues
                console.error('Error:', error);
                // Optionally, display an error message to the user
            });
    } else {
        // Optionally, display an error message to the user for an empty password
        console.error('Budget is empty. Please enter a valid budget.');
    }
}


// modal for changing the income goal
function goal() {
    const goal = document.getElementById('addgoal').value;

    // Update the displayed budget
    document.getElementById("displayGoal").innerHTML = goal;

    // Check if budget is not empty
    if (goal !== null) {
        // Send an AJAX request to the Flask route to handle the income goal change
        fetch('/goal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    goal
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Check the response status
                if (data.status === 'success') {
                    // If the budget change was successful, close the modal
                    $('#goal').modal('hide');
                    // Optionally, display a success message to the user
                    console.log('Goal changed successfully');
                    // Reload the page
                    window.location.reload();
                } else {
                    // If the budget change was not successful, display an error message
                    console.error('Goal change failed:', data.message);
                    // Optionally, display an error message to the user
                }
            })
            .catch(error => {
                // Handle network errors or other issues
                console.error('Error:', error);
                // Optionally, display an error message to the user
            });
    } else {
        // Optionally, display an error message to the user for an empty password
        console.error('Income goal is empty. Please enter a valid goal.');
    }
}


// modal for adding new income category
function addIncomeCategory() {
    const incomeCategory = document.getElementById('newincomecategory').value.trim();
    const dropdown = document.getElementById('input_category');

    // Check if the income category is not empty
    if (incomeCategory !== "") {

        // Create a new temp <option> element
        let newOption = new Option(incomeCategory, incomeCategory);
        dropdown.add(newOption, undefined);

        // add the new option to categories db
        // Send an AJAX request to the Flask route to handle the addition
        fetch('/incomecategory', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    incomeCategory
                }),
            })

            .then(response => response.json())
            .then(data => {
                // Check the response status
                if (data.status === 'success') {
                    // If the addition was successful, close the modal
                    $('#addincomecategory').modal('hide');
                    // Optionally, display a success message to the user
                    console.log('New income category added successfully');
                } else {
                    // If the addition was not successful, display an error message
                    console.error('Income category addition failed:', data.message);
                    // Optionally, display an error message to the user
                }
            })
    }
}


// modal for adding new expense category
function addExpenseCategory() {
    const expenseCategory = document.getElementById('newexpensecategory').value.trim();
    const dropdown = document.getElementById('input_category');

    // Check if the expense category is not empty
    if (expenseCategory !== "") {

        // Create a new temp <option> element
        let newOption = new Option(expenseCategory, expenseCategory);
        dropdown.add(newOption, undefined);

        // add the new option to categories db
        // Send an AJAX request to the Flask route to handle the addition
        fetch('/expensecategory', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    expenseCategory
                }),
            })

            .then(response => response.json())
            .then(data => {
                // Check the response status
                if (data.status === 'success') {
                    // If the addition was successful, close the modal
                    $('#addexpensecategory').modal('hide');
                    // Optionally, display a success message to the user
                    console.log('New expense category added successfully');
                } else {
                    // If the addition was not successful, display an error message
                    console.error('Expense category addition failed:', data.message);
                    // Optionally, display an error message to the user
                }
            })
    }
}


// modal for deleting log in income table
function delete_income_log(event) {
    const button = event.currentTarget;
    const id_value = button.getAttribute('income_id');

    // Send an AJAX request to the Flask route to handle deleting the log
    fetch('/delete_income_log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_value
            }),
        })
        .then(response => {
            // Check if the response status is OK (200)
            if (!response.ok) {
                throw new Error('Failed to delete log');
            }
            return response.json();
        })
        .then(data => {
            // Check if the deletion was successful
            if (data.status === 'success') {
                // hide the modal
                $('#trash').modal('hide');
                // Redirect to the income page
                window.location.href = '/income';
            } else {
                // Optionally, display an error message to the user
                console.error('Deletion failed:', data.message);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
}


// modal for deleting log in expense table
function delete_expense_log(event) {
    const button = event.currentTarget;
    const id_value = button.getAttribute('expense_id');
    // Send an AJAX request to the Flask route to handle deleting the log
    fetch('/delete_expense_log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_value
            }),
        })
        .then(response => {
            // Check if the response status is OK (200)
            if (!response.ok) {
                throw new Error('Failed to delete log');
            }
            return response.json();
        })
        .then(data => {
            // Check if the deletion was successful
            if (data.status === 'success') {
                // hide the modal
                $('#trash').modal('hide');
                // Redirect to the income page
                window.location.href = '/expenses';
            } else {
                // Optionally, display an error message to the user
                console.error('Deletion failed:', data.message);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
}



// displaying file
function openFile() {
    const button = event.currentTarget;
    const name = button.getAttribute('file_name');
    console.error('name:', name)
    if (name === 'None') {
        window.alert('No file');
    } else {
        fetch(`/file_uploads/${name}`, {
                method: 'GET',
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to open file');
                }
                return response.blob(); // Use blob() to handle binary data
            })
            .then(blobData => {
                // Create a blob URL and open it in a new window or tab
                const blobUrl = URL.createObjectURL(blobData);
                window.open(blobUrl, '_blank');
            })
            .catch(error => {
                console.error('Error opening file:', error);
                window.alert('Error opening file: ' + error.message);
            });
    }
}


// filter to-do list

$(document).ready(function() {
    $("#debtSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#debtTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


// delete debt note
function delete_note(event) {
    const button = event.currentTarget;
    const id_value = button.getAttribute('debt_id');
    // Send an AJAX request to the Flask route to handle deleting the log
    fetch('/delete_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_value
            }),
        })
        .then(response => {
            // Check if the response status is OK (200)
            if (!response.ok) {
                throw new Error('Failed to delete log');
            }
            return response.json();
        })
        .then(data => {
            // Check if the deletion was successful
            if (data.status === 'success') {
                // hide the modal
                $('#trash').modal('hide');
                // Redirect to the income page
                window.location.href = '/debt_tracker';
            } else {
                // Optionally, display an error message to the user
                console.error('Deletion failed:', data.message);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
}


// completed note
function checked(event) {
    const button = event.currentTarget;
    const id_value = button.getAttribute('debt_id');
    // Send an AJAX request to the Flask route to handle deleting the log
    fetch('/checked', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_value
            }),
        })
        .then(response => {
            // Check if the response status is OK (200)
            if (!response.ok) {
                throw new Error('Failed to check note');
            }
            return response.json();
        })
        .then(data => {
            // Check if the deletion was successful
            if (data.status === 'success') {
                // Redirect to the income page
                window.location.href = '/debt_tracker';
                window.alert('Yay! You paid your debt.');
            } else {
                // Optionally, display an error message to the user
                console.error('Failed:', data.message);
            }
        })
        .catch(error => {
            // Handle network errors or other issues
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
}
