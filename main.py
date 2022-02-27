import mysql.connector as mycon
import datetime
import time

con = mycon.connect(host='127.0.0.1', user='root', password='1234')
if con.is_connected():
    print("Database Online\n")

cur = con.cursor()
cur.execute("create database if not exists Infinix")
cur.execute("use Infinix")
cur.execute("create table if not exists Main(UID int(4) primary key not null, Phone_Number varchar(30) not null, PASSWORD blob, NAME varchar(40) , TIME_OF_CREATION varchar(60), balance int(5) default 0)")


def LoginUser(uid, passw, name, number):
    cur.execute("select * from Main where UID = {}".format(uid))
    if cur.fetchall() == []:
        date = datetime.datetime.now()
        cur.execute("insert into main values({},{}, AES_ENCRYPT('{}','admin'), '{}', '{}', 0)".format(uid, number, passw, name, date))
        print("New Login Created.\nWelcome user {}: {}".format(uid, name))
        con.commit()
        status = True

    else:
        status = False
        cur.execute("select AES_DECRYPT(password, 'admin') from Main where uid = {}".format(uid))
        t = [item[0] for item in cur.fetchall()][0].decode()
        for i in range(3, 0, -1):
            if passw != t:
                print("Sorry Wrong Password.{} attempt(s) remaining".format(i-1))
                passw = input("Enter Password:")
            elif passw == t:
                print("###Login Success###")
                status = True
                break
            elif i < 2:
                print("Sorry out of attempts Shutting Down!")
    return status


def ForgotPass(uid, passnew):
    promp = input("Are u an admin?(y/n): ")
    if promp == 'y':
        root = input("Enter Root Password(Case Sensitive): ")
        if root == 'Call911':
            ask = input("Are you sure to change pass of user {}?(y/n):".format(uid))
            if ask == 'y':
                cur.execute("update main set password = AES_ENCRYPT('{}','admin') where uid = {}".format(passnew,uid))
                print("Successfully changed Password of user", uid)
                con.commit()
            else:
                print("Okei Nvm that")
        else:
            print("Sorry You are not authorized to perform this action")
    else:
        print("Contact an administrator for help")


def Check_Creation(uid):
    cur.execute("select TIME_OF_CREATION from main where uid = {}".format(uid))
    date = cur.fetchall()
    print([item[0] for item in date][0])
    if not [item[0] for item in date][0]:
        print("Enter a valid UID")


def GameAdd(console):
    if console.lower() == 'pc':
        name = input("Game: ")
        rate = int(input("Rate: "))
        genre = input("Genre: ")
        avail = int(input("Availability: "))
        date = input("Date of Update:")
        multi = input("Multiplayer? ")
        ps4 = 'NO'
        pc = 'yes'
        cur.execute("use Infinix")
        cur.execute("Insert into Games values('{}',{},'{}',{},'{}','{}','{}','{}')".format(name, rate, genre, avail,
                                                                                              date, multi, ps4, pc))
        con.commit()
        print("Added Successfully")
    elif console.lower() == 'ps4':
        name = input("Game: ")
        rate = int(input("Rate: "))
        genre = input("Genre: ")
        avail = int(input("Availability: "))
        date = input("Date of Update:")
        multi = input("Multiplayer? ")
        ps4 = 'Yes'
        pc = 'No'
        cur.execute("use Infinix")
        cur.execute(
            "Insert into Games values('{}',{},'{}',{},'{}','{}','{}', '{}')".format(name, rate, genre, avail, date,
                                                                                      multi, ps4, pc))
        con.commit()
        print("Added Successfully")
    elif console.lower() == 'both':
        name = input("Game: ")
        rate = int(input("Rate: "))
        genre = input("Genre: ")
        avail = int(input("Availability: "))
        date = input("Date of Update:")
        multi = input("Multiplayer? ")
        ps4 = 'Yes'
        pc = 'Yes'
        cur.execute("use Infinix")
        cur.execute(
            "Insert into Games values('{}',{},'{}',{},'{}','{}','{}', '{}')".format(name, rate, genre, avail, date,
                                                                                    multi, ps4, pc))
        con.commit()
        print("Added Successfully")
    else:
        print("We have only PS4 and PC right now")


