from gui import *


def main():
    window = Tk()
    window.title('Vote menu')
    window.geometry('200x200')
    window.resizable(False, False)

    Gui(window)
    window.mainloop()
    

if __name__ == '__main__':
    main()
