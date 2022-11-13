class HashMap:
    def __init__(self, capacity=10):
        self.map = []
        for i in range(capacity):
            self.map.append([])

    def hashing_function(self, key):
        bucket = int(key) % len(self.map)
        return bucket

    def insert(self, key, value):
        hash_key = self.hashing_function(key)
        pair = [key, value]
        if self.map[hash_key] is None:
            self.map[hash_key] = list([pair])
        else:
            for i in self.map[hash_key]:    # collisions handled through chaining
                if i[0] == key:
                    i[1] = pair
            self.map[hash_key].append(pair)

    def get(self, key):
        hash_key = self.hashing_function(key)
        if self.map[hash_key] is not None:
            for p in self.map[hash_key]:
                if p[0] == key:
                    return p[1]
        return None

    def get_id(self, key):
        x = self.get(key)
        return x.id

    def get_address(self, key):
        x = self.get(key)
        return x.address

    def get_deadline(self, key):
        x = self.get(key)
        return x.deadline

    def get_city(self, key):
        x = self.get(key)
        return x.city

    def get_state(self, key):
        x = self.get(key)
        return x.state

    def get_zip(self, key):
        x = self.get(key)
        return x.zip

    def get_weight(self, key):
        x = self.get(key)
        return x.weight

    def get_location(self, key):
        x = self.get(key)
        return x.location

    def get_delivery_time(self, key):
        x = self.get(key)
        return x.delivery_time

    def get_note(self, key):
        x = self.get(key)
        return x.note

    def get_time_seconds(self, key):
        x = self.get(key)
        return x.time_seconds
