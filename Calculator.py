import sys
import math

def pythagoris(a, b): #define the fn
    a_squared = math.pow(a, 2)
    b_squared = math.pow(b, 2)
    return math.sqrt (a_squared + b_squared)

def main():
    command = sys.argv[1]

    if command == "add":
        x = int (sys.argv[2])
        y = int (sys.argv[3])
        print(x + y)

    if command == "sub":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        print(x - y)

    if command == "countto":
        x = int(sys.argv[2])

        for i in range(x):
            print (i)

    if command == "mul":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        print(x * y)

    if command == "div":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        print(x / y)

    if command == "hypot":
        a = int(sys.argv[2])
        b = int(sys.argv[3])
        print (pythagoris(a, b))

if __name__ == '__main__':
    main()
