from tools.loading import lazy_tabs
from utils.ui import interface


def energy_basics_page():
    from utils.generators.energy.energy_basics import EnergyBasicsGenerator

    title = "Types of Energy"
    prefix = "energy_basics"
    difficulties = ["Easy","Medium","Hard"]
    generator = EnergyBasicsGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def energy_conserv_page():
    from utils.generators.energy.energy_conserv import EnergyConservationGenerator

    title = "Conservation of Energy"
    prefix = "energy_conservation"
    generator = EnergyConservationGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def thermal_energy_page():
    from utils.generators.energy.thermal_loss import ThermalLossGenerator

    title = "Thermal Energy"
    prefix = "thermal"
    generator = ThermalLossGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def friction_distance_page():
    from utils.generators.energy.frict_and_dist import ThermalWithFrictionGenerator

    title = "Friction and Distance"
    prefix = "frict_dist"
    generator = ThermalWithFrictionGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def main():
    tab_specs = [
        ("Types of Energy", energy_basics_page),
        ("Conservation of Energy", energy_conserv_page),
        ("Thermal Energy", thermal_energy_page),
        ("Friction and Distance", friction_distance_page),
    ]

    lazy_tabs(tab_specs, state_key="energy_tabs", auto_load_first=True)


if __name__ == "__main__":
    main()
