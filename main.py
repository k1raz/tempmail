from create_email import CreateMail

def main():
    action = int(input("1. Create email \n2. Read email\n"))
    
    if action == 1:
        CreateMail()
        return
    else:
        email = input("Enter email what u want to read:\n")
        CreateMail(email)
        return

main()