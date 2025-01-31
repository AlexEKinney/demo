def estimate_cost():
    totalArea = 0
    totalWallPaperRemoved = 0
    print("Welcome")
    customer_number = input("Enter the customer number: ")
    date_of_estimate = input("Enter the date of the estimate: ")
    number_of_rooms_that_require_painting = int(input("Enter the number of rooms that require painting: "))
    for i in range(number_of_rooms_that_require_painting):
        wallpaperremoved = input("Is wallpaper to be removed? (Y/N): ")
        if wallpaperremoved.lower() == "y":
            totalWallPaperRemoved += 1
        walls_in_the_room = int(input("Enter the number of walls in the room: "))
        for i in range(walls_in_the_room):
            wall_length = int(input("Enter the length of the wall: "))
            wall_height = int(input("Enter the height of the wall: "))
            totalArea += wall_length * wall_height
  

    what_kind_of_employee_should_be_assigned = input("What kind of employee should be assigned? (AP/FQ): ")
    while what_kind_of_employee_should_be_assigned.lower() != "ap" and what_kind_of_employee_should_be_assigned.lower() != "fq":
        print("Invalid qualification")
        what_kind_of_employee_should_be_assigned = input("What kind of employee should be assigned? (AP/FQ): ")
        return
    cost = totalArea * 15
    cost = cost + (totalWallPaperRemoved * 70)
    if(what_kind_of_employee_should_be_assigned.lower() == "ap"):
        cost = cost + 100
    else:
        cost = cost + 250
    cost = cost * 1.2
    print("The estimated cost is: ", cost)
    again = input("Would you like to enter another estimate? (Y/N): ")
    if again.lower() == "y":
        estimate_cost()
    else:
        exit()

def employee_details():
    print("Employee details")
    employee_name = input("Enter the name of the employee: ")
    employee_id = input("Enter the employee ID: ")
    employee_telephone = input("Enter the telephone number: ")

    qualification = input("Enter the qualification: ")
    while qualification.lower() != "ap" and qualification.lower() != "fq":
        print("Invalid qualification")
        qualification = input("Enter the qualification: ")
    print("Employee name: ", employee_name)
    print("Employee ID: ", employee_id)
    print("Employee telephone: ", employee_telephone)
    formatted_qualification = "Apprentice" if qualification.lower() == "ap" else "Fully Qualified"
    print("Employee qualification: ", formatted_qualification)
    correct= input("Is the information correct? (Y/N): ")
    if correct.lower() != "y":
        return
    else:
        estimate_cost()

while True:
    employee_details()
