from genderify import Genderify

genderify = Genderify('gender.json')

print(f'The gender of "Pierre" is {genderify.gender("Pierre")}.')
print(f'The gender ratio of "Pierre" is {genderify.ratio("Pierre")}.')
