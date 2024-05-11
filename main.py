from backup_camera.application import Application


def main():
    scale = 1.3
    app = Application((int(1280 // scale), int(720 // scale)))
    app.run()
    
if __name__ == '__main__':
    main()