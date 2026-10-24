passward = "Preeti"
for attempt in range(3):
    match = input("Enter Password: ")
    if match == passward:
        print("Correct Passward")
    else:
        if attempt == 0:
            print("In Correct Passward ")
            print("two attempt is left")
        elif attempt == 1:
                    print("In Correct Passward")
                    print("one attempt is left")
        else:
            print("Incorrect Passward ")
            print("Account is locked")
