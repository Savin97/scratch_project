def remove_string(s, l1, n):
    # Base case: no more strings to remove
    if n == 0:
        return s
    
    # Remove all occurrences of the last string in the list
    current = l1[n - 1]
    s = s.replace(current, "")
    
    # Recursive call on the remaining list
    return remove_string(s, l1, n - 1)


s = "abcdxyzabc"
l1 = ["ab", "yz"]
n = 2

print("Before:", s, ", remove:", l1)
result = remove_string(s, l1, n)
print("After :", result)
