def generate_ids_map():
    """
    Return generator of generators.
    Used for creating integers that will be used as products IDs.
    """
    stp = 100
    genex = ((y for y in range(x, stp + x)) for x in range(1, 2500000, stp))
    return genex


def generate_ids_map_from_file():
    with open("ids_list.txt", "r") as file:
        ids = file.readlines()

        cleaned_list = [int(x.replace("\n", "")) for x in ids]
        stp = 50
        genex = (cleaned_list[i : i + stp] for i in range(0, len(cleaned_list), stp))

        return genex
