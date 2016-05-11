# from TestSuite import TestSuite
from DESEncryption import DESEncryption


def main():
    message = '0000000100100011010001010110011110001001101010111100110111101111'
    encryption = DESEncryption()
    final_message = encryption.encrypt(message)
    print "\n\nInitial Message: {0}".format(message)
    print "Initial Key: {0}".format(encryption.key)
    print "Final Message: {0}".format(final_message)


# def test_encryption():
#     tester = TestSuite()
#     tester.test_encryption()

if __name__ == "__main__":
    main()
