import random
from Antigen import Antigen
from Landscape import Landscape


def main():
    random.seed(42)
    l = 10
    w = 10
    landscape = Landscape(l, w)
    t = 50
    total_data = []
    counter = 0
    for i in range(t):
        landscape.graph()
        for _ in range(random.randint(0, 6)):
            total_data.append(landscape.increment_time())

        for j in range(random.randint(0, 1)):
            curr_name = str(counter) + "th antigen"
            counter += 1
            print(landscape.clock)
            curr_ant = Antigen(name=curr_name, memory=random.randint(1, 4),
                               response=random.uniform(0, 1000),
                               spread=random.randint(1, 4))
            landscape.add_antigen(random.randint(0, l - 1), random.randint(0, w - 1), curr_ant)

    print("time: " + str(landscape.clock) + " (count =  " + str(landscape.get_landscape_count()) + "):")

    print(landscape)
    landscape.graph()

    print("Over")


if __name__ == "__main__":
    main()
