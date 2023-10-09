def start():
    n = int(input("How many rows of stars should I print? "))

    for x in range(n + 1):
        print("*" * x)


if __name__ == "__main__":
    start()
