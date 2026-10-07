def convertDate(date):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    date = date.strip()

    if "/" in date:
        try:
            month, day, year = date.split("/")

            # Convert strings to integers
            month = int(month)
            day = int(day)
            year = int(year)

            # Month must be between 1 and 12
            if month < 1 or month > 12:
                return None

            # Day must be between 1 and 31
            if day < 1 or day > 31:
                return None

            # Return required format: YYYY-MM-DD
            return f"{year:04d}-{month:02d}-{day:02d}"
        
        except ValueError:
            return None

    try:
        month, day, year = date.split(" ")

        # Month must be one of our valid month names
        if month not in months:
            return None

        # Day contains a comma, e.g. "8,"
        day = int(day.replace(",", ""))

        year = int(year)

        # Day must be between 1 and 31
        if day < 1 or day > 31:
            return None

        month = months.index(month) + 1

        return f"{year:04d}-{month:02d}-{day:02d}"

    except ValueError:
        return None


def main():

    while True:
        date = input("Date: ")

        result = convertDate(date)

        # None means the date was invalid
        if result is None:
            continue

        # Valid date
        print(result)
        break


if __name__ == "__main__":
    main()