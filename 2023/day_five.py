import structlog
import uuid
from utils import read_file

logger = structlog.get_logger()


SEED_TO_SOIL = []
SOIL_TO_FERTILIZER = []
FERTILIZER_TO_WATER = []
WATER_TO_LIGHT = []
LIGHT_TO_TEMPERATURE = []
TEMPERATURE_TO_HUMIDITY = []
HUMIDITY_TO_LOCATION = []

convert_map = {
    "seed-to-soil map:": SEED_TO_SOIL,
    "soil-to-fertilizer map:": SOIL_TO_FERTILIZER,
    "fertilizer-to-water map:": FERTILIZER_TO_WATER,
    "water-to-light map:": WATER_TO_LIGHT,
    "light-to-temperature map:": LIGHT_TO_TEMPERATURE,
    "temperature-to-humidity map:": TEMPERATURE_TO_HUMIDITY,
    "humidity-to-location map:": HUMIDITY_TO_LOCATION,
}


class Map:
    def __init__(self, destination_start, origin_start, map_range, map_type):
        self.id = uuid.uuid4()
        self.destination_start = destination_start
        self.origin_start = origin_start
        self.map_range = map_range
        self.map_type = map_type


class SeedRange:
    def __init__(self, origin, seed_range):
        self.origin = origin
        self.seed_range = seed_range


def parse_seeds(lines: list[str], seed_range: bool = False):
    if not seed_range:
        seeds = [int(seed) for seed in lines[0].split("seeds: ")[1].split(" ")]
    else:
        seeds = []
        potential_seeds = lines[0].split("seeds: ")[1].split(" ")
        k = 0
        while k < len(potential_seeds):
            seed_origin = int(potential_seeds[k])
            seed_range = int(potential_seeds[k + 1])
            seeds.append(SeedRange(origin=seed_origin, seed_range=seed_range))
            k += 2

    return seeds


def parse_maps(lines: list[str]):
    map_type = ""
    for line in lines[1:]:
        if line == "\n":
            continue
        else:
            if line[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                target = convert_map[line.split("\n")[0]]
                map_type = line.split(" ")[0]
                continue
            destination = int(line.split(" ")[0])
            origin = int(line.split(" ")[1])
            map_range = int(line.split(" ")[2].strip())
            map = Map(
                destination_start=destination,
                origin_start=origin,
                map_range=map_range,
                map_type=map_type,
            )
            target.append(map)


def convert_seed(seed: int, map_list: list[Map]) -> int:
    for map in map_list:
        if map.origin_start <= seed <= map.origin_start + map.map_range:
            seed_transformation = seed + (map.destination_start - map.origin_start)
            return seed_transformation

    return seed


def process_seeds(seeds: list[int]):
    for map_list in [
        SEED_TO_SOIL,
        SOIL_TO_FERTILIZER,
        FERTILIZER_TO_WATER,
        WATER_TO_LIGHT,
        LIGHT_TO_TEMPERATURE,
        TEMPERATURE_TO_HUMIDITY,
        HUMIDITY_TO_LOCATION,
    ]:
        seeds = [convert_seed(seed, map_list) for seed in seeds]

    return min(seeds)


def get_map_of_seed(seed: int, map_list: list[Map]) -> Map | None:
    for map in map_list:
        if map.origin_start <= seed < map.origin_start + map.map_range:
            return map
    return None


def convert_seed_range(seed_range: SeedRange, map_list: list[Map]) -> list[SeedRange]:
    result_ranges = []
    k = 0
    while k < seed_range.seed_range:
        map = get_map_of_seed(seed_range.origin + k, map_list)
        if map:
            new_seed_origin = (
                seed_range.origin + k + (map.destination_start - map.origin_start)
            )
            new_seed_range = min(
                [
                    (map.origin_start + map.map_range - (seed_range.origin + k)),
                    (seed_range.seed_range - k),
                ]
            )
            logger.info("new_seed_range_found_map", seed_range=seed_range.seed_range, new=new_seed_range)
            result_ranges.append(
                SeedRange(origin=new_seed_origin, seed_range=new_seed_range)
            )
            k += new_seed_range
        else:
            new_seed_origin = seed_range.origin + k
            max_seed_range_possible = [
                seed_range.origin + k - map.origin_start
                for map in map_list
                if (seed_range.origin + k < map.origin_start and seed_range.origin + k - map.origin_start > 0)
            ]
            max_seed_range_possible.extend([seed_range.seed_range - k])
            new_seed_range = min(max_seed_range_possible)
            logger.info("new_seed_range_no_found_map", seed_range=seed_range.seed_range, new=new_seed_range)
            result_ranges.append(
                SeedRange(origin=new_seed_origin, seed_range=new_seed_range)
            )
            k += new_seed_range

    return result_ranges


def process_seeds_smartly(seeds: list[SeedRange]):
    for map_list in [
        SEED_TO_SOIL,
        SOIL_TO_FERTILIZER,
        FERTILIZER_TO_WATER,
        WATER_TO_LIGHT,
        LIGHT_TO_TEMPERATURE,
        TEMPERATURE_TO_HUMIDITY,
        HUMIDITY_TO_LOCATION,
    ]:
        future_seeds = []
        for seed_range in seeds:
            future_seeds.extend(convert_seed_range(seed_range, map_list))
        logger.info("seed_count", count=sum([seed.seed_range for seed in future_seeds]))
        seeds = future_seeds

    return min(seed_range.origin for seed_range in seeds)


def main():
    lines = read_file("input_five.txt")
    seeds = parse_seeds(lines, seed_range=False)
    parse_maps(lines)
    first_answer = process_seeds(seeds)
    logger.info("first_question", answer=first_answer)

    new_seeds = parse_seeds(lines, seed_range=True)
    second_answer = process_seeds_smartly(new_seeds)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
