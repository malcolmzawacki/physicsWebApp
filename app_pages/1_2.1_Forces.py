from utils.ui import interface
from utils.worksheet_ui import worksheet_shortcut

def newtons_2nd():
    worksheet_shortcut("Newton's Second Law")
    from utils.generators.force_generator import ForceGenerator
    title = "Newton's Second Law"
    prefix = "newtons_2nd"
    difficulties = ["Easy","Medium","Hard"]
    generator = ForceGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def tension():
    worksheet_shortcut('Tension')
    from utils.generators.forces.tension_generator import TensionGenerator
    title = "Tension Problems"
    prefix = "tension"
    difficulties = ["Easy","Medium","Hard"]
    generator = TensionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

def atwood():
    worksheet_shortcut('Atwood Machines')
    from utils.generators.forces.atwood_generator import AtwoodGenerator
    title = "Atwood Machines"
    prefix = "atwood"
    difficulties = ["Medium"]
    generator = AtwoodGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def inclines():
    worksheet_shortcut('Inclined Planes')
    from utils.generators.forces.incline_generator import InclineGenerator
    title = "Inclined Planes"
    prefix = "incline"
    difficulties = ["Medium"]
    generator = InclineGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

def center_of_mass():
    worksheet_shortcut('Center of Mass')
    from utils.generators.forces.center_of_mass_generator import CenterOfMassGenerator
    title = "Center of Mass"
    prefix = "com"
    difficulties = ["Easy", "Medium", "Hard"]
    generator = CenterOfMassGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

