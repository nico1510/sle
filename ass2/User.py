import json
from TurnstileStepper_generated import Stepper

# this module uses the generated python Code

s = Stepper()

sampleInput = json.load(open("./sample_input.json", "r"))

while sampleInput:
    input = sampleInput.pop(0)
    s.step(input)

