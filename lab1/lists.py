from calendar import month_name


def start():
    all_months = month_name[1:]
    print(all_months[2])
    print(all_months[:3])
    print(all_months[:2] + all_months[3:])
    print("January" in all_months)


if __name__ == "__main__":
    start()
