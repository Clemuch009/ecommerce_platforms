def main():
    y = 45
    print('hello')
    def helper():
        print('world', y + 1)
    return (helper())

main()
helper()
