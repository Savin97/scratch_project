# test 1 q1
# [2,6,1,7,8]
# [6,1,7]
# [4]

# max_couple([4], 1) # 4

# [2,6,1,4,7,8]
# max_couple([1,4],2) # 5


def max_couple(l1, size):
    if size == 0:
        return 0
    if size == 1:
        return l1[0]
    if size == 2:
        return l1[0] + l1[1]

    left = l1.pop(0) # remove first
    right = l1.pop() # remove last 

    # restore list
    l1.insert(0, left)
    l1.append(right)

    current_sum = l1[0] + l1[-1]
    return max(current_sum, max_couple(l1, size-2) ) # [6,1,4,7,8]

def main():
    pass

main()