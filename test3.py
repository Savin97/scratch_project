# q1
def is_rolling_list(l1, index=0):
    # If list has less than 2 elements → False
    if len(l1) < 2:
        return False

    # If reached last comparison → True
    if index == len(l1) - 1:
        return True
    # Find leftmost digit of next number recursively (inline logic)
    num = l1[index + 1]
    while num >= 10:
        num //= 10
    # Check rolling condition
    if l1[index] % 10 != num:
        return False

    # Recursive step
    return is_rolling_list(l1, index + 1)

print(is_rolling_list([123]))                 
print(is_rolling_list([123, 345]))            
print(is_rolling_list([123, 345, 541, 12]))    
print(is_rolling_list([127, 345, 541, 12]))     

