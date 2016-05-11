

class DESEncryption:
    def __init__(self):
        pass

    def encrypt(self, initial_message):
        # Given a 12 bit message, return the encrypted equivalent
        # Input should not have 0b at the start. We will add this at the final result
        iteration = 0
        message = self.initial_permutation(initial_message)
        middle_index = len(message)/2
        left_bits = message[0:middle_index]
        right_bits = message[middle_index:]
        while iteration < 16:
            f_calculation = self.f_function(right_bits, self.get_key(iteration))
            temp = left_bits
            left_bits = right_bits
            right_bits = bin(int('0b' + temp, 2) ^ int('0b' + f_calculation, 2))[2:]
            while len(right_bits) < middle_index:
                right_bits = '0' + right_bits
            iteration += 1
        message = left_bits + right_bits
        final_message = self.final_permutation(message)
        return final_message

    def f_function(self, right_input, key):
        # First convert the 6-bit input into an 8 bit string
        new_right_input = '0b' + self.expansion_permutation(right_input)
        # Complete the XOR operation and remove the binary identifier
        xor_result = bin(int(new_right_input, 2) ^ int('0b' + key, 2))[2:]

        # Parse xor_result into an array of 6 bit
        bit_array = []
        for count in range(0, 8):
            bit_array.append(xor_result[count*6:(count+1)*6 - 1])

        # S-Box
        # Changed with the expansions to support 64-bit encryption
        function_result = ''
        for index in range(0, len(bit_array)):
            row = int('0b' + bit_array[index][0:2], 2)
            column = int('0b' + bit_array[index][2:], 2)
            function_result += self.s_box_lookup(index, row, column)

        # Returns bits without 0b
        return function_result

    def s_box_lookup(self, box_number, row, column):
        s_box_file = open('S_{0}.txt'.format(box_number), 'r')
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

    def get_key(self, iteration):
        # Get the key matching the given iteration we are on
        key_to_return = ''
        while len(key_to_return) < 8:
            key_to_return += self.key[iteration % len(self.key)]
            iteration += 1
        # Returns bits without 0b
        # return key_to_return




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
                permutated_message += message[index]
        return permutated_message