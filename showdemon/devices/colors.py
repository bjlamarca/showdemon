
class Colors():
    COLOR_LIST = [
        ('RED', 'Red', (255, 0, 0,)),
        ('GREEN','Green', (0, 255, 0,)),
        ('BLUE', 'Blue', (0, 0, 255,)),
        ('PURPLE', 'Purple', (153, 0, 153)),
        ('ORANGE', 'Orange', (209,32,0)),
        ('PINK','Pink', (255, 192, 203)),
        ('WHITE', 'White', (255, 255, 255)),
    ]

    def get_choices(self):
        choice_dict = {}
        for color in self.COLOR_LIST:
            choice_dict[color[0]] = color[1]
        return choice_dict
    
    def get_rgb(self, name):
        for col in self.COLOR_LIST:
            if col[0] == name:
                return col[2]




if __name__ == '__main__':
    col = Colors()
    #print(str(col.get_choices()))
    print(col.get_rgb('RED'))


        

    
    
