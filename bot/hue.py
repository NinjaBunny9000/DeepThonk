from phue import Bridge
from pprint import pprint as pp

class Hue(Bridge):

    def __init__(self, bridge_ip, *args, **kwargs):
        super(Hue, self).__init__(*args, **kwargs)


hue = Hue('192.168.0.190')
# pp(hue.get_api())  #! debug

lights = hue.get_group(4, 'lights')

pp(lights)

group = {
    'studio': 9,
    'living_room': 4
}

for l in lights:
    print(l)
    hue.set_light(int(l), 'on', False)
    # hue.set_light(int(l), 'bri', 0)
