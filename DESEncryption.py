

class DESEncryption:
    def __init__(self):
        self.key = '0100110010100110010100110010100110010100110010100110010100110010'
        self.temp_key = ''
        self.key_permutation_1()
        circular_shift_order_file = open('DES_Key_Schedule_Calculations/schedule_of_left_shifts.txt')
        self.circular_shift_order = []
        for line in circular_shift_order_file:
            self.circular_shift_order.append(int(line))
        circular_shift_order_file.close()
        self.iteration = 0

    def encrypt(self, initial_message):
        # Given a 64 bit message, return the encrypted equivalent
        # Input should not have 0b at the start. We will add this at the final result
        self.iteration = 0
        message = self.initial_permutation(initial_message)
        middle_index = len(message)/2
        left_bits = message[0:middle_index]
        right_bits = message[middle_index:]
        while self.iteration < 16:
            key = self.update_key(self.iteration)
            if self.iteration == 0:
                print '\n'
                print 'K_{0}: {1}'.format(self.iteration+1, key)
                print 'L_{0}: {1}'.format(self.iteration, left_bits)
                print 'R_{0}: {1}'.format(self.iteration, right_bits)
            f_calculation = self.f_function(right_bits, key)
            temp = left_bits
            left_bits = right_bits
            right_bits = bin(int('0b' + temp, 2) ^ int('0b' + f_calculation, 2))[2:]
            while len(right_bits) < middle_index:
                right_bits = '0' + right_bits
            self.iteration += 1
        message = left_bits + right_bits
        final_message = self.final_permutation(message)
        return final_message

    def f_function(self, right_input, key):
        # First convert the 6-bit input into an 8 bit string
        new_right_input = '0b' + self.expansion_permutation(right_input)

        # Complete the XOR operation and remove the binary identifier
        xor_result = bin(int(new_right_input, 2) ^ int('0b' + key, 2))[2:]
        while len(xor_result) < 48:
            xor_result = '0' + xor_result
        # Parse xor_result into an array of 6 bit
        bit_array = []
        for count in range(0, 8):
            bit_array.append(xor_result[count*6:(count+1)*6])
            count += 1
        # S-Box
        # Changed with the expansions to support 64-bit encryption
        function_result = ''
        s_box_operations = []
        for index in range(0, len(bit_array)):
            row = int('0b' + bit_array[index][0] + bit_array[index][5], 2)
            column = int('0b' + bit_array[index][1:5], 2)
            temp = self.s_box_lookup(index, row, column)
            function_result += temp
            s_box_operations.append([index, row, column, int('0b' + temp,2)])
            index += 1
        function_result = self.permutation_function(function_result)
        # Returns bits without 0b
        if self.iteration == 0:
            print "E[R_{0}]: {1}".format(self.iteration, new_right_input[2:])
            print "Grouped Results: {0}".format(bit_array)
            for count in range(0, len(bit_array)):
                print "{0}: row-{1}, column-{2}, result-{3}".format(
                    bit_array[count],
                    s_box_operations[count][1],
                    s_box_operations[count][2],
                    s_box_operations[count][3])
            print "Concatenated Result: {0}".format(function_result)
        return function_result

    def s_box_lookup(self, box_number, row, column):
        s_box_file = open('S_Boxes/S_{0}.txt'.format(str(int(box_number)+1), 'r'))
        s_box = []
        for line in s_box_file:
            temp = []
            for index in line.split(' '):
                temp.append(int(index))
            s_box.append(temp)
        s_box_file.close()

        bits = bin(s_box[row][column])[2:]
        while len(bits) < 4:
            bits = '0' + bits
        return bits

    def update_key(self, iteration):
        # updates the temp key matching the given iteration we are on
        self.key_circular_shift(iteration)
        return self.key_permutation_2()

    def key_permutation_1(self):
        # Calculate the initial permutation fro the key
        permutation_format = open('DES_Key_Schedule_Calculations/PC_1.txt')
        self.temp_key = self.conduct_permutation(self.key, permutation_format)
        permutation_format.close()

    def key_permutation_2(self):
        permutation_format = open('DES_Key_Schedule_Calculations/PC_2.txt')
        key_to_use = self.conduct_permutation(self.temp_key, permutation_format)
        permutation_format.close()
        return key_to_use

    def key_circular_shift(self, iteration):
        for count in range(0, self.circular_shift_order[iteration]):
            self.temp_key = self.temp_key[1:] + self.temp_key[0]
            count += 1

    def initial_permutation(self, message):
        # Calculates the initial permutation of the given message
        ip_format = open('Permutation_Tables/initial_permutation_format.txt', 'r')
        updated_message = self.conduct_permutation(message, ip_format)
        ip_format.close()
        return updated_message

    def final_permutation(self, message):
        # Calculates the initial permutation of the given message
        fp_format = open('Permutation_Tables/inverse_initial_permutation_format.txt', 'r')
        updated_message = self.conduct_permutation(message, fp_format)
        fp_format.close()
        return updated_message

    def expansion_permutation(self, message):
        expansion_format = open('Permutation_Tables/expansion_permutation.txt')
        updated_message = self.conduct_permutation(message, expansion_format)
        expansion_format.close()
        return updated_message

    def permutation_function(self, message):
        permutation_format = open('Permutation_Tables/permutation_function.txt')
        updated_message = self.conduct_permutation(message, permutation_format)
        permutation_format.close()
        return updated_message

    def conduct_permutation(self, message, permutation_format):
        permutated_message = ''
        for line in permutation_format:
            indices = line.split(' ')
            for index in indices:
                permutated_message += message[int(index)-1]
        return permutated_message