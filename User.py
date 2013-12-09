import json
from TurnstileStepper_generated import Stepper


s = Stepper()

sampleInput = json.load(open("./sample_input.json", "r"))

while sampleInput:
    input = sampleInput.pop(0)
    s.step(input)

