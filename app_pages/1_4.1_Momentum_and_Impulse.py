from utils.ui import interface


def momentum():
    from utils.generators.momentum_generators.momentum import MomentumGenerator
    title = "Momentum"
    prefix = "momentum"
    difficulties = ["Easy"]
    generator = MomentumGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()    

def impulse():
    from utils.generators.momentum_generators.impulse_generator import ImpulseGenerator
    title = "Impulse"
    prefix = "impulse"
    difficulties = ["Easy","Medium","Hard"]
    generator = ImpulseGenerator()
    metadata = generator.stored_metadata()
    
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(diagram_title="Diagram", expanded=True)


def collisions():
    from utils.generators.momentum_generators.collision_generator import CollisionGenerator
    title = "Collisions"
    prefix = "collisions"
    difficulties = ["Easy"]
    generator = CollisionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


