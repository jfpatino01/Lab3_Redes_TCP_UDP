import os
import random

# Define the size of the file in bytes
size = 10 * 1024 * 1024

# Define the path and filename for the new file
filename = "250MB.txt"

# Generate random data to fill the file
data = bytearray(os.urandom(size))

# Write the data to the file
with open(filename, "wb") as f:
    f.write(data)