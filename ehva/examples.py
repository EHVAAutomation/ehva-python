from ehva.ehva_api import EhvaApi

API_KEY = "584721"
URL = "https://localhost:5001"


def basic_example():
    """
    Basic example showing how to consume the rest api.
    Fetch all existing wafers and display them
    """

    api = EhvaApi(URL, API_KEY)

    wafers = api.wafers
    print("Wafer dict keys:")
    for key in wafers[0].keys():
        print(key)

    print("\n List of existing wafers:")
    for wafer in wafers:
        print(f"\n-- {wafer['name']} --")
        for key in wafer.keys():
            print(key, ":", wafer[key])


def component_hierarchy_example():
    """
    This example shows how to retrieve the component hierarchy
        Wafer -> Reticle -> Die -> Circuit -> Optical Port
    """

    # Step 0: Instantiate api
    api = EhvaApi(URL, API_KEY)

    # Step 1: fetch all components from server, filter by hierarchical id
    wafer_of_interest = "Google Wafer 1"
    wafer = [wafer for wafer in api.wafers if wafer["name"] == wafer_of_interest][0]
    reticles = [r for r in api.reticles if r["waferId"] == wafer["id"]]
    dies = [d for d in api.dies if d["reticleId"] in [r["id"] for r in reticles]]
    circuits = [c for c in api.circuits if c["dieId"] in [d["id"] for d in dies]]
    optical_ports = [
        op
        for op in api.optical_ports
        if op["componentId"] in [c["id"] for c in circuits]
    ]

    # Setp 2: Display full hierarchy
    tab = 6 * "-"
    print("Wafer:", wafer["name"])
    for reticle in reticles:
        print(tab, "Reticle:", reticle["name"])
        for die in [d for d in dies if d["reticleId"] == reticle["id"]]:
            print(2 * tab, "Die:", die["name"])
            for circuit in [c for c in circuits if c["dieId"] == die["id"]]:
                print(3 * tab, "Circuit:", circuit["name"])
                for port in [
                    op for op in optical_ports if op["componentId"] == circuit["id"]
                ]:
                    print(
                        4 * tab, "Optical Port:", port["name"], f"({port['position']})"
                    )


def run_sequence_example():
    """
    In this example we show how to run a Test Sequence
    from the API and retrieve the Sequence outputs.
    """

    api = EhvaApi(URL, API_KEY)

    dut = {
        "wafer": "Google Wafer 1",
        "reticle": "R1",
        "die": "tj1",
        "circuit": "mmi1x2_4448d2b6_add_fib_ae5552bc",
        "optical port": "vertical_te_10",
        "electrical port": None,
    }

    result = api.run_sequence("API Test", "2", dut=dut)

    for key in result.keys():
        print(f"{key} : {result[key]}")


if __name__ == "__main__":
    basic_example()
# component_hierarchy_example()
# run_sequence_example()
