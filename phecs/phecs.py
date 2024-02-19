from __future__ import annotations

from enum import Enum, auto
from typing import Any, Dict, Iterator, List, Optional, Tuple, Type


class Error(Enum):
    NoSuchEntity = auto()
    NoSuchComponent = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class NoSuchEntity(Exception):
    pass


class NoSuchComponent(Exception):
    pass


class Entity:
    def __init__(self, id):
        self.__id = id

    def __hash__(self) -> int:
        return hash(self.__id)

    def __repr__(self) -> str:
        return f"Entity(id={self.__id})"

    def __eq__(self, other_entity: Entity) -> bool:
        return self.__id == other_entity.__id


class InternalEntity:
    def __init__(self, entity: Entity):
        self.entity: Entity = entity
        self.components: dict[Type[Any], Any] = {}


"""
Naming Guide for if you really must shorten a variable in a comprehension or something:
e = entity
ie = internal_entity
es = entities
c = component
cs = components
"""


class World:
    def __init__(self) -> None:
        self.next_entity_id: int = 0
        self.entities: Dict[Entity, InternalEntity] = {}

    def spawn(self, *components: Tuple[Any, ...]) -> Entity:
        entity = Entity(self.next_entity_id)
        self.next_entity_id += 1
        internal_entity = InternalEntity(entity)
        self.entities[entity] = internal_entity
        for component in components:
            internal_entity.components[type(component)] = component
        return entity

    def spawn_at(self, entity: Entity, *components: Tuple[Any, ...]) -> None:
        internal_entity = InternalEntity(entity)
        self.entities[entity] = internal_entity
        for component in components:
            internal_entity.components[type(component)] = component

    def despawn(self, entity: Entity) -> Optional[Error]:
        if entity in self.entities:
            del self.entities[entity]
        else:
            return Error.NoSuchEntity

    def clear(self) -> None:
        self.entities.clear()

    def contains(self, entity: Entity) -> bool:
        return entity in self.entities

    def find(
        self,
        *component_types: Type,
        has: Optional[Type | List[Type]] | Tuple[Type, ...] = None,
        without: Optional[Type | List[Type]] | Tuple[Type, ...] = None,
    ) -> Iterator[Tuple[Entity, Tuple[Any, ...]]]:
        has = (
            has
            if isinstance(has, (list, tuple))
            else [has]
            if has is not None
            else None
        )
        without = (
            without
            if isinstance(without, (list, tuple))
            else [without]
            if without is not None
            else None
        )

        for internal_entity in self.entities.values():
            if has and any(c not in internal_entity.components for c in has):
                continue
            if without and any(c in internal_entity.components for c in without):
                continue
            if all(c in internal_entity.components for c in component_types):
                yield (
                    internal_entity.entity,
                    tuple(internal_entity.components[c] for c in component_types),
                )

    def find_on(
        self,
        entity: Entity,
        *component_types: Type,
        has: Optional[Type | List[Type] | Tuple[Type, ...]] = None,
        without: Optional[Type | List[Type] | Tuple[Type, ...]] = None,
    ) -> Optional[tuple[Entity, Tuple[Any, ...]]]:
        if entity not in self.entities:
            return None
        internal_entity = self.entities[entity]

        if has:
            if isinstance(has, (list, tuple)):
                if any(c not in internal_entity.components for c in has):
                    return None
            elif has not in internal_entity.components:
                return None

        if without:
            if isinstance(without, (list, tuple)):
                if any(c in internal_entity.components for c in without):
                    return None
            elif without in internal_entity.components:
                return None

        if all(c in internal_entity.components for c in component_types):
            return (
                internal_entity.entity,
                tuple(internal_entity.components[c] for c in component_types),
            )

        return None

    def get(self, entity: Entity, component_type: Type) -> Any | None:
        if (
            entity in self.entities
            and component_type in self.entities[entity].components
        ):
            return self.entities[entity].components[component_type]
        return None

    def satisfies(
        self,
        entity: Entity,
        has: Optional[Type | List[Type]] | Tuple[Type, ...] = None,
        without: Optional[Type | List[Type]] | Tuple[Type, ...] = None,
    ) -> bool:
        if entity not in self.entities:
            return False
        internal_entity = self.entities[entity]

        if has:
            if isinstance(has, (list, tuple)):
                if any(c not in internal_entity.components for c in has):
                    return False
            elif has not in internal_entity.components:
                return False

        if without:
            if isinstance(without, (list, tuple)):
                if any(c in internal_entity.components for c in without):
                    return False
            elif without in internal_entity.components:
                return False

        return True

    def insert(self, entity: Entity, *components: Tuple[Any, ...]) -> None | Error:
        if entity in self.entities:
            for component in components:
                self.entities[entity].components[type(component)] = component
        else:
            return Error.NoSuchEntity

    def remove(self, entity: Entity, *component_types: Tuple[Any, ...]) -> None:
        if entity in self.entities:
            internal_entity = self.entities[entity]
            for component_type in component_types:
                if component_type in internal_entity.components:
                    del internal_entity.components[component_type]

    def take(self, entity: Entity) -> tuple:
        if entity in self.entities:
            internal_entity = self.entities[entity]
            components = tuple(internal_entity.components.values())
            self.despawn(entity)
            return components
        return ()

    def iter(self) -> Iterator[Entity]:
        for _, internal_entity in self.entities.items():
            yield internal_entity.entity
