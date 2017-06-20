from spy_details import spy,Spy,ChatMessage,friends    #import the classes named as Spy , ChatMessage , list of friends and object spy of the Spy class from the spy_details file
from steganography.steganography import Steganography  #import Stegnography class from stegnography module and stegnography file to encode and decode the message
from datetime import datetime                          #import datetime file from datetime module to use date and time functions
from termcolor import *                          #import colored file from termcolor module to print colored text
import colorama
from collections import Counter



#default status messages
Status_Messages = ["Hey there! I am using spychat.","Busy","Sleeping","At the movies"]


#to ask our spy whether he/she wants to continue as a default user or not
question = "Do you want to continue as " + spy.salutation + spy.name + " Y/N"
existing = raw_input(question)

# def is a keyword to create function
# add_status function is used to add the new status in existing Status_Messages list or to select status from older Status_Messages
def add_status():
    updated_status_message = None

    if spy.current_status_message != None:
        print "Your current status message is %s \n" % (spy.current_status_message)
    else:
        print "You don't have any status message currently "

    default = raw_input("Do you want to select from older status(Y/N)?")

    # if spy wants to set a new status
    if default.upper() == "N":              # upper() function will convert the 'n' or 'N' into uppercase letter 'N'
        new_status_message = raw_input("Which status message do you want to set?")
        if len(new_status_message) > 0:
            updated_status_message = new_status_message
            Status_Messages.append(updated_status_message)   #to append updated status message in Status_Messages list
            print "Status updated!"

    # if spy wants to select status from older status messages
    elif default.upper() == "Y":            # upper() function will convert the 'y' or 'Y' into uppercase letter 'Y'
        status_no = 1
        for message in Status_Messages:     # If the user wants to select from the older status updates,it shows the list of older status
            print str(status_no) + ". " + message
            status_no = status_no + 1

        message_selection = int(raw_input("Choose from the above status\n"))  #to take input from user

        if len(Status_Messages) >= message_selection:
            updated_status_message = Status_Messages[message_selection - 1]    #zero based indexing
            print "Status updated!"
        else:
            print "Please enter valid choice.. "
    else:
        print "The option you choose is not valid! Please enter either y or n."

    if updated_status_message:
        print "Your updated status message is %s" %(updated_status_message)
    else:
        print "You don't have any current status update"
    return updated_status_message



#function add_friend() is used to handle the case when user wants to add a friend
def add_friend():

    new_friend = Spy(" "," ",0,0.0)

    new_friend.name = raw_input("Please add your friend's name?")

    # here len()>0 func checks that user should not press enter without giving any name
    # isspace() func does not allow the user to enter blank spaces in place of name
    if len(new_friend.name) > 0 and new_friend.name.isspace() == False:
        new_friend.salutation = raw_input("Are they Mr. or Ms.?")

    # to check that user does not enter anything else except Mr. or Ms.
        if new_friend.salutation == "Mr." or new_friend.salutation == "Ms.":

            new_friend.name = new_friend.salutation + " " + new_friend.name
            new_friend.age = int(raw_input("Age?"))
            new_friend.rating = float(raw_input("Spy rating?"))

            if new_friend.age > 12 and new_friend.rating >= spy.rating:
                friends.append(new_friend)          #adding new friends to old list
                print "New friend added!"

            else:
                print "Sorry! We can't add a spy with the details you provided.Please enter valid age or valid rating.."
        else:
            print "Please enter valid option.Choose either Mr. or Ms."
    else:
        print "Please enter valid spy name!!"

    return len(friends)        # returns no of friends in friends list



#select_friend() function is used to choose from the list of spy friends added by the user.
def select_friend():
    item_no = 0
    for friend in friends:
        print "%d. %s aged %d with rating %.2f is online" % (item_no +1,friend.name,friend.age,friend.rating)
        item_no = item_no + 1
    friend_choice = raw_input("Choose from your friends")
    friend_choice_position = int(friend_choice) - 1
    return friend_choice_position


# send_message() function calls the select_friend() method to get which friend is to be communicated with
def send_message():
    friend_choice = select_friend()
    print "index = " + str(friend_choice)

    original_image = raw_input("What is the name of the image?")     # Ask the user for the name of the image they want to encode the secret message with.
    output_path = "output.jpg"
    text = raw_input("What do you want to say?")     # Ask the user for the secret message they want to hide.
    list_of = text.split(" ")
    if len(list_of)>= 100:
        print "you cross the message limit"
    else:
        print "your secret message has been ready"

        Steganography.encode(original_image,output_path,text)      # Using the Steganography library hide the message inside the image

        new_chat = ChatMessage(text,True)

        friends[friend_choice].chats.append(new_chat)










#read_message() function calls the select_friend method to get which friend is to be communicated with.
def read_message():
    sender = select_friend()
    print "index = " + str(sender)

    output_path = raw_input("What is the name of the file?")        #Ask the user for the name of the image they want to decode the message from
    secret_text = Steganography.decode(output_path)

    new_chat = ChatMessage(secret_text,False)


    friends[sender].chats.append(new_chat)          #Append the new_chat to chats list inside the friends list for the particular friend
    print "Your secret message has been saved!" + "secret text = " + secret_text





# read_chat_history() function is used to read the entire chat history of a particular friend
def read_chat_history():
    read_for = select_friend()
    colorama.init()
    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print "[%s] %s %s" %(chat.time.strftime("%d %B %Y"),"You said: " ,chat.message)
        else:
            print "[%s] %s said: %s" %(chat.time.strftime("%d %B %Y"),friends[read_for].name,chat.message)










# start_chat is a function that is used to start the chat application and in this, spy has multiple choices to choose from.
def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name

    if spy.age > 12 and spy.age < 50:

        print "Authentication Complete! Welcome " + spy.name + ", age: " + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard!!"

        #The menu will be displayed until the user chooses the menu option to Close the application
        show_menu = True
        while (show_menu):
            menu_choices = "What do you want to do?\n 1. Add a status update\n 2. Add a friend\n 3. Send a secret message\n 4. Read a secret message\n 5. Read Chats from a user\n 6. Close the application\n"
            menu_choice = raw_input(menu_choices)
            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)
                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    no_of_friends = add_friend()
                    if no_of_friends == 1:
                        print "you have %d friend " % (no_of_friends)
                    else:
                        print "you have %d friends " % (no_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                elif menu_choice == 6:
                    show_menu = False
                else:
                    print "The option you choose is not valid. Please enter valid choice!"

    else:
        print "Sorry! You are not of the correct age to be a spy"



# if spy wants to continue as a default user
if existing == "Y" or existing == "y":
# calling start_chat function to start the chat application
    start_chat(spy)
#if spy dont want to continue as default user
elif existing == "N" or existing == "n":

    spy = Spy(" "," ",0,0.0)


    #input all the spy details
    spy.name = raw_input("Welcome to spychat, you must tell me your spyname first : ")
    if len(spy.name) > 0 and spy.name.isspace() == False:
        spy.salutation = raw_input("What should i call you (Mr. or Ms.)?")
        if spy.salutation == "Mr." or spy.salutation == "Ms.":
            spy.age = raw_input("What is your age?")
            spy.age = int(spy.age)

            spy.rating = raw_input("What is your spy rating?")
            spy.rating = float(spy.rating)

            spy.is_online = True

            start_chat(spy)             # calling start_chat function to start the chat application

        else:
            print "Please enter valid option.Choose either Mr. or Ms."


    else:

        print "Please add a valid spy name"      # if spy press enter without giving any name
else:

    print "Please enter valid choice!!"           #if spy enters anything else instead of Y,y,N or n


