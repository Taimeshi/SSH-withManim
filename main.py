from calc_scene import CalcScene


def main():

    code = "val1=4*2+1+2+3"
    scene = CalcScene(code)
    scene.render()


if __name__ == '__main__':
    main()
