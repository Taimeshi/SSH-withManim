from calc_scene import CalcScene


def main():
    code = "val1=1+1"
    scene = CalcScene(code, "test.py")
    scene.render()


if __name__ == '__main__':
    main()
