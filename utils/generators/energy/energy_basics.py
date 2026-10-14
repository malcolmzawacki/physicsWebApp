from random import randint as ri

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun
from utils.quantities import PROFILES, QUANTITIES, equation
from utils.setup_schema import make_setup

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


  @staticmethod
  def _target(difficulty, variant, targets):
      choice = ri(0, 2) if variant is None else variant
      if choice not in (0, 1, 2):
          raise ValueError("Energy Basics requires variant 0, 1, or 2")
      return targets[0 if difficulty == "Easy" else choice]

  @staticmethod
  def _shown(profile, values):
      return {key: f"{value:.2f} {QUANTITIES[PROFILES[profile][key].quantity].unit}"
              for key, value in values.items()}

  @staticmethod
  def _payload(profile, values, target, question):
      role = PROFILES[profile][target]
      return {"question": question, "answers": [values[target]],
              "units": [f"{role.name} ({QUANTITIES[role.quantity].unit})"],
              "extras": {"setup": make_setup(profile, values, set(values) - {target}, [target])}}

  def elastic_problem(self, difficulty, *, variant=None):
      k, x, energy = self.elastic_potential_energy(difficulty)
      values = {"E": energy, "k": k, "x": x}
      target = self._target(difficulty, variant, ("E", "x", "k"))
      direction = "compressed" if ri(0, 1) == 0 else "stretched"
      shown = self._shown("elastic_energy", values)
      if target == "E":
          question = f"An ideal spring with spring constant {shown['k']} is {direction} by {shown['x']} from its relaxed length. How much elastic potential energy does it store?"
      elif target == "x":
          question = f"An ideal spring with spring constant {shown['k']} stores {shown['E']} of elastic potential energy. How far is it {direction} from its relaxed length?"
      else:
          question = f"An ideal spring is {direction} by {shown['x']} from its relaxed length and stores {shown['E']} of elastic potential energy. What is its spring constant?"
      return self._payload("elastic_energy", values, target, question)

  def kinetic_problem(self, difficulty, *, variant=None):
      mass, speed, energy = self.kinetic_energy(difficulty)
      values = {"E": energy, "m": mass, "v": speed}
      target = self._target(difficulty, variant, ("E", "v", "m"))
      noun = random_noun()
      shown = self._shown("kinetic_energy", values)
      if target == "E":
          question = f"A {shown['m']} {noun} moves at a speed of {shown['v']}. What is its kinetic energy?"
      elif target == "v":
          question = f"A {shown['m']} {noun} has {shown['E']} of kinetic energy. What is its speed?"
      else:
          question = f"A {noun} moves at a speed of {shown['v']} and has {shown['E']} of kinetic energy. What is its mass?"
      return self._payload("kinetic_energy", values, target, question)

  def gravitational_problem(self, difficulty, *, variant=None):
      mass, height, energy = self.gravitational_potential_energy(difficulty)
      values = {"E": energy, "m": mass, "g": 10, "h": height}
      target = self._target(difficulty, variant, ("E", "h", "m"))
      noun = random_noun()
      shown = self._shown("gravitational_energy", values)
      if target == "E":
          question = f"A {shown['m']} {noun} is {shown['h']} above the ground. What is its gravitational potential energy?"
      elif target == "h":
          question = f"A {shown['m']} {noun} has {shown['E']} of gravitational potential energy. How high is it above the ground?"
      else:
          question = f"A {noun} is {shown['h']} above the ground and has {shown['E']} of gravitational potential energy. What is its mass?"
      question += f" Use g = {shown['g']} and take gravitational potential energy to be zero at ground level."
      return self._payload("gravitational_energy", values, target, question)

  def work_problem(self, difficulty, *, variant=None):
      force, distance, work = self.work(difficulty)
      values = {"W": work, "F": force, "d": distance}
      target = self._target(difficulty, variant, ("W", "d", "F"))
      noun = random_noun()
      shown = self._shown("work", values)
      if target == "W":
          question = f"A constant {shown['F']} force moves a {noun} {shown['d']} across flat ground. How much work does this force do?"
      elif target == "d":
          question = f"A constant {shown['F']} force does {shown['W']} of work moving a {noun} across flat ground. How far does it move?"
      else:
          question = f"A constant force does {shown['W']} of work moving a {noun} {shown['d']} across flat ground. What is the force?"
      return self._payload("work", values, target, question)

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
      definitions = (
          ("Elastic Potential Energy", "elastic-potential-energy", "elastic_energy",
           r"${E} = \frac{1}{2}${k}${x}^2",
           r"${E} = \frac{1}{2}${k}${x}^2 \quad,\quad ${k} = \frac{2${E}}{${x}^2} \quad,\quad ${x} = \sqrt{\frac{2${E}}{${k}}}"),
          ("Kinetic Energy", "kinetic-energy", "kinetic_energy",
           r"${E} = \frac{1}{2}${m}${v}^2",
           r"${E} = \frac{1}{2}${m}${v}^2 \quad,\quad ${m} = \frac{2${E}}{${v}^2} \quad,\quad ${v} = \sqrt{\frac{2${E}}{${m}}}"),
          ("Gravitational Potential Energy", "gravitational-potential-energy", "gravitational_energy",
           r"${E} = ${m}${g}${h}",
           r"${E} = ${m}${g}${h} \quad,\quad ${m} = \frac{${E}}{${g}${h}} \quad,\quad ${h} = \frac{${E}}{${m}${g}}"),
          ("Work", "work", "work", r"${W} = ${F}${d}",
           r"${W} = ${F}${d} \quad,\quad ${F} = \frac{${W}}{${d}} \quad,\quad ${d} = \frac{${W}}{${F}}"),
      )
      return {name: {"id": "energy-basics." + identity, "aliases": [name],
                     "honors": equation(profile, main), "conceptual": equation(profile, expanded)}
              for name, identity, profile, main, expanded in definitions}
