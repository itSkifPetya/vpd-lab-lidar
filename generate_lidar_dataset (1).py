import numpy as np
import json
import math

class LiDAR2DSimulator:
    def __init__(self):
        # Параметры HOKUYO URG-04LX-UG01
        self.max_range = 5600  # мм
        self.min_range = 60    # мм
        self.angle_resolution = 0.36  # градусы
        self.scan_angle = 240  # градусы
        self.num_points = int(self.scan_angle / self.angle_resolution)
        
    def create_simple_room(self, robot_x=0, robot_y=0, robot_theta=0):
        """Создает простую прямоугольную комнату 8x6 метров"""
        points = []
        
        for i in range(self.num_points):
            angle_deg = -120 + i * self.angle_resolution  # от -120° до +120°
            angle_rad = math.radians(angle_deg + robot_theta)
            
            # Луч от робота
            ray_x = math.cos(angle_rad)
            ray_y = math.sin(angle_rad)
            
            # Стены комнаты (8x6 метров, робот в центре)
            walls = [
                # Правая стена (x = 4000)
                (4000 - robot_x, ray_x, 'vertical'),
                # Левая стена (x = -4000) 
                (-4000 - robot_x, ray_x, 'vertical'),
                # Верхняя стена (y = 3000)
                (3000 - robot_y, ray_y, 'horizontal'),
                # Нижняя стена (y = -3000)
                (-3000 - robot_y, ray_y, 'horizontal')
            ]
            
            min_distance = self.max_range
            
            for wall_pos, ray_component, wall_type in walls:
                if wall_type == 'vertical' and ray_x != 0:
                    t = wall_pos / ray_component
                    if t > 0:
                        distance = t * 1000  # в мм
                        if distance < min_distance:
                            min_distance = distance
                            
                elif wall_type == 'horizontal' and ray_y != 0:
                    t = wall_pos / ray_component
                    if t > 0:
                        distance = t * 1000  # в мм
                        if distance < min_distance:
                            min_distance = distance
            
            # Добавляем шум (±30мм как у реального датчика)
            noise = np.random.normal(0, 20)
            distance = max(self.min_range, min(self.max_range, min_distance + noise))
            
            # # Преобразуем в декартовы координаты
            # x = robot_x + (distance / 1000) * math.cos(angle_rad)
            # y = robot_y + (distance / 1000) * math.sin(angle_rad)
            
            points.append([angle_deg, distance])
            
        return points

    def create_room_with_obstacles(self, robot_x=0, robot_y=0, robot_theta=0):
        """Комната с препятствиями (столы, стулья)"""
        points = []
        
        # Препятствия в комнате
        obstacles = [
            {'x': 1.5, 'y': 1.0, 'radius': 0.3},  # Круглый стол
            {'x': -1.0, 'y': -1.5, 'radius': 0.2}, # Стул
            {'x': 2.0, 'y': -2.0, 'radius': 0.15}, # Другой стул
        ]
        
        for i in range(self.num_points):
            angle_deg = -120 + i * self.angle_resolution
            angle_rad = math.radians(angle_deg + robot_theta)
            
            ray_x = math.cos(angle_rad)
            ray_y = math.sin(angle_rad)
            
            min_distance = self.max_range
            
            # Проверяем стены комнаты
            walls = [
                (4000 - robot_x * 1000, ray_x, 'vertical'),
                (-4000 - robot_x * 1000, ray_x, 'vertical'),
                (3000 - robot_y * 1000, ray_y, 'horizontal'),
                (-3000 - robot_y * 1000, ray_y, 'horizontal')
            ]
            
            for wall_pos, ray_component, wall_type in walls:
                if wall_type == 'vertical' and ray_x != 0:
                    t = wall_pos / ray_component / 1000
                    if t > 0:
                        distance = t * 1000
                        if distance < min_distance:
                            min_distance = distance
                            
                elif wall_type == 'horizontal' and ray_y != 0:
                    t = wall_pos / ray_component / 1000
                    if t > 0:
                        distance = t * 1000
                        if distance < min_distance:
                            min_distance = distance
            
            # Проверяем препятствия
            for obs in obstacles:
                # Расстояние от робота до центра препятствия
                dx = obs['x'] - robot_x
                dy = obs['y'] - robot_y
                
                # Проекция на луч
                dot = dx * ray_x + dy * ray_y
                if dot > 0:  # Препятствие впереди
                    # Расстояние от луча до центра препятствия
                    cross_dist = abs(dx * ray_y - dy * ray_x)
                    
                    if cross_dist <= obs['radius']:
                        # Луч пересекает препятствие
                        chord_half = math.sqrt(obs['radius']**2 - cross_dist**2)
                        intersection_dist = (dot - chord_half) * 1000
                        
                        if intersection_dist > 0 and intersection_dist < min_distance:
                            min_distance = intersection_dist
            
            # Добавляем шум
            noise = np.random.normal(0, 20)
            distance = max(self.min_range, min(self.max_range, min_distance + noise))
            
            # x = robot_x + (distance / 1000) * math.cos(angle_rad)
            # y = robot_y + (distance / 1000) * math.sin(angle_rad)
            
            points.append([angle_deg, distance])      
        return points

