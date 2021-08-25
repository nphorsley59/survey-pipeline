def yes_no(prompt):
    while True:
        user_input = input(f"{prompt} (Y/N) ")
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Invalid input...")
            continue