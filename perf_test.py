import timeit
from phecs.phecs import World


# Define multiple component classes
class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, vx=0.0, vy=0.0):
        self.vx = vx
        self.vy = vy


class Health:
    def __init__(self, hp=100):
        self.hp = hp


class AIControl:
    def __init__(self, state="idle"):
        self.state = state


# Create entities with a mix of components to simulate a real-world scenario
def create_mixed_entities(world, n):
    for i in range(n):
        components = []
        if i % 2 == 0:
            components.append(Position(x=i, y=-i))
            components.append(Velocity(vx=i * 0.1, vy=-i * 0.1))
        if i % 3 == 0:
            components.append(Health(hp=100 - i))
        if i % 5 == 0:
            components.append(AIControl(state="wander" if i % 2 == 0 else "attack"))
        world.spawn(*components)


# Update entities with Position and Velocity components
def update_position_velocity(world):
    for _, pos, vel in world.find(Position, Velocity):
        pos.x += vel.vx
        pos.y += vel.vy


# Heal entities with Health components
def heal_entities(world):
    for _, health in world.find(Health):
        health.hp += 5


# Change AI state for entities with AIControl component
def update_ai_state(world):
    for _, ai in world.find(AIControl):
        ai.state = "idle" if ai.state != "idle" else "active"


# Delete all entities
def delete_entities(world):
    for entity in list(world.iter()):
        world.despawn(entity)


# Number of entities to test with
N = 5000

# Create world instance
world = World()

# Performance measurement
create_time = timeit.timeit(lambda: create_mixed_entities(world, N), number=1)
update_pos_vel_time = timeit.timeit(lambda: update_position_velocity(world), number=1)
heal_time = timeit.timeit(lambda: heal_entities(world), number=1)
update_ai_time = timeit.timeit(lambda: update_ai_state(world), number=1)
delete_time = timeit.timeit(
    lambda: delete_entities(world), number=1
)  # Use delete_entities from previous example

# Output the timings
print(f"Creation of {N} mixed entities: {create_time:.4f} seconds")
print(f"Update of Position and Velocity: {update_pos_vel_time:.4f} seconds")
print(f"Heal entities: {heal_time:.4f} seconds")
print(f"Update AI state: {update_ai_time:.4f} seconds")
print(f"Deletion of {N} entities: {delete_time:.4f} seconds")
