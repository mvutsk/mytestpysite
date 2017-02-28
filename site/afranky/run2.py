from aprj import create_app

def main():
    app = create_app('settings')
    app.run()

if __name__ == '__main__':
    main()
