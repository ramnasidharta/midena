from model.FileUtil import import_FA


def test(words, expected, msg='Success!', start=0):
    i = start
    for word in words:
        i += 1
        if dfa.accept(word) == expected:
            print(f'Test {i}: OK')
        else:
            print(f'Test {i} failed with word: {word}')
            print(f'Expected: {"accept" if expected else "not accept"}\n')
    print(f'{msg}\n')


# starts and ends with same symbol
dfa = import_FA('saves/equal_first_last.json')
print(dfa)

right_words = ['', 'a', 'b', 'aa', 'bb', 'aabbaba', 'bababab', 'bbbab']
test(right_words, True, msg='Correct words accepted.')

wrong_words = ['ab', 'ba', 'abcba', 'c', 'ababbbab', 'bbabbabbabababa']
test(wrong_words, False, msg='Wrong words correctly not accepted.', start=len(right_words))

# ends with 0 (zero)
dfa = import_FA('saves/nfa_ends_with_zero.json')
print(dfa)

right_words = ['0', '000', '01010', '11110', '10', '11110', '10101010']
test(right_words, True, msg='Correct words accepted.')

wrong_words = ['1', '01', '0001', '101', '11101', '01010101', '101010101']
test(wrong_words, False, msg='Wrong words correctly not accepted.', start=len(right_words))