import sys
from parser import Parser, StandardParserError, CustomParserError
from graph import Graph
from rich.traceback import install
from rich import print, markdown
from pathfinding import PathFinding
install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:

    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    parse = Parser(file_path)
    parse.dispatcher()
    wifi = Graph(parse)
    PathFinding(wifi)
    
    data = {key: value.extract_data() for key, value in parse.hubs.items()}
    # 1. We define the table header with the exact same padding we will use for the data
    print("\n" + "=" * 70)
    print(f"{'ZONE NAME':<12} | {'X':<3} | {'Y':<3} | {'TYPE':<12} | {'DRONES':<6} | {'COLOR':<10}")
    print("-" * 70)

    # 2. We extract the physical zone dictionaries from your data map
    for zone_data in data.values():
        # 3. We extract the variables
        z_name = zone_data["name"]
        z_x = zone_data["x"]
        z_y = zone_data["y"]
        z_type = zone_data["zone_type"]
        z_limit = zone_data["max_drones"]
        z_color = zone_data["color"]

        # 4. We print them using strict left-aligned padding (<)
        print(f"{z_name:<12} | {z_x:<3} | {z_y:<3} | {z_type:<12} | {z_limit:<6} | {z_color or '':<10}")

    print("=" * 70 + "\n")



    # Quick test to ensure the WHOLE graph works, could crash?
    print("\n# FULL GRAPH TEST")
    md = markdown.Markdown("# FULL GRAPH INFORMATION\n\nThis is a **markdown** example.")
    # print(md)
    for zone_name in wifi.adj:
        neighbors = wifi.get_neighbors(zone_name)
        if not neighbors:
            print(f"Zone '{zone_name}' has NO connections.")
        else:
            for target_zone, conn, cost in neighbors:
                print(f"From '{zone_name:<10}' -> '{target_zone.name:<10}' | Cost: {cost} | Link Cap: {conn.max_link_capacity}")
if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