def GameList(console):
    if console.lower() == 'pc':
        n = 1
        cur.execute("select NAME from games where PC = 'YES'")
        for i in [item[0] for item in cur.fetchall()]:
            print(n, '.', i)
            n += 1

    elif console.lower() == 'ps4':
        n = 1
        cur.execute("select NAME from games where PS4 = 'YES'")
        for i in [item[0] for item in cur.fetchall()]:
            print(n, '.', i)
            n += 1
    else:
        print("Enter a valid console Budd\n")
        pass


def GameSearch(Name):
    cur.execute("select name from games where name like '%{}%'".format(Name))
    name = [item[0] for item in cur.fetchall()][0]
    cur.execute("select * from Games where Name = '{}'".format(name))
    op = cur.fetchall()
    if op == []:
        print("Sorry mate, we don't have {} right now".format(Name))
    else:
        print("Name:", [item[0] for item in op][0], '\nRate:', [item[1] for item in op][0], '\nAVAILABLE:',
              [item[3] for item in op][0])


def GameStart(uid, Name, time):
    cur.execute("create table if not exists Stock_atm(Name varchar(60) Primary key,Availability int(2))")
    cur.execute("create table if not exists console_check(C_ID int(2) Primary Key, Status int(2) default 1 check(status = 0 or status = 1),UID int(4))")
    cur.execute("create table if not exists user_check(UID int(4) Primary key, Status int(2) default 0 check(Status = 0 or Status = 1),Pending_Payment int(5) default 0)")
    cur.execute("insert into user_check(UID) select UID from main where not exists (select UID from user_check where user_check.uid = main.uid)")

    try:
        cur.execute('insert into Stock_atm select Name, availability from Games')
        for i in range(10):
            cur.execute("insert into console_check(C_ID,UID) value({},{})".format(i + 1, 0))
        con.commit()
    except:
        pass
    con.commit()
    cur.execute("select * from stock_atm where Name = '{}'".format(Name))
    op = cur.fetchall()
    stock = [item[1] for item in op][0]
    cur.execute("select C_ID from console_check where Status = 1")
    c_all = cur.fetchall()
    print(c_all)
    c_id = [item[0] for item in c_all][0]
    cur.execute("select status from user_check where UID = {}".format(uid))
    status = cur.fetchall()
    online = [item[0] for item in status][0]
    cur.execute("select Rate_Per_Hour from games where name = '{}'".format(Name))
    deta = cur.fetchall()
    rate = [item[0] for item in deta][0]
    cost = rate * time
    if stock != 0 and online == 0:
        print("Your Game is Ready to Begin")
        stock -= 1
        print("You may use Console {}".format(c_id))
        status = 0
        cur.execute("update stock_atm set availability = {} where Name = '{}'".format(stock, Name))
        cur.execute("update Console_check set Status = {} where C_ID = {}".format(status, c_id))
        cur.execute("update user_check set status = 1, Pending_Payment = Pending_Payment + {} where UID = {}".format(cost, uid))
        con.commit()
    elif stock == 0:
        print("Sorry someone is already playing {}".format(Name))
    elif online == 1:
        print("You are already playing a game elsewhere. Please Logout before proceeding :D")
    else:
        print("An unexpected error occurred, Please contact admin ")


def GameStop(uid, name):
    cur.execute("select status from user_check where UID = {}".format(uid))
    status = cur.fetchall()
    online = [item[0] for item in status][0]
    if online == 1:
        cur.execute("select name from games where name like '%{}%'".format(name))
        deta = cur.fetchall()
        Name = [item[0] for item in deta][0]
        cur.execute("update user_check set status = 0 where UID = {}".format(uid))
        cur.execute("update console_check set status = 1 where uid = {}".format(uid))
        cur.execute("update stock_atm set availability = availability + 1 where name = '{}'".format(Name))
        con.commit()
        print("You have stopped playing {}".format(Name))
    else:
        print("You aren't playing any game now")


