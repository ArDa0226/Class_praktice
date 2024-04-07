
class Road:

    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance

class Warehouse:

    def __init__(self, name, content=0):
        self.name = name
        self.content = content
        self.road_out = None
        self.set_road_out = None
        self.queue_in = []
        self.queue_out = []
    def __str__(self):
        return f'Склад {self.name} груза {self.content}'

    def set_road_out(self, road):
        self.set_road_out = road

    def truck_arrived(self, truck):
        self.queue_in.append(truck)
        print(f'{self.name} прибыл грузовик {truck}')

    def get_next_truck(self):
        if self.queue_in:
            truck = self.queue_out.pop()
            return truck

    def truck_ready(self, truck):
        self.queue_out.append(truck)
        print(f'{self.name} грузовик готов {truck}')
    def act(self):
        while self.queue_out:
            truck = self.queue_out.pop()
            truck.go_to(road=self.road_out)

class Vehicle:
    fuel_rate = 0

    def __init__(self, model):
        self.model = model
        self.fuel = 0


    def __str__(self):
        return f'{self.model, self.fuel} топлива'

    def tank_up(self):
        self.fuel += 1000
        print(f'{self.model} заправился')

class Truck(Vehicle):
    fuel_rate = 50
    def __init__(self, model, body_space = 1000):
        super().__init__(model=model)
        self.body_space = body_space
        self.cargo = 0
        self.velocity = 100
        self.place = None
        self.distance_to_target = 0

    def __str__(self):
        res = super().__str__()
        return res + f'груза {self.cargo}'


    def ride(self):
        self.fuel -= self.fuel_rate
        if self.distance_to_target > self.velocity:
            self.distance_to_target -= self.velocity
            print(f'{self.model} едет по дороге, осталось {self.distance_to_target}')
        else:
            self.place = self.place.end
            self.place.truck_arrrived(self)
            print(f'{self.model} доехал')

    def go_to(self, road):
        self.place = road
        self.distance_to_target = road.distance
        print(f'{self.model} Выехал в путь ')

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
        elif isinstance(self.place, Road):
            self.ride()

class AutoLoader(Vehicle):
    fuel_rate = 30

    def __init__(self, model, bucket_capacity = 100, warehouse = None, role = 'Loader'):
        super().__init__(model=model)
        self.bucket_capacity = bucket_capacity
        self.warehouse = warehouse
        self.role = role
        self.truck = None
    def __str__(self):
        res = super().__str__()
        return res + f'груза {self.truck}'


    def act(self):
       if self.fuel <= 10:
           self.tank_up()
       elif self.truck is None:
           self.truck = self.warehouse.get_next_truck()
           print(f'{self.model} взял в работу {self.truck}')
       elif self.role == 'Loader':
           self.load()
       else:
           self.unload()

    def load(self):
        self.fuel -= self.fuel_rate
        truck_cargo_rest = self.truck.body_space - self.truck.cargo
        if truck_cargo_rest >= self.bucket_capacity:
            self.warehouse.content -= self.bucket_capacity
            self.truck.cargo += self.bucket_capacity
        else:
            self.warehouse.content -= truck_cargo_rest
            self.truck.cargo += truck_cargo_rest
        print(f'{self.model} грузил {self.truck}')
        if self.truck.cargo == self.truck.body_space:
            self.warehouse.truck_ready(self.truck)
            self.truck = None


    def unload(self):
        self.fuel -= self.fuel_rate
        if self.truck.cargo >= self.bucket_capacity:
            self.warehouse.content -= self.bucket_capacity
            self.truck.cargo += self.bucket_capacity
        else:
            self.warehouse.content -= self.truck.cargo
            self.truck.cargo += self.truck.cargo
        print(f'{self.model} разгузил {self.truck}')
        if self.truck.cargo == 0:
            self.warehouse.truck_ready(self.truck)
            self.truck = None

TOTAL_CARGO = 100000

moscow = Warehouse(name='Москва', content=TOTAL_CARGO)
piter = Warehouse(name='Питер', content=0)

moscow_piter = Road(start=moscow, end=piter, distance=715)
piter_moscow = Road(start=piter, end=moscow_piter, distance=780)

moscow.set_road_out(moscow_piter)
piter.set_road_out(piter_moscow)

loader_1 = AutoLoader(model='Bobcat', bucket_capacity=1000, warehouse=moscow, role='Loader')
loader_2 = AutoLoader(model='Lonking', bucket_capacity=500, warehouse=piter, role='Unloader')

truck_1 = Truck(model='Kamaz', body_space=5000)
truck_2 = Truck(model='MAN', body_space=2000)

moscow.truck_arrived(truck_1)
moscow.truck_arrived(truck_2)

hour = 0
while piter.content < TOTAL_CARGO:
    hour += 1
    print(f'-------------------час {hour}----------------------')
    truck_1.act()
    truck_2.act()
    loader_1.act()
    loader_2.act()
    moscow.act()
    piter.act()
    print(truck_1)
    print(truck_2)
    print(loader_1)
    print(loader_2)
    print(moscow)
    print(piter)
