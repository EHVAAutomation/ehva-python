# ehva-python 0.0.3
A package to integrate python scripts to the [EHVA App](https://ehva.ca).

## Requirements
python 3

## Installation
`pip install ehva`

## Usage
```python
from ehva import python_engine
import numpy as np

""" Parse inputs and convert into desired types """
data = python_engine.parse_inputs()

a = float(data["a"])
b = float(data["b"])
c = float(data["c"])

""" Perform task: solving quadratic equation """
x1 = -b - np.sqrt(b**2 - 4*a*c)/2/a
x2 = -b + np.sqrt(b**2 - 4*a*c)/2/a

""" Create output dictionary and send back to Ehva App """
outputs = {
    "solution1" : x1,
    "solution2" : x2,
    }

python_engine.send_outputs(outputs)

```
