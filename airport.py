import tkinter as tk
from csv import reader

# Global variables
uk_airport = None
overseas_airport = None
aircraft_type = None
first_class_seats = None
price_standard_seat = None
price_first_class_seat = None
airports_data = {}
aircraft_data = {
    "Medium narrow body": {
        "running_cost": 8,
        "max_range": 2650,
        "capacity": 180,
        "min_first_class_seats": 8
    },
    "Large narrow body": {
        "running_cost": 7,
        "max_range": 5600,
        "capacity": 220,
        "min_first_class_seats": 10
    },
    "Medium wide body": {
        "running_cost": 5,
        "max_range": 4050,
        "capacity": 406,
        "min_first_class_seats": 14
    }
}

# Read airport data from file
with open("airports.csv") as file:
    reader = reader(file)
    for row in reader:
        airports_data[row[1]] = {"distance_ljl": int(row[2]), "distance_boh": int(row[3])}



def enter_airport_details():
    """
    Function to handle user input for UK and overseas airport codes.
    """
    # Create labels and entry fields for UK airport code
    uk_airport_label = tk.Label(root, text="Enter UK Airport Code (LPL or BOH):")
    uk_airport_label.pack()
    uk_airport_entry = tk.Entry(root, width=3)
    uk_airport_entry.pack()

    # Create labels and entry fields for overseas airport code
    overseas_airport_label = tk.Label(root, text="Enter Overseas Airport Code:")
    overseas_airport_label.pack()
    overseas_airport_entry = tk.Entry(root, width=3)
    overseas_airport_entry.pack()

    # Define function to handle submit button click
    def submit_airport_details():
        global uk_airport, overseas_airport

        # Get entered airport codes
        entered_uk_airport = uk_airport_entry.get().upper()
        entered_overseas_airport = overseas_airport_entry.get().upper()

        # Validate UK airport code
        if entered_uk_airport not in {"LPL", "BOH"}:
            error_message = tk.Label(root, text="Invalid UK airport code. Please enter LPL or BOH.")
            error_message.pack()
            return

        # Validate overseas airport code
        if entered_overseas_airport not in airports_data:
            error_message = tk.Label(root, text="Invalid overseas airport code. Please check the list.")
            error_message.pack()
            return

        # Store valid airport codes
        uk_airport = entered_uk_airport
        overseas_airport = entered_overseas_airport

        # Clear entry fields and error messages (if any)
        uk_airport_entry.delete(0, tk.END)
        overseas_airport_entry.delete(0, tk.END)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and "Invalid" in widget.cget("text"):
                widget.destroy()

        # Show confirmation message
        success_message = tk.Label(root, text="Airport details entered successfully.")
        success_message.pack()

    # Create and configure submit button
    submit_button = tk.Button(root, text="Submit", command=submit_airport_details)
    submit_button.pack()


def enter_flight_details():
    """
    Function to handle user input for aircraft type and number of first-class seats.
    """

    # Create label and dropdown menu for aircraft type selection
    aircraft_type_label = tk.Label(root, text="Select Aircraft Type:")
    aircraft_type_label.pack()
    aircraft_type_choices = list(aircraft_data.keys())  # Replace with actual aircraft data key names
    aircraft_type_menu = tk.OptionMenu(root, variable=tk.StringVar(), *aircraft_type_choices)
    aircraft_type_menu.pack()

    # Create label and entry field for number of first-class seats
    first_class_seats_label = tk.Label(root, text="Enter Number of First-Class Seats:")
    first_class_seats_label.pack()
    first_class_seats_entry = tk.Entry(root, width=3)
    first_class_seats_entry.pack()

    # Define function to handle submit button click
    def submit_flight_details():
        global aircraft_type, first_class_seats

        # Get selected aircraft type
        selected_aircraft_type = aircraft_type_menu.winfo_variable().get()

        # Get entered number of first-class seats
        entered_first_class_seats = int(first_class_seats_entry.get())

        # Validate entered number of first-class seats
        min_seats = aircraft_data[selected_aircraft_type]["min_first_class_seats"]
        max_seats = aircraft_data[selected_aircraft_type]["capacity"] // 2
        if entered_first_class_seats < min_seats:
            error_message = tk.Label(root, text="Number of first-class seats must be at least {}.".format(min_seats))
            error_message.pack()
            return
        elif entered_first_class_seats > max_seats:
            error_message = tk.Label(root, text="Number of first-class seats cannot exceed {}.".format(max_seats))
            error_message.pack()
            return

        # Store valid values in global variables
        aircraft_type = selected_aircraft_type
        first_class_seats = entered_first_class_seats

        # Calculate and display aircraft data (running cost, maximum range, capacity)
        running_cost = aircraft_data[aircraft_type]["running_cost"]
        max_range = aircraft_data[aircraft_type]["max_range"]
        capacity = aircraft_data[aircraft_type]["capacity"]
        display_data = tk.Label(root, text="Running cost per seat: £{}\nMaximum flight range: {} km\nTotal capacity: {} seats".format(running_cost, max_range, capacity))
        display_data.pack()

        # Clear entry field and error messages (if any)
        first_class_seats_entry.delete(0, tk.END)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and ("Invalid" in widget.cget("text") or "Number of" in widget.cget("text")):
                widget.destroy()

        # Show confirmation message
        success_message = tk.Label(root, text="Flight details entered successfully.")
        success_message.pack()

    # Create and configure submit button
    submit_button = tk.Button(root, text="Submit", command=submit_flight_details)
    submit_button.pack()



