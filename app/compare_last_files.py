"""

 Created by Razvan at 1/1/2021
 
 
"""

from os import listdir


def import_data(PATH):

    """Function to import the last two files located inside the data directory"""

    if len(listdir(PATH))<2:
        f = open(PATH + "/" + "0_empty_file.txt", "a")
        f.write("This is definitely empty!")
        f.close()

    files = [f for f in listdir(PATH)]
    first = PATH + "/" + files[-1]
    second = PATH + "/" + files[-2]

    print("First file is: ", first)
    print("Second file is: ", second)


    return first, second


def files_to_lists(first, second):

    """Function to convert the imported files to lists.
    Also removes the first ement which is the total number of followers"""

    with open(first) as file:
        first_content = file.readlines()
        first_content = [x.strip() for x in first_content]
        first_content.pop(0)

    with open(second) as file:
        second_content = file.readlines()
        second_content = [x.strip() for x in second_content]
        second_content.pop(0)

    return first_content, second_content


def get_new_followers(first, second):

    """Function to extract the list of people which are in the n file and not in the n-1 file"""

    new_followers = []
    first = sorted(first)
    second = sorted(second)

    for e in first:
        if e not in second:
            new_followers.append(e)

    return list_to_string(new_followers)


def get_unfollowers(first, second):

    """Function to extract the list of people which are in the n-1 file and not in the n file"""

    unfollowers = []
    for e in second:
        if e not in first:
            unfollowers.append(e)

    return list_to_string(unfollowers)


def list_to_string(l):

    """Function to covert the lists into more readable strings"""

    text = ""
    for e in range(len(l)):
        if e != len(l)-1:
            text += l[e] + ", "
        else:
            text += l[e] + "."

    return text


def prep_data(PATH):
    first, second = import_data(PATH)
    first, second = files_to_lists(first, second)

    return first, second
