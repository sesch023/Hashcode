def read_data(file):
    data = {
        "teams": (0, 0, 0),
        "pizza": []
    }

    with open(file) as file:
        data["teams"] = list(map(int, file.readline().split(" ")[1:-1]))
        pizzas = file.read().split("\n")[:-1]
        for pizza in pizzas:
            data["pizza"].append(pizza.split(" ")[1:])

    return data


def write_score_file(data, target):
    with open(target, "w") as file:
        file.write(str(len(data)) + "\n")

        for element in data:
            for el in element:
                file.write(str(el) + " ")
            file.write("\n")


def scoring(data_file, score_file):
    data = read_data(data_file)
    pizzas = data["pizza"]
    teams = data["teams"]
    score_points = 0

    with open(score_file) as score:
        pizzas_num = int(score.readline().rstrip())
        for pizza in list(map(str.rstrip, score.read().split("\n")[:-1])):
            pizza_data = list(map(int, pizza.split(" ")))
            team_num = pizza_data[0]
            team_pizzas = pizza_data[1:]
            team_pizza_set = set()

            for pizza_el in team_pizzas:
                team_pizza_set |= set(pizzas[pizza_el])
                pizzas[pizza_el] = []

            if teams[team_num - 2] > 0:
                score_points += (len(team_pizza_set) * len(team_pizza_set))

    return score_points


data = read_data("files/c_many_ingredients.in")
score_target = "scores/a_submit_new"
result = [
    [2, 1, 4],
    [3, 0, 2, 3]
]

write_score_file(result, score_target)
print(scoring("files/a_example", score_target))
