from utils.ui import interface


def torque_activity():
    from utils.generators.torque_generator import TorqueGenerator

    title = "Torque"
    prefix = "torque"
    difficulties = ["Easy", "Medium", "Hard"]
    generator = TorqueGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(expanded=True)
