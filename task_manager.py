"""
Notes:
1. Use the following username and password to access the admin rights
username: admin
password: password
2. Ensure you open the whole folder for this task in VS Code otherwise the
program will look in your root directory for the text files.
"""

# =====importing libraries===========

import os
from datetime import datetime, date
import sys

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def read_file(filename):
    """Read provided file and returns the content of file"""
    filepath = os.getcwd() + f"/{filename}"

    try:
        if not os.path.exists(filepath):
            with open(filepath, "w") as file:
                if filename == "user.txt":
                    file.write("admin;password")
                else:
                    pass
        with open(filepath, "r") as file:
            file_data = file.read().split("\n")
            file_data = [t for t in file_data if t != ""]
            return file_data

    except Exception as e:
        raise e


def write_into_file(filename, data="", mode="a"):
    """Writes data to specified file with optional mode"""
    filepath = os.getcwd() + f"/{filename}"
    with open(filepath, mode) as file:
        file.write("\n" + data)


def update_task(task, index, value):
    """Overwrite file with updated task"""
    file_data = read_file("tasks.txt")
    task_name = task[1]
    task_description = task[2]
    updated_file_data = []

    for each_record in file_data:

        if task_name in each_record and task_description in each_record:
            if index == 1:
                task[0] = value
                updated_record = ";".join(task)
                updated_file_data.append(updated_record)
            elif index == 2:
                task[-2] = value
                updated_record = ";".join(task)
                updated_file_data.append(updated_record)
            elif index == 3:
                task[-1] = value.capitalize()
                updated_record = ";".join(task)
                updated_file_data.append(updated_record)
        else:
            updated_file_data.append(each_record)

    str_updated_data = "\n".join(updated_file_data)
    write_into_file("tasks.txt", str_updated_data, "w")


def login(curr_user, curr_pass):
    """Verify user login credentials"""
    username_password = {}
    user_data = read_file("user.txt")

    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    if curr_user not in username_password.keys():
        print("\nUser does not exist\n")
    elif username_password[curr_user] != curr_pass:
        print("\nWrong password\n")
    else:
        # print("\nLogin Successful!")
        return True


def is_user_exists(username):
    """Check whether user exists or not"""
    username = username.lower()
    usernames = []
    user_data = read_file("user.txt")
    for record in user_data:
        uname, pwd = record.split(";")
        usernames.append(uname)
    if username in usernames:
        return True


def register_user(username, password):
    """Create new user and add record into user.txt file"""
    user_record = f"{username.lower()};{password}"
    write_into_file("user.txt", user_record)
    print("\nUser added\n")


def add_task(user, task_title, description, curr_date, due_date):
    """Add new task to tasks.txt file"""
    if is_user_exists(user):
        task = f"{user};{task_title};{description};{curr_date};{due_date};No"
        write_into_file("tasks.txt", task)
        print("\nTask has been added\n")
    else:
        print("\nUser does not exist. Please enter a valid username\n")


def view_all_tasks():
    """Read tasks.txt file and prints all tasks"""
    all_tasks_list = read_file("tasks.txt")

    for task in all_tasks_list:

        task_details = task.split(";")
        display_task = f"Assigned To: \t\t{task_details[0]}\n"
        display_task += f"Task Name: \t\t{task_details[1]}\n"
        display_task += f"Task Description: \t{task_details[2]}\n"
        display_task += f"Date Assigned: \t\t{task_details[3]}\n"
        display_task += f"Due Date: \t\t{task_details[4]}\n"
        display_task += f"Completed: \t\t{task_details[5]}\n"
        print(display_task)


def view_my_tasks(curr_user):
    """Prints tasks assigned to user and returns total number of tasks"""
    all_tasks_list = read_file("tasks.txt")
    print("\nPlease find your assigned task details below:\n")
    i = 1
    for task in all_tasks_list:
        task_details = task.split(";")
        if curr_user == task_details[0]:
            display_task = f"{i}. Task Name: {task_details[1]}"
            print(display_task)
            i += 1
    return i


def get_task_details(curr_user, task_number):
    """Returns specified task details of user"""
    user_tasks = []
    all_tasks_list = read_file("tasks.txt")
    print("\nPlease find task details below:\n")

    for task in all_tasks_list:
        task_details = task.split(";")
        if curr_user == task_details[0]:
            user_tasks.append(task_details)

    display_task = f"Assigned To: \t\t{user_tasks[task_number][0]}\n"
    display_task += f"Task Name: \t\t{user_tasks[task_number][1]}\n"
    display_task += f"Task Description: \t{user_tasks[task_number][2]}\n"
    display_task += f"Date Assigned: \t\t{user_tasks[task_number][3]}\n"
    display_task += f"Due Date: \t\t{user_tasks[task_number][4]}\n"
    display_task += f"Completed: \t\t{user_tasks[task_number][5]}\n"
    print(display_task)

    return user_tasks[task_number]


