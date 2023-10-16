def start():
    nums: list[int] = list()

    while True:
        try:
            raw = input()
            if raw == "stop":
                break

            nums.append(int(raw))
        except KeyboardInterrupt:
            exit(0)

    length = len(nums)

    print("=== Results ===")
    print(f"You entered {length} numbers.")
    print(f"Minimum number: {min(nums)}")
    print(f"Maximum number: {max(nums)}")
    print(f"Mean: {sum(nums) / length}")


if __name__ == "__main__":
    start()
