class Moon:
    def __init__(self, x_pos, y_pos, z_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

        self.total_energy = 0

    def __repr__(self):
        """
        Implementing this similarly to the example, but not going to
        worry about aligning whitespace with other moons
        """
        pos = f'pos=<x={self.x_pos}, y={self.y_pos}, z={self.z_pos}>'
        vel = f'vel=<x={self.x_vel}, y={self.y_vel}, z={self.z_vel}>'
        return f'{pos}, {vel}'

    def apply_gravity(self, other_moon):
        """
        Update the velocity of self based on the position of other_moon
        
        This does not modify other_moon, which is somewhat less computationally
        efficient but easier to read in my opinion
        """
        if other_moon.x_pos > self.x_pos:
            self.x_vel += 1
        elif other_moon.x_pos < self.x_pos:
            self.x_vel -= 1

        if other_moon.y_pos > self.y_pos:
            self.y_vel += 1
        elif other_moon.y_pos < self.y_pos:
            self.y_vel -= 1

        if other_moon.z_pos > self.z_pos:
            self.z_vel += 1
        elif other_moon.z_pos < self.z_pos:
            self.z_vel -= 1

    def apply_velocity(self):
        """
        Update the position of self based on the velocity of self
        """
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.z_pos += self.z_vel

    def update_total_energy(self):
        """
        Update the overall total energy for this moon, and also return
        the total energy for this step
        """
        potential_energy = abs(self.x_pos) + abs(self.y_pos) + abs(self.z_pos)
        kinetic_energy = abs(self.x_vel) + abs(self.y_vel) + abs(self.z_vel)
        total_energy = potential_energy * kinetic_energy

        self.total_energy = total_energy

        return total_energy


def build_moon_list(input_str):
    moons = input_str.split("\n")
    moon_objs = []
    for moon in moons:
        moon = moon[1:-1]
        x, y, z = moon.split(", ")
        x = int(x[2:])
        y = int(y[2:])
        z = int(z[2:])

        moon_obj = Moon(x, y, z)
        moon_objs.append(moon_obj)
    return moon_objs


def update_all_moons(moons):
    for index, moon in enumerate(moons):
        other_moons = moons.copy()
        other_moons.pop(index)
        for other_moon in other_moons:
            moon.apply_gravity(other_moon)

    for moon in moons:
        moon.apply_velocity()
        moon.update_total_energy()


def run_n_times_and_return_energy(n, input_str):
    moon_list = build_moon_list(input_str)
    for _ in range(n):
        update_all_moons(moon_list)
    total_total_energy = 0
    for moon in moon_list:
        total_total_energy += moon.total_energy
    return total_total_energy

def run_to_find_cycles(input_str):
    moon_list = build_moon_list(input_str)

    moon_1 = moon_list[0]
    moon_2 = moon_list[1]
    moon_3 = moon_list[2]
    moon_4 = moon_list[3]

    moon_1_initial_x = (moon_1.x_pos, moon_1.x_vel)
    moon_2_initial_x = (moon_2.x_pos, moon_2.x_vel)
    moon_3_initial_x = (moon_3.x_pos, moon_3.x_vel)
    moon_4_initial_x = (moon_4.x_pos, moon_4.x_vel)

    moon_1_initial_y = (moon_1.y_pos, moon_1.y_vel)
    moon_2_initial_y = (moon_2.y_pos, moon_2.y_vel)
    moon_3_initial_y = (moon_3.y_pos, moon_3.y_vel)
    moon_4_initial_y = (moon_4.y_pos, moon_4.y_vel)

    moon_1_initial_z = (moon_1.z_pos, moon_1.z_vel)
    moon_2_initial_z = (moon_2.z_pos, moon_2.z_vel)
    moon_3_initial_z = (moon_3.z_pos, moon_3.z_vel)
    moon_4_initial_z = (moon_4.z_pos, moon_4.z_vel)

    x_repeat_step = None
    y_repeat_step = None
    z_repeat_step = None

    step = 0

    while True:
        step += 1

        moon_1.apply_gravity(moon_2)
        moon_1.apply_gravity(moon_3)
        moon_1.apply_gravity(moon_4)

        moon_2.apply_gravity(moon_1)
        moon_2.apply_gravity(moon_3)
        moon_2.apply_gravity(moon_4)

        moon_3.apply_gravity(moon_1)
        moon_3.apply_gravity(moon_2)
        moon_3.apply_gravity(moon_4)

        moon_4.apply_gravity(moon_1)
        moon_4.apply_gravity(moon_2)
        moon_4.apply_gravity(moon_3)

        moon_1.apply_velocity()
        moon_2.apply_velocity()
        moon_3.apply_velocity()
        moon_4.apply_velocity()

        if (x_repeat_step == None and
                (moon_1.x_pos, moon_1.x_vel) == moon_1_initial_x and
            (moon_2.x_pos, moon_2.x_vel) == moon_2_initial_x and
            (moon_3.x_pos, moon_3.x_vel) == moon_3_initial_x and
                (moon_4.x_pos, moon_4.x_vel) == moon_4_initial_x):
            x_repeat_step = step

        if (y_repeat_step == None and
            (moon_1.y_pos, moon_1.y_vel) == moon_1_initial_y and
            (moon_2.y_pos, moon_2.y_vel) == moon_2_initial_y and
            (moon_3.y_pos, moon_3.y_vel) == moon_3_initial_y and
                (moon_4.y_pos, moon_4.y_vel) == moon_4_initial_y):
            y_repeat_step = step

        if (z_repeat_step == None and
            (moon_1.z_pos, moon_1.z_vel) == moon_1_initial_z and
            (moon_2.z_pos, moon_2.z_vel) == moon_2_initial_z and
            (moon_3.z_pos, moon_3.z_vel) == moon_3_initial_z and
                (moon_4.z_pos, moon_4.z_vel) == moon_4_initial_z):
            z_repeat_step = step

        if x_repeat_step != None and y_repeat_step != None and z_repeat_step != None:
            break
    import math
    x_y_lcm = (x_repeat_step *
               y_repeat_step) // math.gcd(x_repeat_step, y_repeat_step)
    x_y_z_lcm = (x_y_lcm * z_repeat_step) // math.gcd(x_y_lcm, z_repeat_step)
    return x_y_z_lcm
