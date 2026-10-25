user_name = input("Enter Your Name: ").lower()
user_password = input("Enter Your Password: ").lower()
inbuilt_user_name = "admin"
inbuilt_user_password = "admin123"

if user_name == inbuilt_user_name and user_password == inbuilt_user_password:
    print("Login successfill")
else:
    print("Invalid username or password")