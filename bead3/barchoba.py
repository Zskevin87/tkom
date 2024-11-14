import random

class Barchoba:

    interval_start = 1
    interval_end = 100
    thought_number = -1

    def __init__(self):
        self.__GenerateRandomNumber__()
        self.__PrintNumber__()
        exit(0)
    
    # Generates a random number in a closed interval of [1,100] and gives it to self.number.
    def __GenerateRandomNumber__(self):
        self.number = random.randint(1,100)

    # The implementation of binary search.
    # Parameters:
    # a : The list to search in
    # n : The length of the list
    # t : The target we search for
    def __BinarySearch__(self):
        # the floor of the middle number of the interval
        if ()


        '''
        l = 0
        r = n - 1

        if l > r:
            raise Exception("The length of the list cannot be less or equal to 0!")

        while l <= r:
            m = ((l + r) // 2)
            if a[m] < t:
                l = m + 1
            elif a[m] > t:
                r = m - 1
            else:
                return m
        raise Exception("Binary search was unsuccessful.")
        '''
    def __CheckNumber__():
        pass

    def __PrintNumber__(self):
        print(f"The number is: {self.number}")


b = Barchoba()