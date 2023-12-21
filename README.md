# Genderify Sweden

This code is the implementation of an attempt to guess the gender of a first name by using public name statistics from the Swedish statistical agency (*Statistiska centralbyrån, SCB*).

## What does it do?

The file [generate_ratios.py](generate_ratios.py) processes the statistics and creates the [gender.json](gender.json) by calculating a female/(male + female) ratio of the people bearing each names in Sweden.

That file can then be reused using the [Genderify](genderify.py) methods .gender() and ratio() to guess the gender of a single name or calculate the gender balance of a larger population of people (see **How to use**).

## Installation

- Install Python 3 on your machine if you don't already have it.

- Install the dependencies

```python
pip install -r requirements.txt
```

## How to use

 Import ***genderify*** and use one of its functions

```python
from genderify import Genderify

# An instance of the class should be initialised once to load the name list.
genderify = Genderify('gender.json')

# Once that is done, use the gender(name) function to get a gender guess.
print(f'The gender of "Pierre" is {genderify.gender("Pierre")}.')

# You can also change the ratio above which the function returns A (for ambiguous).
# By default, the value is set to 2%.
print(f'The gender of "Pierre" is {genderify.gender("Pierre", 0.1)}.')

# If you prefer get the raw ratio to calculate the gender of a large population,
# you can call the ratio(name) function.
print(f'The gender ratio of "Pierre" is {genderify.ratio("Pierre")}.')
```
