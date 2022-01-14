class TravelGuide:
    def __init__(self):
        self.current_level = 1
        self.levels_open = {1: 'open',
                            2: 'open',
                            3: 'close',
                            4: 'close',
                            5: 'close',
                            6: 'close'
                            }

    def update_current_level(self, level_id):
        self.current_level = level_id

    def check_open_level(self, id):
        if self.levels_open[id] == 'close':
            return False
        return True

    def update_current_level_pluse(self):
        self.current_level += 1
        self.levels_open[self.current_level] = 'open'


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
            return 13 * 32, 13 * 32
        if self.current_level == 3:
            return 10 * 32, 15 * 32
        if self.current_level == 4:
            return 10 * 32, 15 * 32
        if self.current_level == 5:
            return 10 * 32, 15 * 32
        if self.current_level == 6:
            return 10 * 32, 10 * 32

    def return_coins_coords(self):
        if self.current_level == 1:
            return [
                [[39 * 32, 13 * 32], [47 * 32, 15 * 32], [50 * 32, 15 * 32],
                 [55 * 32, 15 * 32], [59 * 32, 15 * 32], [76 * 32, 11 * 32],
                 [86 * 32, 9 * 32], [100 * 32, 11 * 32], [104 * 32, 11 * 32]],
                [[49 * 32, 5 * 32], [60 * 32, 7 * 32], [82 * 32, 9 * 32]],
                [[39 * 32, 4 * 32], [90 * 32, 7 * 32]],
                [[95 * 32, 9 * 32], [68 * 32, 10 * 32]]]
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
            return [58 * 32, 16 * 32], [48 * 32, 6 * 32], [67 * 32, 11 * 32], [40 * 32, 5 * 32], \
                   [109 * 32, 12 * 32], [102 * 32, 12 * 32]
        if self.current_level == 2:
            return [53 * 32, 13 * 32], [62 * 32, 13 * 32], [79 * 32, 16 * 32], [73 * 32, 16 * 32]
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
            return [(55 * 32, 6 * 32), (46 * 32, 6 * 32),
                    (54 * 32, 16 * 32), (61 * 32, 16 * 32),
                    (64 * 32, 11 * 32), (73 * 32, 11 * 32),
                    (37 * 32, 5 * 32), (44 * 32, 5 * 32),
                    (98 * 32, 12 * 32), (111 * 32, 12 * 32)
                    ]
        if self.current_level == 2:
            return [(49 * 32, 13 * 32), (65 * 32, 13 * 32), (71 * 32, 16 * 32), (87 * 32, 16 * 32)]
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

    def return_mobs_damage_type_id(self):
        if self.current_level == 1:
            return 1, 20
        if self.current_level == 2:
            return 2, 40
        if self.current_level == 3:
            return 1, 60
        if self.current_level == 4:
            return 1, 80
        if self.current_level == 5:
            return 1, 80
        if self.current_level == 6:
            return 1, 100

    def change_dict(self, id):
        self.levels_open[id] = 'Open'