def generate_reports():
    """Generate user.txt and task_overview.txt"""
    tasks = read_file("tasks.txt")
    total_tasks = len(tasks)
    total_completed_tasks = 0
    total_incompleted_tasks = 0
    total_overdue_tasks = 0
    perc_of_incomplete_tasks = 0
    perc_of_overdue_tasks = 0
    current_date = date.today()

    if not total_tasks == 0:
        for task in tasks:
            splitted_task = task.split(";")
            if splitted_task[-1].lower() == "yes":
                total_completed_tasks += 1
            elif splitted_task[-1].lower() == "no":
                total_incompleted_tasks += 1
            due_date = datetime.strptime(splitted_task[4],
                                         DATETIME_STRING_FORMAT).date()
            if due_date < current_date:
                total_overdue_tasks += 1
    try:
        perc_of_incomplete_tasks = round((total_incompleted_tasks /
                                          total_tasks) * 100, 2)
        perc_of_overdue_tasks = round((total_overdue_tasks / total_tasks)
                                      * 100, 2)
    except Exception as e:
        print(e)

    display_task = f"""\t\t\t*** Task Overview ***
----------------------------------------------------------------
Total Tasks:                    {total_tasks}
Total Completed Tasks:          {total_completed_tasks}
Total Incompleted Tasks:        {total_incompleted_tasks}
Total Overdue Tasks:            {total_overdue_tasks}
Percentage of Incomplete Tasks: {perc_of_incomplete_tasks}
Percentage of Overdue Tasks:    {perc_of_overdue_tasks}
    """

    write_into_file("task_overview.txt", data=display_task, mode="w")

    users_data = read_file("user.txt")
    username_list = [ind.split(";")[0] for ind in users_data]
    total_users = len(username_list)
    info = []
    unassigned_usernames = []

    for name in username_list:
        user_info = {}

        for task in tasks:
            splitted_task = task.split(";")

            if name == splitted_task[0]:
                user_info["username"] = name
                completed = 1 if splitted_task[-1].lower() == "yes" else 0
                due_date = datetime.strptime(splitted_task[4],
                                             DATETIME_STRING_FORMAT).date()
                if name in user_info.keys():
                    user_info[name] += 1
                else:
                    user_info[name] = 1

                if "completed" in user_info.keys():
                    user_info["completed"] += completed
                else:
                    user_info["completed"] = completed

                overdue = 0

                if splitted_task[-1].lower() == "no":
                    if due_date < current_date:
                        overdue = 1

                if "overdue" in user_info.keys():
                    user_info["overdue"] += overdue
                else:
                    user_info["overdue"] = overdue

        total_user_tasks = user_info.get(name)

        if total_user_tasks is None:
            unassigned_usernames.append(name)

        if total_user_tasks is not None:
            percent = (total_user_tasks / total_tasks) * 100
            user_info["perc_assigned"] = percent
            percent_completed = round((user_info["completed"] /
                                       total_user_tasks) * 100, 2)
            user_info["percent_completed"] = percent_completed

            remaining = round(((total_user_tasks - user_info.get("completed"))
                               / total_user_tasks) * 100, 2)
            user_info["remaining_percent"] = remaining

            overdue_perc = round((user_info["overdue"] / total_user_tasks) *
                                 100, 2)
            user_info["overdue_percent"] = overdue_perc

        if bool(user_info):
            info.append(user_info)

    display_task = f"""\t\t\t*** User Overview ***
----------------------------------------------------------------
Total Users: {total_users}
Total Tasks: {total_tasks}
----------------------------------------------------------------
UserName    Task_Assigned   Completed(%)    Remaining(%)    Overdue(%)"""
    write_into_file("user_overview.txt", data=display_task, mode="w")

    for usr_data in info:
        user_string = (f"{usr_data["username"]} \t\t\t"
                       f"{usr_data[usr_data["username"]]} \t\t\t\t"
                       f"{usr_data["percent_completed"]} \t\t\t"
                       f"{usr_data["remaining_percent"]} \t\t\t"
                       f"{usr_data["overdue_percent"]}")
        write_into_file("user_overview.txt", data=user_string, mode="a")

    for name in unassigned_usernames:
        user_string = (f"{name} \t\t\t"
                       "0 \t\t\t\t"
                       "0 \t\t\t\t"
                       "0 \t\t\t\t"
                       "0")
        write_into_file("user_overview.txt", data=user_string, mode="a")
    return "\nReports has been generated.\n"


