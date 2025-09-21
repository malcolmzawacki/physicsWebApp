import streamlit as st
from utils.generators.collision_generator import CollisionGenerator
from utils.ui import interface

class collisions:
    
    @staticmethod
    def main():
        generator = CollisionGenerator()
        metadata = generator.stored_metadata()
        difficulties = ["Easy"]
        title = "Collisions"
        prefix = "collisions"

        ui = interface(prefix, title, generator, metadata, difficulties)
        ui.unified_smart_layout()


if __name__ == "__main__":
    collisions.main()
