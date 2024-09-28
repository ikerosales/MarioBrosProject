
from constants import Constants

class Number:
    """
    class for numbers for the time countdown and coins
    """

    def __init__(self, numb: int, x: int, y: int):
        self.__figure = numb
        # coordinates in the pyxres file
        x_image_numbers = Constants.NUMBERS_FIGURES_X_POSITION
        x_pyxres = x_image_numbers[numb]
        y = y
        # depending on the figure it has one image associated and a position
        self.sprite = [x, y, 2, x_pyxres, 0, 16, 16]

    @property
    def figure(self):
        return self.__figure
    @figure.setter
    def figure(self, new_numb):
        self.__figure = new_numb

    def change_sprite(self):
        """
        changes the image of each number according to its new figure
        """
        x_image_numbers = Constants.NUMBERS_FIGURES_X_POSITION
        x_pyxres = x_image_numbers[self.figure]
        # depending on the figure it has one image associated and a position
        self.sprite[3] = x_pyxres

    def change_value_time(unit_time, tenths_time, hundredths_time):
        """
        acts as a countdown
        """
        if unit_time.figure == 0:
            unit_time.figure = 9
            if tenths_time.figure == 0:
                tenths_time.figure = 9
                hundredths = hundredths_time.figure - 1
                hundredths_time.figure = hundredths
            else:
                tenths = tenths_time.figure - 1
                tenths_time.figure = tenths
        else:
            units = unit_time.figure - 1
            unit_time.figure = units

        # now we change the image associated with each figure in time
        unit_time.change_sprite()
        tenths_time.change_sprite()
        hundredths_time.change_sprite()

    def change_value_coin_counter(unit_coins, tenths_coins):
        """
        adds a value
         """
        if unit_coins.figure == 9:
            unit_coins.figure = 0
            tenths = tenths_coins.figure
            tenths_coins.figure = tenths + 1
        else:
            unit = unit_coins.figure
            unit_coins.figure = unit + 1


        # now we change the image associated with each figure for the coin counter
        unit_coins.change_sprite()
        tenths_coins.change_sprite()


    def score_counter_update(score: int, score_numbers: list):
        """
        this will change the numbers on the screen according to the new score
        """
        # abcdef
        # a-> centenas de millar
        # b-> decenas de millar
        # c-> millar
        # d-> centenas
        # e-> decenas
        # f-> unidades
        if score < 0:
            score = 0

        a = score // 100000
        score -= a * 100000
        b = score // 10000
        score -= b * 10000
        c = score // 1000
        score -= c * 1000
        d = score // 100
        score -= d * 100
        e = score // 10
        score -= e * 10
        f = score // 1

        score_numbers[0].figure = a
        score_numbers[1].figure = b
        score_numbers[2].figure = c
        score_numbers[3].figure = d
        score_numbers[4].figure = e
        score_numbers[5].figure = f

        for number in score_numbers:
            number.change_sprite()

