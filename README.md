# phecs

![Icon](phecs_logo_small.png)

## What is it?
PHECS is an ecs with an api like hecs, but for python python-hecs. 
Pronounced 'fecs' as in, what the phecs wrong with you.

## Why was it made?

Most ECS libraries come with processor or system abstractions, or require some component registration boilerplate. 
We needed a library that feels like it was made for python. Normal iteration, normal functions as systems.
HECS, in Rust, does a good job of this, but has some funky query syntax that would look really weird in python.
This is a near direct port of the api surface of HECS, but with a pythonic api.

## But why should I use it?

Has the following advantages:

- Lets you declare your assets in the same place as the paths (no more dictionary of mappings).
- Uses an enum as the base type for your assets (instead of strings). This means your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor may also detect asset name typos. (thank you)
- Has a preload feature to warm the cache.
- Is already written.
- Is only like 100 lines of code. (Hackable, Grokkable.)

## How do?

### Installation

1. Install

   ```bash
   pip install phecs
   ```

2. Import

   ```python
   from phecs import {
       World,
       Entity
   }
   ```

### 1. Define Components

First, define some components.
In Phecs, any class is a component. You do not need to decorate them or subclass anything.

```python
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class Health:
    def __init__(self, hp):
        self.hp = hp

class Burning:
    pass

class Dead:
    pass
```

### 2. Make Your World, and Fill It With Entities

Create a world and spawn some entities with components.

```python
# Create a world
world = World()

# Create an entity with some components
entity = world.spawn(Position(0, 0), Velocity(1, 1), Health(100))
world.add_component(entity, Burning()) # add another component later
```

world.spawn is variadic, so you can add as many components as you want, or just one, or none at all.

```python
world = World()
world.spawn(Position(0, 0), Velocity(1, 1), Health(100))
world.spawn(Position(1, 1))
world.spawn()
```

### 3. Define Systems

Define some systems. In Phecs, a system is any function that operates on the world.

```python
def physics(world):
    for entity, position, velocity in world.find(Position, Velocity):
        position.x += velocity.dx
        position.y += velocity.dy

def burn(world):
    for entity, health, burning in world.find(Health, Burning):
        health.hp -= 1

def die_if_dead(world):
    for entity, health in world.find(Health):
        if health.hp <= 0:
            world.insert(entity, Dead())
```

### 4. Run Systems

Run the systems in your game loop.

```python
while True:
    physics(world)
    burn(world)
    die_if_dead(world)
draw(graphics_context, world)
```


## Handy Features

### Filter Queries

In a find query entities can be filtered by components.

```python
for entity, position, velocity in world.find(Position, Velocity, without=Dead):
    pass

for entity, position, velocity in world.find(Position, Velocity, has=Health):
    pass
```

Get complicated with it.

```python
for entity, position, velocity in world.find(Position, Velocity, has=(Player, Burning), without=Dead):
    pass
```

## See Also
Documentation at: www.link_to_documentation.com
```