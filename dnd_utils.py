class DndUtils:
    def get_stat_mod(stat_value):
        match stat_value:
            case stat_value if stat_value == 1:
                return f'{stat_value} (-5)'
            case stat_value if stat_value in range(2, 4):
                return f'{stat_value} (-4)'
            case stat_value if stat_value in range(4, 6):
                return f'{stat_value} (-3)'
            case stat_value if stat_value in range(6, 8):
                return f'{stat_value} (-2)' 
            case stat_value if stat_value in range(8, 10):
                return f'{stat_value} (-1)' 
            case stat_value if stat_value in range(10, 12):
                return f'{stat_value} (+0)' 
            case stat_value if stat_value in range(12, 14):
                return f'{stat_value} (+1)' 
            case stat_value if stat_value in range(14, 16):
                return f'{stat_value} (+2)' 
            case stat_value if stat_value in range(16, 18):
                return f'{stat_value} (+3)' 
            case stat_value if stat_value in range(18, 20):
                return f'{stat_value} (+4)' 
            case stat_value if stat_value in range(20, 22):
                return f'{stat_value} (+5)' 
            case stat_value if stat_value in range(22, 24):
                return f'{stat_value} (+6)' 
            case stat_value if stat_value in range(24, 26):
                return f'{stat_value} (+7)' 
            case stat_value if stat_value in range(26, 28):
                return f'{stat_value} (+8)' 
            case stat_value if stat_value in range(28, 30):
                return f'{stat_value} (+9)' 
            case stat_value if stat_value == 30:
                return f'{stat_value} (+10)' 
