from enum import IntEnum, auto


class State(IntEnum):
    VERSE_NUMBER = 1
    SANSKRIT = auto()
    WORDS_TRANSLATION = auto()
    TRANSLATION = 4


class ParsingState:
    def __init__(self):
        # parsing_state
        self.ps = State.VERSE_NUMBER
        self.sanskrit = False

    def next_state(self):
        self.ps += 1
        # after 4th state, we go back to beginning
        if self.ps > 4:
            # now it is int, not State(IntEnum) anymore !!! this is bug but it is working
            self.ps = State.VERSE_NUMBER
        # we are done parsing it
        if self.sanskrit is True:
            self.sanskrit = False

def get_verses():
    parser = ParsingState()

    with open('108_BG_sloka.txt', encoding="utf-8") as file:
        line_number_counter = 0    # for DEBUG
        for line in file:
            line_number_counter += 1

            line_empty = False
            line = line.strip()
            #print(f'{line=}')
            if line == '':
                line_empty = True

            match parser.ps:
                case State.VERSE_NUMBER:
                    #print(f'{line_number_counter} --- State.VERSE_NUMBER {line_empty=}')
                    if line_empty is False:
                        #f = float(line)
                        f = line
                        parser.next_state()

                case State.SANSKRIT:
                    #print(f'{line_number_counter} --- State.SANSKRIT \
                    #    {parser.sanskrit=} {line_empty=}')
                    if parser.sanskrit is False:
                        if line_empty is True:
                            continue
                        else:
                            parser.sanskrit = True
                    elif parser.sanskrit is True:
                        if line_empty is False:
                            continue
                        else:
                            parser.next_state()
                    else:
                        print('ERROR 2'); break

                case State.WORDS_TRANSLATION:
                    #print(f'{line_number_counter} --- State.WORDS_TRANSLATION {line_empty=}')
                    if line_empty is False:
                        parser.next_state()
                    else:
                        print('ERROR 3'); break

                case State.TRANSLATION:
                    #print(f'{line_number_counter} --- State.TRANSLATION {line_empty=}')
                    if line_empty is True:
                        continue
                    else:
                        translation = line
                        parser.next_state()
                        # one cycle done
                        #print(f"{f}\n{translation}\n")
                        yield (f, translation)

                case _:
                    print("ERROR STATE 5"); break

def main():
    for number, verse in get_verses():
        print(f"{verse}\n\n{number} Bhagavat Gita\n%")


def is_float(string: str):
    f = None
    try:
        f = float(string)
        result = True
    except ValueError:
        #print("Not a float")
        result = False

    return (result, f)


if __name__ == "__main__":
    main()