def generate_movement_sequence():
    """Генерирует последовательность движений робота"""
    simulator = LiDAR2DSimulator()
    
    # Сценарий 1: Простое движение вперед
    sequence1 = []
    for i in range(10):
        x = i * 0.2  # движение по 20см
        scan = simulator.create_simple_room(robot_x=x, robot_y=0, robot_theta=0)
        sequence1.append({
            'timestamp': i * 0.1,  # каждые 100мс
            'robot_pose': {'x': x, 'y': 0, 'theta': 0},
            'scan': scan
        })
    
    # Сценарий 2: Поворот на месте
    sequence2 = []
    for i in range(15):
        theta = i * 3  # поворот по 3 градуса
        scan = simulator.create_room_with_obstacles(robot_x=0, robot_y=0, robot_theta=theta)
        sequence2.append({
            'timestamp': i * 0.1,
            'robot_pose': {'x': 0, 'y': 0, 'theta': theta},
            'scan': scan
        })
    
    # Сценарий 3: Сложная траектория (L-образный поворот)
    sequence3 = []
    waypoints = [
        (0, 0, 0), (0.5, 0, 0), (1.0, 0, 0), (1.5, 0, 0),  # вперед
        (1.5, 0, 15), (1.5, 0, 30), (1.5, 0, 45), (1.5, 0, 60), (1.5, 0, 90),  # поворот
        (1.5, 0.3, 90), (1.5, 0.6, 90), (1.5, 0.9, 90)  # вперед после поворота
    ]
    
    for i, (x, y, theta) in enumerate(waypoints):
        scan = simulator.create_room_with_obstacles(robot_x=x, robot_y=y, robot_theta=theta)
        sequence3.append({
            'timestamp': i * 0.1,
            'robot_pose': {'x': x, 'y': y, 'theta': theta},
            'scan': scan
        })
    
    return {
        'scenario_1_forward_motion': sequence1,
        'scenario_2_rotation': sequence2,
        'scenario_3_complex_path': sequence3
    }

if __name__ == "__main__":
    print("Генерирую датасет LiDAR...")
    
    dataset = generate_movement_sequence()
    
    # Сохраняем в JSON файлы
    for scenario_name, data in dataset.items():
        filename = f"data/lidar_data_{scenario_name}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Сохранен {filename} с {len(data)} сканами")
    
    # Создаем также отдельные файлы для быстрого тестирования
    sim = LiDAR2DSimulator()
    
    # Один скан из простой комнаты
    scan1 = sim.create_simple_room(0, 0, 0)
    with open('data/single_scan_room.json', 'w') as f:
        json.dump(scan1, f, indent=2)
    
    # Тот же скан, но робот слегка сдвинут (для тестирования ICP)
    scan2 = sim.create_simple_room(0.1, 0.05, 2)  # сдвиг 10см, 5см, поворот 2°
    with open('data/single_scan_moved.json', 'w') as f:
        json.dump(scan2, f, indent=2)
    
    print("\nДополнительно созданы:")
    print("- single_scan_room.json (базовый скан)")
    print("- single_scan_moved.json (тот же скан после небольшого движения)")
    print(f"\nКаждый скан содержит {len(scan1)} точек")
    print("Формат данных: angle_deg, distance_mm, x_m, y_m")