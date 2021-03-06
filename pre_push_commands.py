from os import system as execute_cmd


def title_message(title_str: str, title_size: int):
    print(
        f"{'*' * title_size}\n"
        f"* {title_str.center(title_size - 4, ' ')} *\n"
        f"{'*' * title_size}"
    )


if __name__ == '__main__':
    # for development pdoc server at localhost:8081
    # pipenv run python -m  pdoc --http localhost:8081 Rigol1000z

    str_width = 24

    title_message('Starting type checking', str_width)
    execute_cmd('mypy -p ECPF')
    title_message('Type checking Complete', str_width)
    print("\n")

    title_message('Starting tests', str_width)
    execute_cmd('pipenv run python -m unittest discover -s ./tests')
    title_message('Testing complete', str_width)
    print("\n")

    title_message('Generating documentation', str_width)
    execute_cmd('pdoc ECPF --html --force')
    title_message('Documentation generating complete', str_width)
    print("\n")

    title_message('Creating distribution wheel', str_width)
    execute_cmd("pipenv run python setup.py sdist bdist_wheel")
    title_message('Wheel creation complete', str_width)
    print("\n")
