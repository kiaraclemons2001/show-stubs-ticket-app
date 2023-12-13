import sqlite3
import user

menu = (
    "1: Login\n"
    "2: Register\n"
    "3: Buy Tickets\n"
    "4: Add Points\n"
    "5: View Account\n"
    "6: View Events\n"
    "7: View Main Menu\n"
    "8: Logout\n"
    "9: exit\n"
)


def connect():
    try:
        path = "./Database/TicketDatabase.db"
        sqlite_connection = sqlite3.connect(path)
        return sqlite_connection
    except sqlite3.Error as error:
        print("An error occurred with database connection", error)
        return None


def cursor(connection):
    try:
        new_cursor = connection.cursor()
        return new_cursor
    except sqlite3.Error as error:
        print("An error occurred with cursor creation", error)
        return None


def register(new_user):
    new_username = new_user.username
    new_password = new_user.userPassword
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            balance = str(new_user.userPoints)
            addPoints = str(new_user.addedPoints)
            query = (
                '''SELECT * FROM Customers WHERE Username =\'''' + new_username
                + '''\' AND Password=\'''' + new_password + '''\''''
            )
            try:
                new_cursor.execute(query)
                if len(new_cursor.fetchall()) == 0:  # If user does not exist
                    query = (
                        '''INSERT INTO Customers (Username, Password, AccountBalance, 
                        AddedPoints) VALUES ("''' + new_username + '''", "''' + new_password
                        + '''", "''' + balance + '''", "''' + addPoints + '''")'''
                    )
                    new_cursor.execute(query)
                    conn.commit()  # Saves the updates made to table(s)
                    conn.close()
                    return (
                        "You have been successfully added as a new user, congrats!"
                        + "\n" + menu
                    )
                else:
                    return (
                        "This user already exists, try logging in"
                        + "\n" + menu
                    )
            except sqlite3.Error as error:
                conn.close()
                return (
                        "An error occurred: " + str(error) + "\n"
                        + "Login must be unique\n" + menu
                )
        else:
            return "Could not create cursor"
    else:
        return "Could not connect"


def login(temp_user):
    temp_username = temp_user.username
    temp_password = temp_user.userPassword
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            query = (
                '''SELECT * FROM Customers WHERE Username =\'''' + temp_username
                + '''\' AND Password=\'''' + temp_password + '''\''''
            )
            try:
                new_cursor.execute(query)
                resultset = new_cursor.fetchall()
                if (len(resultset) != 0) and (len(resultset) != -1):  # If user does exist
                    existing_user = user.User(temp_username, temp_password)
                    for row in resultset:
                        existing_user.userID = row[0]
                        existing_user.userPoints = row[3]
                        existing_user.addedPoints=row[4]
                    existing_user.loginFlag = True
                    conn.close()
                    return existing_user
                else:
                    print("not found")
                    return temp_user
            except sqlite3.Error as error:
                print("An error occurred ", error)
                conn.close()
                return temp_user
        else:
            print("Could not create cursor.")
            return temp_user
    else:
        print("Could not establish connection.")
        return temp_user


def execute_event():
    query1 = '''SELECT * FROM Event'''
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            try:
                new_cursor.execute(query1)
                resultset = new_cursor.fetchall()
                string = ''
                for row in resultset:
                    string += "\nEvent number: " + str(row[0])
                    string += "\nEvent name: " + str(row[1])
                    string += "\nNumber of Tickets available: " + str(row[2])
                    string += "\nPrice of the tickets: " + str(row[3])
                    string += "\n"
                #print(string)
                return string
            except sqlite3.Error as error:
                error = str(error)
                return "An error occurred" + error
            finally:
                conn.close()
        else:
            return ("There was an error creating the cursor")
    else:
        return ("There was an error creating the connection")

def events_execute():
    query1 = '''SELECT * FROM Event'''
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            try:
                new_cursor.execute(query1)
                resultset = new_cursor.fetchall()
                my_events=[]
                for row in resultset:
                    my_events.append(int(row[1]))
                if (len(my_events) != 0):
                    print("Successful")
                    return my_events
                else:
                    print("There are no events")
                    return None
            except sqlite3.Error as error:
                error = str(error)
                print("An error occurred", error)
                return None
            finally:
                conn.close()
        else:

            print("There was an error creating the cursor")
            return None
    else:
        print("There was an error creating the connection")
        return None