def enter_price_plan_and_calculate():
    """
    Function to handle input for standard and first-class seat prices and calculate profit.
    """

    # Check if airport and aircraft details are entered
    if not uk_airport or not overseas_airport or not aircraft_type or not first_class_seats:
        error_message = tk.Label(root, text="Please enter all required details before calculating profit.")
        error_message.pack()
        return

    # Check if flight range is sufficient
    aircraft_range = aircraft_data[aircraft_type]["max_range"]
    distance = airports_data[overseas_airport]["distance_ljl"] if uk_airport == "LPL" else airports_data[overseas_airport]["distance_boh"]
    if distance > aircraft_range:
        error_message = tk.Label(root, text="Selected aircraft doesn't have enough range for this flight.")
        error_message.pack()
        return

    # Create labels and entry fields for standard and first-class seat prices
    standard_price_label = tk.Label(root, text="Enter Standard Seat Price (£):")
    standard_price_label.pack()
    standard_price_entry = tk.Entry(root, width=5)
    standard_price_entry.pack()
    first_class_price_label = tk.Label(root, text="Enter First-Class Seat Price (£):")
    first_class_price_label.pack()
    first_class_price_entry = tk.Entry(root, width=5)
    first_class_price_entry.pack()

    # Define function to handle submit button click
    def calculate_profit():
        global flight_profit

        # Get entered prices
        standard_price = float(standard_price_entry.get())
        first_class_price = float(first_class_price_entry.get())

        # Calculate standard and first-class seat counts
        total_seats = aircraft_data[aircraft_type]["capacity"]
        standard_seats = total_seats - first_class_seats * 2

        # Calculate flight cost per seat
        running_cost = aircraft_data[aircraft_type]["running_cost"]
        flight_cost_per_seat = running_cost * distance / 100

        # Calculate total flight cost and income
        flight_cost = flight_cost_per_seat * (standard_seats + first_class_seats)
        flight_income = standard_price * standard_seats + first_class_price * first_class_seats

        # Calculate and display flight profit
        flight_profit = flight_income - flight_cost
        profit_message = tk.Label(root, text="Flight Profit: £{}".format(round(flight_profit, 2)))
        profit_message.pack()

    # Create and configure submit button
    submit_button = tk.Button(root, text="Calculate Profit", command=calculate_profit)
    submit_button.pack()


def clear_data():
    """
    Function to clear all entered data and reset the GUI.
    """

    global uk_airport, overseas_airport, aircraft_type, first_class_seats, price_standard_seat, price_first_class_seat, flight_profit

    # Reset global variables
    uk_airport = None
    overseas_airport = None
    aircraft_type = None
    first_class_seats = None
    price_standard_seat = None
    price_first_class_seat = None
    flight_profit = None

    # Destroy all existing widgets in the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Display a confirmation message
    clear_message = tk.Label(root, text="All data cleared successfully.")
    clear_message.pack()


def quit_program():
    """
    Function to exit the flight planning application.
    """

    # Close the main window, ending the program
    root.destroy()



# Initialize main window and menu
root = tk.Tk()
root.title("Flight Planning")

menu = tk.Menu(root)
root.config(menu=menu)

# Create submenus for each option
airport_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Airports", menu=airport_menu)
airport_menu.add_command(label="Enter UK Airport", command=enter_airport_details)
airport_menu.add_command(label="Enter Overseas Airport", command=enter_airport_details)

flight_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Flight", menu=flight_menu)
flight_menu.add_command(label="Enter Aircraft Type", command=enter_flight_details)
flight_menu.add_command(label="Enter Number of First-Class Seats", command=enter_flight_details)

price_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Price Plan", menu=price_menu)
price_menu.add_command(label="Enter Prices and Calculate Profit", command=enter_price_plan_and_calculate)

menu.add_command(label="Clear Data", command=clear_data)
menu.add_command(label="Quit", command=quit_program)

# Start the main loop
root.mainloop()