while True:
    login_register = input("Select option from below: \n L - Login\n " +
                           "R - Register\n : ").lower()
    if login_register == "l":
        current_user = input("Username: ")
        current_password = input("Password: ")
        while not login(current_user, current_password):
            user_choice = input("Enter -1 to exit or enter " +
                                "anything to try again ")
            if user_choice == "-1":
                sys.exit(0)
            else:
                current_user = input("Username: ")
                current_password = input("Password: ")
        break
    elif login_register == "r":
        new_user = input("Username: ")
        if is_user_exists(new_user):
            print("User already exists, please login instead")
            continue
        while True:
            new_password = input("Password: ")
            confirm_password = input("Confirm Password: ")
            if new_password != confirm_password:
                print("Both password do not match, Try again")
                continue
            else:
                register_user(new_user, new_password)
                break
    else:
        print("Please enter 'l' or 'r' to continue...")


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()

    menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    # Register new user
    if menu == 'r':

        '''Add a new user to the user.txt file'''

        new_username = input("New Username: ")

        if is_user_exists(new_username):
            print("\nUser already exists, taking you to the main menu.\n")
            continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:
            register_user(new_username, new_password)
        else:
            print("\nPasswords do not match, taking you to the main menu.\n")

    elif menu == 'a':

        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following:
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and
             - the due date of the task.'''

        task_username = input("Name of person assigned to task: ").lower()

        if not is_user_exists(task_username):
            print("\nUser doesn't exist, taking you to the main menu.\n")
            continue

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date = datetime.strptime(task_due_date,
                                             DATETIME_STRING_FORMAT).date()
                curr_date = date.today()
                if due_date > curr_date:
                    break
                else:
                    print("\nDue date can't be in past, Try again.\n")

            except ValueError:
                print("\nInvalid datetime format. Please use the" +
                      " format specified.\n")
        add_task(task_username, task_title, task_description, curr_date,
                 due_date)

        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''

    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the
           format of Output.
        '''
        view_all_tasks()

    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the
           format of Output.
        '''
        while not login(current_user, current_password):
            current_user = input("Enter username: ")
            current_password = input("Enter password: ")

        while True:
            total_user_tasks = view_my_tasks(current_user)
            try:
                task_choice = int(input("Please select task number to " +
                                        "view/edit the details or enter -1 " +
                                        "for main menu: "))
            except Exception as e:
                print(e)

            if task_choice - 1 in range(0, total_user_tasks):
                user_selected_task = get_task_details(current_user,
                                                      task_choice - 1)

                modify = input("Do you want to modify task? (y/n): ").lower()

                if modify == "y":

                    while True:
                        if user_selected_task[-1].lower() == "yes":
                            print("\nTask is completed, not able to edit\n")
                            break
                        else:
                            modify_options = """What do you want to modify?
                            1. Assign task to different user
                            2. Due date of task
                            3. Mark task as complete
                            4. Quit
                            : """
                            try:
                                user_selection = int(input(modify_options))
                            except Exception as e:
                                print(e)

                            if user_selection == 1:
                                while True:
                                    new_user = input("Enter username " +
                                                     "of person: ")
                                    if not is_user_exists(new_user):
                                        print("User doesn't exist, Try again")
                                        continue
                                    else:
                                        update_task(user_selected_task,
                                                    user_selection, new_user)
                                        print(f"Task re-asigned to {new_user}")
                                        break
                            elif user_selection == 2:
                                new_due_date = input("Enter new due date" +
                                                     "(yyyy-mm-dd)")
                                update_task(user_selected_task, user_selection,
                                            new_due_date)
                                print(f"Due date is updated to {new_due_date}")
                                continue
                            elif user_selection == 3:
                                update_task(user_selected_task, user_selection,
                                            "yes")
                                print("\nTask marked as Completed\n")
                                break
                            elif user_selection == 4:
                                break

                            else:
                                print("\nWrong selection, Try again.\n")
                else:
                    print("\nTaking you to the your tasks options\n")
                    continue
            elif task_choice == -1:
                break

            else:
                print("\nPlease enter valid input, Try again.\n")
    elif menu == "gr":
        '''Only admin user can generate user and task overview reports'''
        if current_user == "admin":
            message = generate_reports()
            print(message)
        else:
            print("\nOnly admin can generate these reports.\n")
    elif menu == 'ds':
        '''Statistics will be displayed if user is logged in as admin'''
        if current_user == "admin":
            generate_reports()
            task_overview = read_file("task_overview.txt")
            for each_detail in task_overview:
                print(each_detail)
            user_overview = read_file("user_overview.txt")
            for each_detail in user_overview[0:4]:
                print(each_detail)
            data = []
            for each_user in user_overview[4:]:
                individual_list = [d.strip() for d in each_user.split("\t")
                                   if d != ""]
                data.append(individual_list)
            for record in data:
                for item in record:
                    print(item + "\t\t", end="")
                print()
        else:
            print("\nOnly admin can see the statistics.\n")

    elif menu == 'e':
        print('\nGoodbye!!!\n')
        exit()

    else:
        print("\nYou have made a wrong choice, Please Try again.\n")
