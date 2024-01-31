"""
    THIS IS AS ALWAYS WELL COMMENTED CODE
    tkinter docs used online via python.org --> https://docs.python.org/3/library/tkinter.html
    this *should* work on windows, I haven't tested it on windows, but it should work
"""
import tkinter as tk
import time
from tkinter import PhotoImage
uk_airport = ""
overseas_airport = ""
aircraft_type = ""
first_class_seats = 0
price_standard_seat = 0
price_first_class_seat = 0
airports_data = {
    "JFK": {
        "distance_ljl": 5326,
        "distance_boh": 5485
    },
    "ORY": {
        "distance_ljl": 629,
        "distance_boh": 379
    },
    "MAD": {
        "distance_ljl": 1428,
        "distance_boh": 1151
    },
    "AMS": {
        "distance_ljl": 526,
        "distance_boh": 489
    },
    "CAI": {
        "distance_ljl": 3779,
        "distance_boh": 3584
    }
}
aircraft_data = {
    "MNB": {
        "running_cost": 8,
        "max_range": 2650,
        "capacity": 180,
        "min_first_class_seats": 8
    },
    "LNB": {
        "running_cost": 7,
        "max_range": 5600,
        "capacity": 220,
        "min_first_class_seats": 10
    },
    "MWB": {
        "running_cost": 5,
        "max_range": 4050,
        "capacity": 406,
        "min_first_class_seats": 14
    }
}


def enter_airport_details():
    resetScreen()
    uk_airport_label = tk.Label(root, text="Enter UK Airport Code:")
    uk_airport_label.pack()
    uk_airport_entry = tk.Entry(root, width=4)
    uk_airport_entry.pack()
    overseas_airport_label = tk.Label(root, text="Enter Overseas Airport Code:")
    overseas_airport_label.pack()
    overseas_airport_entry = tk.Entry(root, width=4)
    overseas_airport_entry.pack()
    def submit_airport_details():
        global uk_airport, overseas_airport
        entered_uk_airport = uk_airport_entry.get().upper()
        entered_overseas_airport = overseas_airport_entry.get().upper()
        if entered_uk_airport not in {"LPL", "BOH"}:
            error_message = tk.Label(root, text="Invalid UK airport code.")
            error_message.pack()
            return
        if entered_overseas_airport not in airports_data:
            error_message = tk.Label(root, text="Invalid overseas airport code.")
            error_message.pack()
            return
        uk_airport = entered_uk_airport
        overseas_airport = entered_overseas_airport
        uk_airport_entry.delete(0, tk.END)
        overseas_airport_entry.delete(0, tk.END)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and "Invalid" in widget.cget("text"):
                widget.destroy()
        success_message = tk.Label(root, text="Airport details entered successfully.")
        success_message.pack()
    submit_button = tk.Button(root, text="Submit", command=submit_airport_details)
    submit_button.pack()

"""
ALEXANDER KINNEY
"""
def enter_flight_details():
    resetScreen()
    if not uk_airport or not overseas_airport:
        error_message = tk.Label(root, text="fill in flight details first")
        error_message.pack()
        return
    aircraft_type_menulabel = tk.Label(root, text="Enter AIRCRAFT TYPE (MNB, LNB or MWB):")
    aircraft_type_menulabel.pack()
    aircraft_type_menu = tk.Entry(root, width=4)
    aircraft_type_menu.pack()
    first_class_seats_entrylabel = tk.Label(root, text="Number of first class seats (must be over min. amt):")
    first_class_seats_entrylabel.pack()
    first_class_seats_entry = tk.Entry(root, width=4)
    first_class_seats_entry.pack()
    def submit_flight_details():
        global aircraft_type, first_class_seats

        selected_aircraft_type = aircraft_type_menu.get().upper()

        entered_first_class_seats = int(first_class_seats_entry.get())

        min_seats = aircraft_data[selected_aircraft_type]["min_first_class_seats"]
        max_seats = aircraft_data[selected_aircraft_type]["capacity"] // 2 ## javascript 
        if entered_first_class_seats < min_seats:
            error_message = tk.Label(root, text="Number of first-class seats must be at least {}.".format(min_seats))
            error_message.pack()
            return
        elif entered_first_class_seats > max_seats:
            error_messagee = tk.Label(root, text="Number of first-class seats cannot exceed {}.".format(max_seats))
            error_messagee.pack()
            return

        aircraft_type = selected_aircraft_type
        first_class_seats = entered_first_class_seats

        running_cost = aircraft_data[aircraft_type]["running_cost"]
        max_range = aircraft_data[aircraft_type]["max_range"]
        capacity = aircraft_data[aircraft_type]["capacity"]
        display_data = tk.Label(root, text="Running cost per seat: £{}\nMaximum flight range: {} km\nTotal capacity: {} seats".format(running_cost, max_range, capacity))
        display_data.pack()
        first_class_seats_entry.delete(0, tk.END)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and ("Invalid" in widget.cget("text") or "Number of" in widget.cget("text")):
                widget.destroy()
        success_message = tk.Label(root, text="done")
        success_message.pack()
        time.sleep(2)
    submit_button = tk.Button(root, text="save", command=submit_flight_details)
    submit_button.pack()



