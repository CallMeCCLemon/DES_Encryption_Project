

class DESEncryption:
    def __init__(self):

        self.s_boxes = [
            [
                # S box 1
                ['101', '010', '001', '110', '011', '100', '111', '000'],
                ['001', '100', '110', '010', '000', '111', '101', '011']
            ],
            [
                # S box 2
                ['100', '000', '110', '101', '111', '001', '011', '010'],
                ['101', '011', '000', '111', '110', '010', '001', '100']
            ]
        ]

        self.key = '011001010'

    def encrypt(self, message, iterations):
        # Given a 12 bit message, return the encrypted equivalent
        # Input should not have 0b at the start. We will add this at the final result
        iteration = 0
        middle_index = len(message)/2
        left_bits = message[0:middle_index]
        right_bits = message[middle_index:]
        while iteration < iterations:
            f_calculation = self.f_function(right_bits, self.get_key(iteration))
            temp = left_bits
            left_bits = right_bits
            right_bits = bin(int('0b' + temp, 2) ^ int('0b' + f_calculation, 2))[2:]
            while len(right_bits) < middle_index:
                right_bits = '0' + right_bits
            iteration += 1
        return left_bits + right_bits

    def f_function(self, right_input, key):
        # First convert the 6-bit input into an 8 bit string
        new_right_input = '0b' + self.e_function(right_input)
        # Complete the XOR operation and remove the binary identifier
        xor_result = bin(int(new_right_input, 2) ^ int('0b' + key, 2))[2:]
        # S-Box lookup
        function_result = \
            self.s_boxes[0][int(xor_result[0], 2)][int(xor_result[1:4], 2)] + \
            self.s_boxes[1][int(xor_result[4], 2)][int(xor_result[5:8], 2)]
        # Returns bits without 0b
        return function_result

    def e_function(self, input_to_manipulate):
        input_to_use = '{0}{1}{2}{3}{4}'.format(
            input_to_manipulate[0:2],
            input_to_manipulate[3],
            input_to_manipulate[2:4],
            input_to_manipulate[2],
            input_to_manipulate[4:6])
        # returns bits without 0b
        return input_to_use

    def get_key(self, iteration):
        # Get the key matching the given iteration we are on
        key_to_return = ''
        while len(key_to_return) < 8:
            key_to_return += self.key[iteration % len(self.key)]
            iteration += 1
        # Returns bits without 0b
        return key_to_return

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