import matplotlib.pyplot as plt


class Unboxy:
    def __init__(self, imagebin):
        self.bitmap = [[[245 for i in range(3)] for j in range(256)] for k in range(256)]
        self.x0 = 0
        self.y0 = 0
        self.width = 0
        self.height = 0
        self.color = 0
        with open(imagebin) as image:
            f = image.read()
        self.f = map(lambda x: ord(x), list(f))

    def plot_rectangle(self):
        if self.print_previous:
            self.print_previous = False
            plt.imshow(self.bitmap)
            plt.show()
        rgb_color = self.get_rgb_color()
        for x in range(self.width):
            for y in range(self.height):
                for i in range(3):
                    self.bitmap[self.x0 + x][self.y0 + y][i] = rgb_color[i]

    def get_rgb_color(self):
        if self.color == 0:
            return [255, 255, 255]
        if self.color == 1:
            return [0, 0, 0]
        if self.color == 2:
            return [255, 0, 0]
        if self.color == 3:
            return [127, 255, 0]
        if self.color == 4:
            return [255, 255, 0]
        if self.color == 5:
            return [0, 0, 255]
        if self.color == 6:
            return [255, 0, 255]
        if self.color == 7:
            return [0, 255, 255]

    def execute(self):
        i = 0
        while i < len(self.f):
            if self.f[i] == 255 and self.f[i+1] == 0:
                # plot rectangle
                self.plot_rectangle()
                i += 2
            elif self.f[i] == 1 and self.f[i+2] == 2:
                # create rectangle
                self.width = self.f[i+3]
                self.height = self.f[i+1]
                i += 4
                if self.width == 255 and self.height == 255:
                    self.print_previous = True
            elif self.f[i] == 3:
                # paint rectangle
                self.color = self.f[i+1]
                i += 2
            elif self.f[i] == 4 and self.f[i+2] == 5:
                # move rectangle
                self.x0 = self.f[i+1]
                self.y0 = self.f[i+3]
                i += 4
            elif self.f[i] == 6:
                # move rectangle up
                self.x0 -= self.f[i+1]
                i += 2
            elif self.f[i] == 7:
                # move rectangle down
                self.x0 += self.f[i+1]
                i += 2
            elif self.f[i] == 8:
                # move rectangle left
                self.y0 -= self.f[i+1]
                i += 2
            elif self.f[i] == 9:
                # move rectangle right
                self.y0 += self.f[i+1]
                i += 2
            else:
                print("Unknown instruction i = {}, {}, {}".format(i, self.f[i], self.f[i+1]))
                exit()
        plt.imshow(self.bitmap)
        plt.show()


if __name__ == "__main__":
    p = Unboxy('./files/reverseme')
    p.execute()
