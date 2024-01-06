import math

print('Application running')

array = []


def returnMax(num):

    """
    :param num: the input number.
    :return: return the max binary value based on the number provided.
    """
    binaryString = bin(num)[2:]
    length = len(binaryString)
    adding = 0
    for i in range(length):
        adding += math.pow(2, i)
    return int(adding)


def returnMin(num):

    """

    :param num: the input number
    :return: return the min binary value based on the number provided
    """

    binaryString = bin(num)[2:]
    length = len(binaryString)
    adding = 0
    for i in range(length - 1):
        adding += math.pow(2, i)
    return int(adding)


def bet_umber(num):

    """

    :param num:
    :return: Encounter the number in an interval and calculates the number of bets
    """

    minimus = returnMin(num)
    maximus = returnMax(num)
    change = 0

    def is_greater(numerus, initialis):
        if numerus < initialis:
            return True
        else:
            return False

    def is_smaller(numerus, initialis):
        if numerus > initialis:
            return True
        else:
            return False

    mean = (minimus + maximus) / 2
    initial = mean
    percentage = 1 / 4
    counter = 0

    processes = 0
    procsUp = 0
    procsDown = 0

    while True:
        processes += 1

        print(round(initial))

        if round(initial) == num:
            break

        cond_g = is_greater(num, initial)

        previous_obj = {
            'initial': initial,
            'cond': cond_g,
        }
        delta = percentage / math.pow(2, counter + 1)
        print(f"Percentage: {percentage * 100}%, Delta: {delta * 100}%")

        if minimus < previous_obj['initial'] < initial and is_smaller(num, initial):
            minimus = initial
            print('new min', minimus)
        elif initial < previous_obj['initial'] < maximus and is_greater(num, initial):
            maximus = initial
            print('new max', maximus)

        if cond_g:
            procsDown += 1

            if processes == 0:
                maximus = previous_obj['initial']

            print(maximus, minimus)
            initial -= initial * percentage
            percentage += delta

            if round(initial) < minimus:
                print("Epa!")
                initial = previous_obj['initial']
                percentage /= 2
                initial -= initial * percentage
                continue

            if initial < maximus and is_greater(num, initial):
                maximus = initial
                print("new max", maximus)

            print(minimus, maximus)

        else:
            procsUp += 1

            if processes == 0:
                minimus = previous_obj['initial']

            initial += initial * percentage
            percentage += delta

            if initial > maximus:
                initial = previous_obj['initial']
                percentage /= 2
                initial += initial * percentage
                continue

        print(minimus, maximus)

        cond_g = is_greater(num, initial)
        obj = {
            'initial': initial,
            'cond': cond_g,
        }

        if obj['cond'] != previous_obj['cond']:
            print(f"Obj: {obj['cond']}, Previous: {previous_obj['cond']}")
            print(f"Current {obj['initial']}, Previous {previous_obj['initial']}")
            print('Change!')
            counter += 1
            print(f"{counter} switches...")
            print("\033[F" * 5, end="")
            print("\033[J", end="")
            percentage = 1 - percentage
            continue

    return {
        'commence': round(initial),
        'isgreater': is_greater(num, initial),
        'up': procsUp,
        'down': procsDown,
    }


def init(num):

    """

    :param num:
    :return: Initialize the bet
    """

    return bet_umber(num)
