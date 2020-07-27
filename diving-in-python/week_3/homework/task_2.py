import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

class Car(CarBase):
    car_type = 'car'
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)



class Truck(CarBase):
    car_type = 'truck'
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        #self.body_whl = body_whl # надо распарсить на lenth width hight

        whl = body_whl.split('x')

        try:
            if len(whl) != 3:
                raise ValueError
            self.body_length = float(whl[0])
            self.body_width = float(whl[1])
            self.body_height = float(whl[2])
        except:
            self.body_length = self.body_width = self.body_height = float(0)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__( brand, photo_file_name, carrying)
        self.extra = extra



def get_car_list(csv_filename):
    car_list = []
    car_types = ['car', 'truck', 'spec_machine']
    ext = ['.jpg', '.jpeg', '.gif', '.png']
    with open(csv_filename) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) == 7:
                car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = row

                if (car_type in car_types) and brand and photo_file_name and carrying:
                    try:
                        if os.path.splitext(photo_file_name)[1] not in ext:
                            raise ValueError

                        carrying = float(carrying)

                        if carrying <= 0:
                            raise ValueError

                    except ValueError:
                        continue

                    if car_type == 'car' and not body_whl and not extra:
                        try:
                            car_list.append(Car(brand, photo_file_name, carrying, int(passenger_seats_count)))
                        except:
                            continue

                    if car_type == 'truck' and not passenger_seats_count and not extra:
                        try:
                            car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
                        except:
                            continue

                    if car_type == 'spec_machine' and not passenger_seats_count and not body_whl and extra:
                        try:
                            car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
                        except:
                            continue

    return car_list