def Logout(uid, passw):
    cur.execute("select AES_DECRYPT(password, 'admin') from Main where uid = {}".format(uid))
    t = [item[0] for item in cur.fetchall()][0].decode()
    cur.execute("select Pending_payment from user_check where uid = {}".format(uid))
    payment = [item[0] for item in cur.fetchall()][0]
    if passw == t:
        y = input("Are you Sure to logout?(Y/N):")
        ye = 'y'
        verify = True
    elif passw != t:
        print("Sorry wrong password mate;-;")
        ye = 'n'
        verify = False
    if y.lower() == 'y' and verify and payment == 0:
        cur.execute("update console_check set status = 1 where UID = {}".format(uid))
        cur.execute("update user_check set status = 0 where UID = {}".format(uid))
        cur.execute("update log_check set LOGGED_IN = 0 where UID = {}".format(uid))
        print("Logout Success\nC ya later gator ;)")
    elif payment != 0:
        print("Make ur Payment before logging out,STUFF ain't free dude")
    else:
        print("Keep playing :D")


def check_wallet(uid):
    cur.execute("select balance from main where uid = {}".format(uid))
    deta = cur.fetchall()
    print("The balance is:", [item[0] for item in deta][0])


def Add_money(uid, amount):
    cur.execute("update main set balance = balance + {} where uid = {}".format(amount,uid))
    print(amount, "has been successfully credited into the user's account!")
    con.commit()


def Check_bill(uid):
    cur.execute("select Pending_payment from user_check where uid = {}".format(uid))
    payment = [item[0] for item in cur.fetchall()][0]
    print('You need to pay {} Rupees before you logout'.format(payment))
    return payment


def Pay_bill(uid, payment):
    cur.execute("select Pending_payment from user_check where uid = {}".format(uid))
    amount = [item[0] for item in cur.fetchall()][0]
    if payment == amount:
        print("Payment Done(Happy-Kachingg-Noices)\nYou are free to logout or keep playing")
        cur.execute("update user_check set Pending_Payment = 0 where uid = {}".format(uid))
        con.commit()
    elif payment > amount:
        print("Please Collect:", payment-amount, "as balance.\nThank You for Visiting IdeArc!")
    else:
        print("Payment not enuff, recheck ur bill or get glasses xD")


def uid_check():

    while True:
        try:
            id = int(input("Enter UID:"))
            break
        except:
            print("Enter a Valid ID!")
            continue
    return id


def Close(root):
    if root == 'Call911':
        return True
    else:
        return False

