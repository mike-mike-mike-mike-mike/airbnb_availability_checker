from jobs.check_availabilities_job import CheckAvailabilitiesJob


def main():
    CheckAvailabilitiesJob().perform()


if __name__ == "__main__":
    main()
