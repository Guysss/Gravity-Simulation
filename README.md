## Gravity simulation

This is a simulation of gravity that I made to train me. This program is based on **Newton's Second Law**.

You can change defaults values if you want to have more fun with :
- ```G``` : The gravitational constant is the strengh of the gravitational force between objects.
- ```OBJECTS_NUM``` : The number of objects that will be spawn in the simulation.
- ```DENSITY``` : The density of objects, it will influence their size according to their mass.
- ```BOUNCE``` : The object will bounce on edges.

The mass of each objects is randomly defined in the ```__init__()``` function of *Object()* class.

> [!NOTE]
> If you change one of the default values, I recommend you to change other values too and try to adjust them to get a coherent simulation.

Finally, if the size of the void is too small you can change it in ```WIDTH``` and ```HEIGHT```.

> [!WARNING]
> If you don't have the pygame library, type ```pip3 install pygame``` on Linux or ```python3 -m pip install pygame``` on Windows.

- Guys_s