def enter_price_plan_and_calculate():
    resetScreen()
    if not uk_airport or not overseas_airport or not aircraft_type or not first_class_seats:
        error_message = tk.Label(root, text="use other menus first. this is the last one")
        error_message.pack()
        return
    aircraft_range = aircraft_data[aircraft_type]["max_range"]
    distance = airports_data[overseas_airport]["distance_ljl"] if uk_airport == "LPL" else airports_data[overseas_airport]["distance_boh"]
    if distance > aircraft_range:
        error_message = tk.Label(root, text="range too small for this aircraft! range: " + str(aircraft_range) + "distance: "+  str(distance))
        error_message.pack()
        return

    standard_price_label = tk.Label(root, text="standard price")
    standard_price_label.pack()
    standard_price_entry = tk.Entry(root, width=5)
    standard_price_entry.pack()
    first_class_price_label = tk.Label(root, text="rich people price")
    first_class_price_label.pack()
    first_class_price_entry = tk.Entry(root, width=5)
    first_class_price_entry.pack()
    def calculate_profit():
        global flight_profit
        standard_price = float(standard_price_entry.get())
        first_class_price = float(first_class_price_entry.get())
        total_seats = aircraft_data[aircraft_type]["capacity"]
        standard_seats = total_seats - first_class_seats * 2
        running_cost = aircraft_data[aircraft_type]["running_cost"]
        flight_cost_per_seat = running_cost * distance / 100
        flight_cost = flight_cost_per_seat * (standard_seats + first_class_seats)
        flight_income = standard_price * standard_seats + first_class_price * first_class_seats
        flight_profit = flight_income - flight_cost
        profit_message = tk.Label(root, text="profit{}".format(round(flight_profit, 2)))
        profit_message.pack()

    submit_button = tk.Button(root, text="Calculate", command=calculate_profit)
    submit_button.pack()

def resetScreen():
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Flight Planning")

    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Enter Airport Details", command=enter_airport_details)
    iconn = PhotoImage(file = 'icon.png') 
    root.iconphoto(False, iconn) 

    menu.add_command(label="Enter Aircraft Details", command=enter_flight_details)
    menu.add_command(label="Enter Prices and Calculate Profit", command=enter_price_plan_and_calculate)
    data_menu = tk.Menu(menu, tearoff=False)
    data_menu.add_command(label="Clear Data", command=clear_data)
    data_menu.add_command(label="Clear Screen", command=resetScreen)
    data_menu.add_command(label="List ALL STORED DATA DEBUG", command=list_all_data)
    menu.add_cascade(label="Data", menu=data_menu)
    menu.add_command(label="Quit", command=quit_program)
def list_all_data():
    global uk_airport, overseas_airport, aircraft_type, first_class_seats, price_standard_seat, price_first_class_seat, flight_profit
    resetScreen()
    uk_airport_label = tk.Label(root, text="UK Airport Code (LPL or BOH):" + str(uk_airport))
    uk_airport_label.pack()
    overseas_airport_label = tk.Label(root, text="Overseas Airport Code:" + str(overseas_airport))
    overseas_airport_label.pack()
    aircraft_type_label = tk.Label(root, text="Aircraft Type:" + str(aircraft_type))
    aircraft_type_label.pack()
    first_class_seats_label = tk.Label(root, text="Number of First-Class Seats:" + str(first_class_seats))
    first_class_seats_label.pack()
    standard_price_label = tk.Label(root, text="Standard Seat Price (£):" + str(price_standard_seat))
    standard_price_label.pack()
    first_class_price_label = tk.Label(root, text="First-Class Seat Price (£):" + str(price_first_class_seat))
    first_class_price_label.pack()
    profit_message = tk.Label(root, text="Flight Profit: £{}".format(round(flight_profit, 2)))
    profit_message.pack()

def clear_data():

    global uk_airport, overseas_airport, aircraft_type, first_class_seats, price_standard_seat, price_first_class_seat, flight_profit
    uk_airport = ""
    overseas_airport = ""
    aircraft_type = ""
    first_class_seats = 0
    price_standard_seat = 0
    price_first_class_seat = 0
    flight_profit = 0
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Flight Planning")
    menu = tk.Menu(root)
    root.config(menu=menu)
    iconn = PhotoImage(file = 'icon.png') 
    root.iconphoto(False, iconn) 
    menu.add_command(label="Enter Airport Details", command=enter_airport_details)
    menu.add_command(label="Enter Aircraft Details", command=enter_flight_details)
    menu.add_command(label="Enter Prices and Calculate Profit", command=enter_price_plan_and_calculate)
    data_menu = tk.Menu(menu, tearoff=False)
    data_menu.add_command(label="Clear Data", command=clear_data)
    data_menu.add_command(label="Clear Screen", command=resetScreen)
    data_menu.add_command(label="List ALL STORED DATA DEBUG", command=list_all_data)
    menu.add_cascade(label="Data", menu=data_menu)
    menu.add_command(label="Quit", command=quit_program)
    clear_message = tk.Label(root, text="All data cleared successfully.")
    clear_message.pack()


def quit_program():
    root.destroy()



root = tk.Tk()
root.title("Flight Planning")

menu = tk.Menu(root)
root.config(menu=menu)

resetScreen() 
root.mainloop() ## hacking the mainloop
"""
ALEXANDER KINNEY
"""