def execute_account(user):
    query = (
            '''SELECT Username, AccountBalance, AddedPoints from Customers
             where Customer_ID =\'''' + str(user.userID) + '''\''''
    )
    string = ''
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            try:
                new_cursor.execute(query)
                resultset = new_cursor.fetchall()
                for row in resultset:
                    string += "\nUsername: " + str(row[0])
                    string += "\nAccount Balance: $" + str(row[1])
                    string += "\nNumber of Times to Add Points: "+str(row[2])
                    string += "\n"

            except sqlite3.Error as error:
                error = str(error)
                return "An error occurred: " + error + ".\n"
            #print(string)
            query1 = (
                    '''SELECT Event.Name, Event.Price From Event
                     Inner join Ticket on Event.Event_ID=Ticket.Event_ID
                    where Customer_ID= ''' + str(user.userID) + ''';'''
            )
            try:
                new_cursor.execute(query1)
                resultset = new_cursor.fetchall()
                for row in resultset:
                    string += "\nYou are seeing: " + str(row[0])
                    string += "\nand paid " + str(row[1]) + " for your ticket"
                    string += "\n"
            except sqlite3.Error as error:
                print("An error occurred" + str(error))
            #print(string)
            conn.close()
            return string
        else:
            return ("There was an error creating the cursor")
    else:
        return ("There was an error creating the connection")


def insert_query(query):
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            try:
                new_cursor.execute(query)
                conn.commit()
                print("Successful!")
                return True
            except sqlite3.Error as error:
                error = str(error)
                print("An error occurred: " + error + ".\n")
                return False
            finally:
                conn.close()
        else:
            print("There was an error creating the cursor")
    else:
        print("There was an error creating the connection")


def buy_ticket(user, eventnum):
    conn = connect()
    if conn is not None:
        new_cursor = cursor(conn)
        if new_cursor is not None:
            # list events

            # allow user to select the event they want
            # check the amount they have and the amount the ticket is worth

            # user.userPoints
            my_events = events_execute()
            has_event=any(eventnum in e for e in my_events)
            var = True if has_event else False
            if (var== True):



                query1 = (
                    '''SELECT TicketNumber, Price From Event where Event_ID=''' + str(eventnum)

                )
                try:
                    new_cursor.execute(query1)
                    resultset = new_cursor.fetchall()
                    for row in resultset:
                        if (int(row[0]) > 0):  # The value for the number of tickets is 0 or less than 0
                            # check if the event has enough tickets to purchase

                            if (row[1] < user.userPoints):
                                print("The price of the ticket is", str(row[1]))
                                query_update = (
                                        '''Update Event SET TicketNumber=TicketNumber-1
                                         where Event_ID=''' + str(eventnum)
                                )
                                if (insert_query(query_update)):


                                    #update the user's points

                                    user.subtract_points(int(row[1]))

                                    #update the database's points
                                    account_query= (
                                        '''Update Customers SET AccountBalance=AccountBalance-'''
                                        +str(row[1])+''' where Customer_ID=''' + str(user.userID)
                                    )
                                    if (insert_query(account_query)):

                                        # purchase ticket (subtract from total amount)
                                        # insert into ticket table
                                        query2 = (
                                            '''INSERT INTO Ticket (Customer_ID, Event_ID) 
                                            Values (\'''' + str(user.userID) + '''\', \''''
                                            + str(eventnum) + '''\' )'''
                                        )
                                        if (insert_query(query2)):
                                            return("Congratulations, you have a new ticket")
                                        else:
                                            return("There was an error in creating your ticket")
                                    else:
                                        return("There was an error in updating your account information")
                                else:
                                    return("Sorry, there was an error in the database")
                            else:
                                return("Sorry, you do not have enough to purchase this ticket")
                        else:
                            return("Sorry, there are no more tickets to purchase for this event")
                except sqlite3.Error as error:
                    return("You have an error" + str(error))
            else:
                return("There was an error grabbing the events")
        else:
            return ("There was an error creating the cursor")
    else:
        return("There was an error creating the connection")


def add_points(user):
    if (user.addedPoints != 0):  #Makes sure the user cannot go over a certain limit to add points
        print("You can add points but you have "+ str(user.addedPoints-1)+ " more times to add points")


        query_update = (
                '''Update Customers SET AccountBalance=AccountBalance+50
                 where Customer_ID=''' + str(user.userID)
        )
        if(insert_query(query_update)):
            #update the user's points

            query_addedPoints = (
                '''Update Customers SET AddedPoints=AddedPoints-1
                                     where Customer_ID=''' + str(user.userID)
            )
            if(insert_query(query_addedPoints)):


                user.add_points(50)

                #update the limit
                user.addedPoints= user.addedPoints - 1

                return("Congratulations, you have 50 more points")
            else:
                return("Sorry, there was an error in updating your user")
        else:
            return("Sorry, there was an error in adding your points")
    else:
        return("Sorry, you have exceeded the amount of times you can add points to your account")


# Put customer id in there


# check to make sure the user has enough to purchase
# user.getAmount

# get username & delete points
# check the user has the points

# make adjustments to points & number of tickets

# add to database

