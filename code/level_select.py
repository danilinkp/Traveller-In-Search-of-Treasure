class TravelGuide:
    def __init__(self):
        self.current_level = 1
        self.levels_open = {'1 ': 'Open', '2': 'close'}

    def update_current_level(self, level_id):
        self.current_level = level_id

    def return_map(self):
        if self.current_level == 1:
            return 'maps/level.tmx'

        if self.current_level == 2:
            return 'maps/level2.tmx'
        if self.current_level == 3:
            return 'maps/level3.tmx'

        if self.current_level == 4:
            return 'maps/level4.tmx'
        if self.current_level == 5:
            return 'maps/level5.tmx'

        if self.current_level == 6:
            return 'maps/level6.tmx'

    def return_hero_coords(self):
        if self.current_level == 1:
            return 10 * 32, 15 * 32
        if self.current_level == 2:
            return 10 * 32, 15 * 32
        if self.current_level == 3:
            return 10 * 32, 15 * 32
        if self.current_level == 4:
            return 10 * 32, 15 * 32
        if self.current_level == 5:
            return 10 * 32, 15 * 32
        if self.current_level == 6:
            return 10 * 32, 15 * 32



    def return_coins_coords(self):
        if self.current_level == 1:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
        if self.current_level == 2:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
        if self.current_level == 3:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
        if self.current_level == 4:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
        if self.current_level == 5:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
        if self.current_level == 6:
            return [[[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]], [[10 * 32, 15 * 32]]]
    def return_enemy_coords(self):
        if self.current_level == 1:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]
        if self.current_level == 2:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]
        if self.current_level == 3:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]
        if self.current_level == 4:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]
        if self.current_level == 5:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]
        if self.current_level == 6:
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32]

    def return_constrains_coords(self):
        if self.current_level == 1:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        if self.current_level == 2:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        if self.current_level == 3:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        if self.current_level == 4:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        if self.current_level == 5:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        if self.current_level == 6:
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]

    def return_scroll_x(self):
        if self.current_level == 1:
            return -370 * 2
        if self.current_level == 2:
            return -450 * 2
        if self.current_level == 3:
            return -370 * 2
        if self.current_level == 4:
            return -400 * 2
        if self.current_level == 5:
            return -370 * 2
        if self.current_level == 6:
            return -450 * 2



    def change_dict(self, id):
        self.levels_open[id] = 'Open'
