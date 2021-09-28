"""
This program gives a step by step implementation of hamming code which is an error correction code that uses parity bits to detect and 
correct bit errors that can occur when data is transmitted from one point to another. It is one of the oldest codes used in error 
detection and correction of data.

For this implementation, I decided to use Classes and methods to implement the operation and inorder to break down every process.
"""
# First we implement the encoding class
class Encode ():
    def __init__(self):
        self.information = [int(i) for i in str(input("Enter your data"))] 
        self.information.reverse()
        self.r = 0
        self.parity_bits_positions = []
        self.dummy_data = []
        self.parity_binary_positions = []
        self.data_binary_positions = []  
        self.parity = []  
        self.encoded_data = [] 
        print("Original Data:", self.information)

    def parity_bits(self):
        # This method calculates the number of parity bits needed to be attached to the message being sent
        for self.r in range(len(self.information) + 1):
            if 2 ** self.r >= len(self.information) + self.r + 1:
                self.r = self.r
                break
        return f"No of parity bits: ", self.r

    def parity_bits_position(self):
        # This method calculates the positions that the parity bits are meant to be attached.
        for i in range(self.r):
            self.val1 = 2**i
            self.parity_bits_positions.append(self.val1)
        return f"Parity bit positions:", self.parity_bits_positions
 
    def insert_zeros(self):
        # Insert zeros into the parity bit positions to get the new dummy data. This will aid in easi=y manipulation of the information
        self.dummy_data = self.information.copy()
        for i in range (len(self.parity_bits_positions)):
            self.dummy_data.insert(self.parity_bits_positions[i]-1,0)
        return f"Pre-encoded data",self.dummy_data


    def index_of_ones_locations(self):
        """
        Convert the parity bit positions i.e 1,2,4,8 and also the dummy data indexes into binary data, i.e 1 is converted to 0001,
        from this, the index locations of all 1's are determined for the parity bit positions and also the dummy data indexes.
        We would use this information to calculate the values of the parity bits to be inserted into the data.
        """
        # First we calculate the binary data for the parity bit positions
        for i in self.parity_bits_positions:
            binary = bin(i)
            binary = binary[::-1]
            check = binary.index('1')
            self.parity_binary_positions.append(check)

        # Next we calculate the binary data for the indexes of the dummy data
        for i in range(1,len(self.dummy_data)+1):
            binary = bin(i)
            binary = binary[::-1]
            index = self.index_of_ones(binary,'1') #This method has been created below
            self.data_binary_positions.append(index)
        print("location of 1's in the binary equivalent of the parity bit locations:",self.parity_binary_positions)
        return f"Location of 1's in the binary equivalent of the pre-encoded data indexes ",self.data_binary_positions
    
    def index_of_ones(self,string,var):
        # This method is used to get the index positions of 1's in a binary data
        self.index_position_list  = []
        for i in range(len(string)):
            if string[i] == var:
                self.index_position_list.append(i)

                
        return self.index_position_list
    
    def calculate_parity_values(self):
        """
        This method is what then calculates the parity bits values to be inserted in the data
        """
        # The parity bit values are calculated using the XOR function implemented below, so we first create this function
        def xor(pos):
            r = 0
            for n in pos:
                r = r ^ n
            return r
        """
        Before using the XOR function, we need to determine the data bits that will be used to calculate each parity bit value for each
        parity bit location.
        Here, we check for the values of the binary of the data indexes that are equal to the values of the binary of the parity bits
        locations and store in a list for calculation.
        """
        count = 0
        while count < len(self.parity_binary_positions):
            self.data_indexes = []
            self.data_bits = []
            for i in range(len(self.data_binary_positions)):
                for j in self.data_binary_positions[i]:
                    if j == count:
                        self.data_indexes.append(i+1)
            self.data_indexes.pop(0)
            # print(self.data_indexes)
            for i in self.data_indexes:
                for j in range(len(self.dummy_data)):
                    if i-1 == j:
                        self.data_bits.append(self.dummy_data[j])
            # print(self.data_bits)
            parity_values = xor(self.data_bits)
            self.parity.append(parity_values)
            count+=1

        return  f"Parity bits Values:",self.parity

    def insert_parity_values(self):
        # Insert the parity bits calaculated into the parity bit positions to get the encoded data.
        self.encoded_data = self.information.copy()   
        for i in range (len(self.parity_bits_positions)):
            self.encoded_data.insert(self.parity_bits_positions[i]-1,self.parity[i])
        self.encoded_data.reverse()
        return f"Encoded Data:",self.encoded_data
            
