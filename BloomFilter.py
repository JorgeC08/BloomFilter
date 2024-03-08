import math
import sys

class BloomFilter:

    # Initializing the Bloom Filter with the size of the array and the number of hash functions
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    # Adding an item to the Bloom Filter by setting the bits at the calculated indexes to 1
    def add(self, item):

        for seed in range(self.hash_count):
            #Creating the hash with built in hash function
            hash_result = hash(str(seed) + item) % self.size
            # Setting the bit at the hash result index to 1
            self.bit_array[hash_result] = 1
    def check(self, item):

        #Checking if the item is in the Bloom Filter
        for seed in range(self.hash_count):
            hash_result = hash(str(seed) + item) % self.size

            # If any of the bit at the calculated index is 0 the item is NOT on the filter
            if self.bit_array[hash_result] == 0:
                return False

        # If all the bits at the calculated indexes are 1 the item is PROBABLY on the filter
        return True


def calculate_parameters(n, p):
    # Calculating the parameters of the array of bits.
    # m = size of the array and k = number of hash functions
    # n = number of items in the array and p = probability of false positives
    m = -(n * math.log(p)) / (math.log(2) ** 2)
    k = (m / n) * math.log(2)
    return int(m), int(k)

def main():

    # Check if enough arguments are provided to minimize mistakes while testing
    if len(sys.argv) != 3:
        print("Usage: python BloomFilter.py <input_file> <check_file>")
        sys.exit(1)

    # Probability of false positives, the more precise the more memory is needed
    p = 0.0000001

    # Command line arguments, input_file and check_file
    input_file = sys.argv[1]
    check_file = sys.argv[2]

    # Populating the Bloom filter with emails from input_file
    with open(input_file, 'r') as file:
        next(file)
        uniqueEmails = {email.strip() for email in file}
    expectedNumItems = len(uniqueEmails)

    # Calculating the parameters of the Bloom Filter
    size, hash_count = calculate_parameters(expectedNumItems, p)

    # Creating the bloom filter
    bloom_filter = BloomFilter(size, hash_count)

    # Adding the emails to the bloom filter
    for email in uniqueEmails:
        bloom_filter.add(email.strip())

    # Check emails from the second file and output results
    with open(check_file, 'r') as file:
        next(file)
        for email in file:
            email = email.strip() # Removing the \n from the end of the line
            result = "Probably in the DB" if bloom_filter.check(email) else "Not in the DB"
            print(email + "," + result) # Output format, sometimes moodle has problem with print(f"{email},{result}")

if __name__ == "__main__":
    # The 'if' statement is to prevent errors when submiting through moodle
    if len(sys.argv) > 1:
        main()

