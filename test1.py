# Test 1 q1
def max_couple(l1, size):
    if size==0:
        return 0
    if size == 1:
        return l1[0]
    sum1 = l1[0] + l1[-1]
    l1.pop(0)
    l1.pop(-1)

    return max(sum1, max_couple(l1, size-2)) #type:ignore
maxcouple = max_couple([2,6,1,7,8] , 5)   
print(maxcouple)



def max_couple_no_slicing(l1, size):
    if size==0:
        return 0
    if size == 1:
        return l1[0]
    left = l1.pop(0) # remove first
    right = l1.pop() # remove last 
    current_sum = left + right
    # restore list
    l1.insert(0, left)
    l1.append(right)

    current_sum = l1[0] + l1[-1]
    return max(current_sum, max_couple(l1, size-2) )





# q2
def is_valid_email(email):
    if not (8 <= len(email) <= 30):
        return False

    # exactly one '@'
    if email.count("@") != 1:
        return False

    user, server = email.split("@")

    # username must start with a letter
    if not user or not user[0].isalpha():
        return False

    # username has at least one uppercase and at least one lowercase letter
    if not any(ch.isupper() for ch in user):
        return False
    if not any(ch.islower() for ch in user):
        return False

    # server has at least one dot
    if "." not in server:
        return False

    # server must end with at least two letters
    if len(server) < 2 or not server[-1].isalpha() or not server[-2].isalpha():
        return False

    return True

print( is_valid_email("example@Dan") ) # print line to check


# q4
def create_dict1(songs):
    result = {}

    for song in songs:
        writers = songs[song]["writers"]
        performers = songs[song]["performer"]

        # Count writers
        for writer in writers:
            if writer not in result:
                result[writer] = [0, 0]
            result[writer][0] += 1

        # Count performers
        for performer in performers:
            if performer not in result:
                result[performer] = [0, 0]
            result[performer][1] += 1

    return result


songs = {
    "Rocket Man": {
    "writers": ["Elton John", "Bernie Taupin"],
    "performer":["Elton John"]
    },
    "Someone Like You": {
    "writers": ["Adele"],
    "performer": ["Adele"]
    },
    "Thinking Out Loud": {
    "writers": ["Ed Sheeran"],
    "performer": ["Ed Sheeran"]
    },
}

print(create_dict1(songs))