choice = 0
while choice != 9876:
    print("1.User Login/Create ID\n2.Show available Games\n3.Search for a Game?\n4.Start Gaming!\n5.Check/Pay bill\n6.Stop Gaming\n7.Logout\n8.Admin tier\n9.Check Balance")
    while True:
        try:
            choice = int(input("Enter your Choice:"))
            break
        except:
            print("Enter a Valid Number!")
            continue
    cond = False
    cur.execute("create table if not exists log_check(UID int(4),LOGGED_IN int(2) default 0)")
    if choice == 1:
        prompt = input("Are you an existing User?(Y/N):")
        uid = uid_check()
        cur.execute("select * from Main where UID = {}".format(uid))
        if not cur.fetchall():
            prompt = 'n'
        if prompt.lower() == 'y':
            passw = input("Enter your password(CaSe SenSitiVe): ")
            cond = LoginUser(uid, passw, 'default', 'default')
            con.commit()
            if cond:
                cur.execute("insert into log_check(UID) select UID from main where not exists (select UID from log_check where log_check.uid = main.uid)")
                cur.execute("update log_check set LOGGED_IN = 1 where uid = {}".format(uid))
            print("\n")
        else:
            cur.execute("select Max(uid) from main")
            try:
                uid = [item[0] for item in cur.fetchall()][0] + 1
            except TypeError:
                uid = 1
            name = input("Enter your Name:")
            number = int(input("Enter your Phone Number: "))
            passw = input("Enter your password(CaSe SenSitiVe):")
            cond = LoginUser(uid, passw, name, number)
            con.commit()
            if cond:
                cur.execute("insert into log_check(UID) select UID from main where not exists (select UID from log_check where log_check.uid = main.uid)")
                cur.execute("update log_check set LOGGED_IN = 1 where uid = {}".format(uid))
            print("\n")
    elif choice == 2:
        console = input("We have either PS4 or PC for u to play as of now\nEnter the console to see list(PS4/PC):")
        GameList(console)
        print("\n")
    elif choice == 3:
        Name = input("Enter a game's name to Search:")
        GameSearch(Name)
        print("\n")
    if 3 < choice < 8:
        uid = uid_check()
        cur.execute("select LOGGED_IN from log_check where uid = {}".format(uid))
        cond = [item[0] for item in cur.fetchall()][0]
        print("\n")
        if cond == 1:
            if choice == 4:
                name = input("Enter the game u want to play(Name as in list): ")
                cur.execute("select name from games where name like '%{}%'".format(name))
                deta = cur.fetchall()
                Name = [item[0] for item in deta][0]
                time = int(input("Enter time in Hours you wanna play:"))
                GameStart(uid, Name, time)
                print("\n")
            elif choice == 5:
                pay = Check_bill(uid)
                print("Contact an admin and pay {}".format(pay))
                print("\n")
            elif choice == 6:
                name = input("Name of game you stopped playing:")
                cur.execute("select name from games where name like '%{}%'".format(name))
                deta = cur.fetchall()
                Name = [item[0] for item in deta][0]
                GameStop(uid, Name)
            elif choice == 7:
                passw = input("Enter your password to confirm logout:")
                Logout(uid, passw)
                print("\n")
            else:
                print("Enter an option from 1-8!")
                print("\n")
        else:
            print("Login First mate!")
            print("\n")
    elif choice == 9876:
        break
    elif choice == 8:
        root = input("Enter Root password:")
        if root == 'Call911':
            while True:
                print("1.Forgot Password\n2.Check date and time of account creation\n3.Add new Games\n4.Pay bill\n5.Add Money to Wallet\n6.Close User-Interface\n7.Exit admin mode\n")
                while True:
                    try:
                        pmp = int(input("Enter your Choice:"))
                        break
                    except:
                        print("Enter a Valid Number!")
                        continue
                if pmp == 1:
                    uid = uid_check()
                    passnew = input("Enter new pass without showing the admin:")
                    ForgotPass(uid, passnew)
                    print("\n")
                elif pmp == 2:
                    uid = uid_check()
                    Check_Creation(uid)
                    print("\n")
                elif pmp == 3:
                    console = input("PS4 or PC?")
                    GameAdd(console)
                    print("\n")
                elif pmp == 4:
                    uid = uid_check()
                    payment = int(input("Enter money received:"))
                    Pay_bill(uid, payment)
                    print("\n")
                elif pmp == 5:
                    uid = uid_check()
                    amount = int(input("Enter Money to Add into Wallet: "))
                    promp = input("Are you sure u want to add {} into User {}'s account?(Y/N) ".format(amount,uid))
                    if promp.lower() == "y":
                        Add_money(uid, amount)
                    else:
                        print("Nvm")
                        pass
                elif pmp == 6:
                    conf = input("R u sure?(Y/N)")
                    if conf.lower() == 'y':
                        sure = Close(root)
                        if sure:
                            print("Goodbye")
                            choice = 9876
                            break
                        else:
                            print("OK nvm")
                            print("\n")
                elif pmp == 7:
                    break
    elif choice == 9:
        uid = uid_check()
        passw = input("Enter Password: ")
        cur.execute("select AES_DECRYPT(password, 'admin') from Main where uid = {}".format(uid))
        t = [item[0] for item in cur.fetchall()][0].decode()
        if passw != t:
            print("Sorry Wrong Password!")
        elif passw == t:
            check_wallet(uid)
        else:
            print("Wrong Pass Mate")
            pass