# Now we implement the decode class. The methods used here are similar to what was implemented in the Encode class
class Decode ():
    def __init__(self):
        self.received_data = [int(i) for i in str(input("Enter the received data"))]
        self.received_data.reverse()
        self.parity_bits_positions = []
        self.parity_binary_positions = []
        self.data_binary_positions = []
        self.error_binary = []
        self.decoded_data = []
        print("Received data", self.received_data)


    def parity_bits(self):
        # This method calculates the number of parity bits that were attached in the message received
        for self.r in range(len(self.received_data) + 1):
            if 2 ** self.r >= len(self.received_data):
                self.r = self.r
                break
        return f"No of parity bits in data:", self.r

    def parity_bits_position(self):
        # This method calculates the positions that the parity bits are located in.
        for i in range(self.r):
            self.val1 = 2**i
            self.parity_bits_positions.append(self.val1)
        return f"Parity bits positions", self.parity_bits_positions

  

    def index_of_ones_locations(self):
        for i in self.parity_bits_positions:
            binary = bin(i)
            binary = binary[::-1]
            check = binary.index('1')
            self.parity_binary_positions.append(check)
        
        for i in range(1,len(self.received_data)+1):
            binary = bin(i)
            binary = binary[::-1]
            index = self.index_of_ones(binary,'1') 
            self.data_binary_positions.append(index)
        print("location of 1's in the binary equivalent of the parity bit locations:",self.parity_binary_positions)
        return f"Location of 1's in the binary equivalent of the pre-decoded data indexes ",self.data_binary_positions
    

    def index_of_ones(self,string,var):
    # This method is used to get the index positions of 1's in a binary data
        self.index_position_list  = []
        for i in range(len(string)):
            if string[i] == var:
                self.index_position_list.append(i)
                
        return self.index_position_list

    def calculate_error_bit(self):
        # The method used in calculating error bit is similar to that which is used in calculating parity values in the encoding part
        def xor(pos):
            r = 0
            for n in pos:
                r = r ^ n
            return r

        count = 0
        while count < len(self.parity_binary_positions):
            self.data_indexes = []
            self.data_bits = []
            for i in range(len(self.data_binary_positions)):
                for j in self.data_binary_positions[i]:
                    if j == count:
                        self.data_indexes.append(i+1)
            # self.check.pop(0)
            # print(self.data_indexes)
            for i in self.data_indexes:
                for j in range(len(self.received_data)):
                    if i-1 == j:
                        self.data_bits.append(self.received_data[j])
            # print(self.data_bits)
            parity_values = xor(self.data_bits)
            self.error_binary.append(str(parity_values))
            count+=1
        self.error_binary.reverse()

        return  f"Indicates if there is an error in the received data. '0000' means no error",self.error_binary

    def handle_error_bit(self):
        self.to_string = ""
        self.to_dec = self.to_string.join(self.error_binary)
        self.decimal = int(self.to_dec,2)

        if self.decimal == 0:
            return self.received_data
        else:
            if self.received_data[self.decimal-1] == 0:
                self.received_data[self.decimal-1] = 1
            else:
                self.received_data[self.decimal-1] = 0
        return f"If there is an error, it has been corrected", self.received_data
        
    def remove_parity_bits(self):
        self.decoded_data = self.received_data.copy()
        for i in range(len(self.parity_bits_positions)):
            self.decoded_data[self.parity_bits_positions[i]-1] = 2
        self.decoded_data = [i for i in self.decoded_data if i !=2]
        self.decoded_data.reverse()
        return f"Decoded Data:", self.decoded_data
 



info1 = Encode()
print(info1.parity_bits())
print(info1.parity_bits_position())
print(info1.insert_zeros())
print(info1.index_of_ones_locations())
print(info1.calculate_parity_values())
print(info1.insert_parity_values())

info2 = Decode()
print(info2.parity_bits())
print(info2.parity_bits_position())
print(info2.index_of_ones_locations())
print(info2.calculate_error_bit())
print(info2.handle_error_bit())
print(info2.remove_parity_bits())
