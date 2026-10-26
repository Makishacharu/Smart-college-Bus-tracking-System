from modules.student import add_student, view_students
from modules.bus import add_bus,view_buses
from modules.attendance import attendance_menu



def main():
    while True:
        print("\n========================================")
        print("      COLLEGE BUS TRACKING SYSTEM")
        print("========================================")
        print("1. Student Management")
        print("2. Bus Management")
        print("3. Attendance")
        print("4. Bus Tracking")
        print("5. Notifications")
        print("6. Reports")
        print("7. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_menu()

        elif choice == "2":
            bus_menu()

        elif choice == "3":
            attendance_menu()

        elif choice == "4":
            print("\nBus Tracking - Coming Soon")

        elif choice == "5":
            print("\nNotifications - Coming Soon")

        elif choice == "6":
            print("\nReports - Coming Soon")

        elif choice == "7":
            print("\nThank you for using the system!")
            break

        else:
            print("\nInvalid choice! Please try again.")


def student_menu():
    
    while True:
        print("\n========== STUDENT MANAGEMENT ==========")
        print("1. Add Student")
        print("2. View Students")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            break

        else:
            print("Invalid choice!")
def bus_menu():
    while True:
        print("\n========== BUS MANAGEMENT ==========")
        print("1. Add Bus")
        print("2. View Buses")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_bus()

        elif choice == "2":
            view_buses()

        elif choice == "3":
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()