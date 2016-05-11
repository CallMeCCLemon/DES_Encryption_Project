from DESEncryption import DESEncryption


class TestSuite:
    def __init__(self):
        self.encrypt = DESEncryption()

    def test_get_key(self):
        print "Get Key Test:"
        # The first and last strings should be identical
        for count in range(0, len(self.encrypt.key)+1):
            self.encrypt.get_key(count)

    def test_e_function(self):
        function_return = self.encrypt.e_function('011001')
        print "E Function Test:"
        print "Expected Return: 01010101"
        print "Function Return: {0}".format(function_return)

    def test_f_function(self):
        function_result = self.encrypt.f_function('100110', '01100101')
        print "F Function Test:"
        print "Expected Return: 000100"
        print "Function Return: {0}".format(function_result)

    def test_encryption(self):
        message = '011100100110'
        result = self.encrypt.encrypt(message, 1)
        print "Encryption Test"
        print "Input: {0}".format(message)
        print "Expected Return: 100110011000"
        print "Function Return: {0}".format(result)
