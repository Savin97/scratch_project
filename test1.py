# Test 1 q1
def max_couple(l1, size):
    if size==0:
        return 0
    if size == 1:
        return l1[0]
    current_sum = l1[0] + l1[-1]
    return max(current_sum, max_couple(l1[1:-1], size-2) )

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

def main():
    maxcouple = max_couple([2,6,1,7,8],5)   
    print(maxcouple)