from utils.ui import interface


def rotational_kinematics():
    from utils.generators.rotational_motion_generator import RotationalMotionGenerator
    title = "Rotational Kinematics"
    prefix = "rotational_kinematics"
    difficulties = ["Easy", "Medium", "Hard"]
    generator = RotationalMotionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

