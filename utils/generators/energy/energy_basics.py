from random import randint as ri

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class EnergyBasicsGenerator(BaseGenerator):
  def __init__(self):
        super().__init__(state_prefix="energy_basics_")
  

  def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10
    
  # # # B A S I C    E N E R G Y    N U M B E R S # # # 
  def kinetic_energy(self,difficulty):
      upper = self.get_difficulty_range(difficulty)
      mass = ri(1,upper)
      velocity = ri(1,upper)
      flip = ri(0,1)
      if flip == 0:
          mass*=2
      else:
          velocity*=2
      return mass, velocity, 0.5*mass*velocity**2

  def gravitational_potential_energy(self,difficulty):
      upper = self.get_difficulty_range(difficulty)
      mass = ri(1,upper)
      height = ri(1,upper)
      return mass, height, mass*10*height

  def elastic_potential_energy(self,difficulty):
      upper = self.get_difficulty_range(difficulty)
      spring_constant = ri(2,upper)
      compression = ri(1,upper)
      flip = ri(0,1)
      if flip == 0:
          spring_constant*=2
      else:
          compression*=2
      return spring_constant, compression, 0.5*spring_constant*compression**2

  def work(self,difficulty):
      upper = self.get_difficulty_range(difficulty)
      force = ri(1,upper)
      distance = ri(1,upper)
      return force, distance, force*distance


  # # # B A S I C    E N E R G Y    P R 0 B L E M S # # # 
  def elastic_problem(self,difficulty):
      spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
      q_type = ri(0,2)
      dirn = ri(0,1)
      dirn_string = "compressed" if dirn == 0 else "stretched"
      if q_type == 0 or difficulty == "Easy":
          question = f"""A spring with strength {spring_constant:.2f} N/m is {dirn_string} by {compression:.2f} meters.
          \n What is the amount of elastic potential energy held in the spring?"""
          answer = elastic_e
          unit = "Elastic Potential Energy (Joules)"
      elif q_type == 1:
          question = f"""A spring with strength {spring_constant:.2f} N/m contains {elastic_e} Joules of elastic potential energy.
          \n How much was this spring {dirn_string}?"""
          answer = compression
          unit = "Compression Distance (meters)"
      else:
          question = f"""A spring is {dirn_string} by {compression:.2f} meters, and contains {elastic_e} Joules of elastic potential energy.
          \n What is the strength of the spring constant?"""
          answer = spring_constant
          unit = "Spring Strength (N/m)"

      return {"question": question, "answers": [answer], "units": [unit]}
  
  def kinetic_problem(self,difficulty):
      mass, velocity, kinetic_e = self.kinetic_energy(difficulty)
      q_type = ri(0,2)
      noun = random_noun()
      if q_type == 0 or difficulty == "Easy":
          question = f"""How much kinetic energy does a {mass:.2f} kg {noun} moving at {velocity:.2f} m/s have?"""
          answer = kinetic_e
          unit = "Kinetic Energy (Joules)"
      elif q_type == 1:
          question = f"""How fast would a {mass:.2f} kg {noun} have to move to have {kinetic_e} Joules of kinetic energy?"""
          answer = velocity
          unit = "Velocity (m/s)"
      else:
          question = f"""How much mass would a {noun} moving at {velocity:.2f} m/s need to have to contain {kinetic_e} Joules of kinetic energy?"""
          answer = mass
          unit = "Mass (kilograms)"

      return {"question": question, "answers": [answer], "units": [unit]}
  
  def gravitational_problem(self,difficulty):
      mass, height, gravit_e = self.gravitational_potential_energy(difficulty)
      q_type = ri(0,2)
      noun = random_noun()
      if q_type == 0 or difficulty == "Easy":
          question = f"""How much gravitational potential energy does a {mass:.2f} kg {noun} 
          held {height:.2f} meters above the ground have?"""
          answer = gravit_e
          unit = "Gravitational Potential Energy (Joules)"
      elif q_type == 1:
          question = f"""How high up would a {mass:.2f} kg {noun} have to be to have 
          {gravit_e} Joules of gravitational potential energy?"""
          answer = height
          unit = "Height (meters)"
      else:
          question = f"""How much mass would a {noun} at a height of {height:.2f} meters need to have 
          to contain {gravit_e} Joules of gravitational potential energy?"""
          answer = mass
          unit = "Mass (kilograms)"

      return {"question": question, "answers": [answer], "units": [unit]}
  
  def work_problem(self,difficulty):
      force, distance, work = self.work(difficulty)
      q_type = ri(0,2)
      noun = random_noun()
      if q_type == 0 or difficulty == "Easy":
          question = f"""A {noun} is moved {distance:.2f} meters by a {force} Newton force. 
          \n How much work was done?"""
          answer = work
          unit = "Work (Joules)"
      elif q_type == 1:
          question = f"""Over how much distance would a {force} Newton force 
          have to push a {noun} before it did {work} Joules of work?"""
          answer = distance
          unit = "Distance (meters)"
      else:
          question = f"""{work} Joules of work are done on a {noun} over a distance of {distance:.2f} meters.
          \n How much force was applied?"""
          answer = force
          unit = "Force (Newtons)"

      return {"question": question, "answers": [answer], "units": [unit]}
  

  # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
  def choose_problem_dict(self,problem_type, difficulty):
      if problem_type == "Elastic Potential Energy":
          return self.elastic_problem(difficulty)
      elif problem_type == "Kinetic Energy":
          return self.kinetic_problem(difficulty)
      elif problem_type == "Gravitational Potential Energy":
          return self.gravitational_problem(difficulty)
      elif problem_type == "Work":
          return self.work_problem(difficulty)
      
  
  def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
           "Elastic Potential Energy": {
                "honors" : r"EPE = \frac{1}{2} k \Delta x^2", 
                "conceptual": r"""EPE = \frac{1}{2} k \Delta x^2 \;\; , 
                \;\; k = \frac{2 \cdot EPE}{\Delta x^2} \;\; , 
                \;\; \Delta x = \sqrt{\frac{2 \cdot EPE}{k}}"""
                },
            "Kinetic Energy": {
                "honors": r"KE = \frac{1}{2} m v^2",
                "conceptual": r"""KE = \frac{1}{2} m v^2\;\; ,
                \;\; m = \frac{2KE}{v^2} \;\; ,
                \;\; v = \sqrt{\frac{2KE}{m}}"""
            },               
            "Gravitational Potential Energy" : {
                "honors": r"GPE = mgh",
                "conceptual": r"""GPE = mgh\;\; ,
                \;\; m = \frac{GPE}{gh} \;\; ,
                \;\; h = \frac{GPE}{mg}"""
            },
            "Work": {
                "honors": r"W = Fd",
                "conceptual": r"""W = Fd\;\; ,
                \;\; F = \frac{W}{d} \;\; ,
                \;\; d = \frac{W}{F}"""
            },
        }
