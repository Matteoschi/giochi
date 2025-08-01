import random

# Definizione dei livelli di difficoltà
livelli = [
    {"soglia": 500, "velocità": 6, "spawn_min": 150, "spawn_max": 250},
    {"soglia": 1500, "velocità": random.randint(6, 8), "spawn_min": 100, "spawn_max": 180},
    {"soglia": 2000, "velocità": random.randint(8, 10), "spawn_min": 100, "spawn_max": 150},
    {"soglia": 2500, "velocità": random.randint(10, 12), "spawn_min": random.randint(60, 100), "spawn_max": random.randint(125, 150)},
    {"soglia": 3500, "velocità": random.randint(12, 14), "spawn_min": random.randint(50, 60), "spawn_max": random.randint(70, 100)}
]
