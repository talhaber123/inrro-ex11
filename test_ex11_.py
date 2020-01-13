import pickle
import itertools

import ex11

# Change to True in order to check your optimal tree structure
CHECK_OPTIMAL_TREE = False

flu_leaf = ex11.Node("influenza", None, None)
cold_leaf = ex11.Node("cold", None, None)
inner_vertex = ex11.Node("fever", flu_leaf, cold_leaf)
healthy_leaf = ex11.Node("healthy", None, None)
root = ex11.Node("cough", inner_vertex, healthy_leaf)
simple_diagnoser = ex11.Diagnoser(root)
one_leaf_diagnoser = ex11.Diagnoser(flu_leaf)

with open('data/big_diagnoser.dmp', 'rb') as f:
    big_diagnoser = pickle.load(f)
with open('data/medium_diagnoser.dmp', 'rb') as f:
    medium_diagnoser = pickle.load(f)


def repr_tree(tree, tabs=0, s=''):
    """
    Prints symptoms tree.
    :return: None
    """
    if tree.positive_child:
        s += ' ' * tabs + str(tree.data) + ': True\n'
        s += repr_tree(tree.positive_child, tabs + 4)
    if tree.negative_child:
        s += ' ' * tabs + str(tree.data) + ': False\n'
        s += repr_tree(tree.negative_child, tabs + 4)
    else:
        s += ' ' * tabs + str(tree.data) + '\n'
    return s


def repr_records(records):
    return '\n'.join([f'{record.symptoms} -> {record.illness}'
                      for record in records])


def test_simple_test(capsys):
    diagnosis = simple_diagnoser.diagnose(["cough"])
    assert diagnosis == "cold"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_diagnose(capsys):
    for symptoms, diagnosis in {
        ('congestion',
         'cough',
         'fatigue'): ['cold', 'influenza', 'healthy', 'influenza'],
        ('congestion',
         'cough',
         'fatigue',
         'fever',
         'headache',
         'irritability',
         'muscle_ache',
         'nausea',
         'rigidity',
         'sore_throat'): ['influenza', 'mono', None, 'influenza'],
        ('nausea',): ['healthy', 'healthy', None, 'influenza'],
        (): ['healthy', 'healthy', 'healthy', 'influenza'],
    }.items():
        for i, cur_diagnoser in enumerate([simple_diagnoser, big_diagnoser,
                                           medium_diagnoser,
                                           one_leaf_diagnoser]):
            expected = diagnosis[i]
            actual = cur_diagnoser.diagnose(list(symptoms))
            assert actual == expected, \
                f"tree: {repr_tree(cur_diagnoser.root)}\n" \
                f"symptoms: {list(symptoms)}\n" \
                f"expected: {expected}\n" \
                f"actual: {actual}"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_calculate_success_rate(capsys):
    for fn, successes in {
        r'data/tiny_data.txt': [2 / 6, 5 / 6, 5 / 6, 1 / 6],
        r'data/small_data.txt': [20 / 60, 44 / 60, 47 / 60, 10 / 60],
        r'data/medium_data.txt': [213 / 600, 442 / 600, 534 / 600, 100 / 600],
        r'data/big_data.txt': [2278 / 6000, 4403 / 6000, 5298 / 6000,
                               1000 / 6000],
    }.items():
        records = ex11.parse_data(fn)
        for i, cur_diagnoser in enumerate([simple_diagnoser, big_diagnoser,
                                           medium_diagnoser,
                                           one_leaf_diagnoser]):
            expected = successes[i]
            actual = cur_diagnoser.calculate_success_rate(records)
            assert actual == expected, \
                f"tree: {repr_tree(cur_diagnoser.root)}\n" \
                f"records from: {fn}\n" \
                f"expected: {expected}\n" \
                f"actual: {actual}"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_all_illnesses(capsys):
    big_diagnoser_permutations = []
    for i in itertools.permutations(['mono', 'influenza'], 2):
        for j in itertools.permutations(['cold', 'meningitis', 'strep',
                                         'healthy'], 4):
            big_diagnoser_permutations.append(tuple(i + j))

    for cur_diagnoser, illnesses in {
        simple_diagnoser: list(itertools.permutations(
            ['influenza', 'cold', 'healthy'], 3)),
        big_diagnoser: big_diagnoser_permutations,
        medium_diagnoser: [('influenza', 'mono', 'strep',
                            'healthy', 'cold', 'meningitis'),
                           ('influenza', 'mono', 'strep',
                            'cold', 'healthy', 'meningitis')
                           ],
        one_leaf_diagnoser: [('influenza',)],
    }.items():
        expected = illnesses
        actual = tuple(cur_diagnoser.all_illnesses())
        assert actual in expected, \
            f"tree: {repr_tree(cur_diagnoser.root)}\n" \
            f"expected: {expected}\n" \
            f"actual: {actual}"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_paths_to_illness(capsys):
    for illness, paths in {
        "influenza": [[[True, True]],
                      [[True, True, False], [True, False, False]],
                      [[True, True, True, True, True, False],
                       [True, True, True, True, False, False],
                       [True, True, True, False, False, False],
                       [True, True, False, True, False, False],
                       [True, False, True, True, True, False],
                       [True, False, True, True, False, False],
                       [True, False, True, False, False, False],
                       [False, True, True, True, True, False],
                       [False, True, True, False, True, False],
                       [False, True, False, True, True, False],
                       [False, True, False, False, True, False],
                       [False, False, True, True, True, False]],
                      [[]]
                      ],
        "cold": [[[True, False]],
                 [[False, True, True]],
                 [[True, False, False, True, False, True],
                  [True, False, False, True, False, False],
                  [True, False, False, False, False, True],
                  [False, False, False, True, False, True]],
                 []
                 ],
        "healthy": [[[False]],
                    [[False, False, False]],
                    [[True, True, False, False, False, False],
                     [True, False, False, False, False, False],
                     [False, True, False, False, False, False],
                     [False, False, False, False, False, False]],
                    []
                    ]
    }.items():
        for i, cur_diagnoser in enumerate([simple_diagnoser, big_diagnoser,
                                           medium_diagnoser,
                                           one_leaf_diagnoser]):
            actual = cur_diagnoser.paths_to_illness(illness)
            expected = paths[i]
            assert sorted(actual) == sorted(expected), \
                f"tree: {repr_tree(cur_diagnoser.root)}\n" \
                f"illness: {illness}\n" \
                f"expected: {expected}\n" \
                f"actual: {actual}"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_build_tree(capsys):
    for tree, fn in {
        # sanity
        ex11.build_tree(ex11.parse_data(r'data/tiny_data.txt'),
                        ['cough', 'irritability', 'headache']):
            [f'data/build_tree_sanity{i}.txt' for i in range(1, 5)],
        # empty symptoms
        ex11.build_tree(ex11.parse_data(r'data/tiny_data.txt'), []):
            [f'data/build_tree_empty_symptoms{i}.txt' for i in range(1, 7)],
        # empty records
        ex11.build_tree([], ['cough', 'irritability', 'headache']):
            ['data/build_tree_empty_records.txt'],
        # empty both
        ex11.build_tree([], []):
            ['data/build_tree_empty_both.txt'],
        # double symptoms
        ex11.build_tree(ex11.parse_data(r'data/tiny_data.txt'),
                        ['cough', 'headache', 'headache']):
            [f'data/build_tree_double_symptoms{i}.txt' for i in range(1, 9)],
    }.items():
        actual = repr_tree(tree)
        expected = [open(_fn).read() for _fn in fn]
        assert actual in expected, \
            f"test name: {fn}\n" \
            f"expected: {expected}\n" \
            f"actual: {actual}"

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"


def test_optimal_tree(capsys):
    symptoms = [
        'congestion',
        'cough',
        'fatigue',
        'fever',
        'headache',
        'irritability',
        'muscle_ache',
        'nausea',
        'rigidity',
        'sore_throat'
    ]

    for fn, successes in {
        r'data/tiny_data.txt': [1 / 6, 2 / 6, 4 / 6, 5 / 6,
                                1, 1, 1, 1, 1, 1, 1],
        r'data/small_data.txt': [10 / 60, 20 / 60, 36 / 60, 49 / 60, 52 / 60,
                                 53 / 60, 55 / 60, 56 / 60, 56 / 60,
                                 56 / 60, 56 / 60],
        r'data/medium_data.txt': [100 / 600, 195 / 600, 346 / 600, 445 / 600,
                                  491 / 600, 517 / 600, 534 / 600,
                                  540 / 600, 543 / 600, 544 / 600, 545 / 600],
        r'data/big_data.txt': [1000 / 6000, 1951 / 6000, 3359 / 6000,
                               4403 / 6000],
    }.items():
        records = ex11.parse_data(fn)
        for i in range(len(symptoms) + 1):
            if fn.endswith('big_data.txt') and i > 3:
                continue
            tree = ex11.optimal_tree(records, symptoms, i)
            if CHECK_OPTIMAL_TREE:
                actual = repr_tree(tree)
                # open(fn + '.4expected' + str(i), 'w').write(actual)
                expected1 = open(fn + '.expected' + str(i)).read()
                expected2 = open(fn + '.2expected' + str(i)).read()
                expected3 = open(fn + '.3expected' + str(i)).read()
                expected4 = open(fn + '.4expected' + str(i)).read()
                assert actual in (expected1, expected2, expected3, expected4), \
                    "Maybe your answer is correct, check it carefully. " \
                    "If it's OK, remove this assert."
            cur_diagnoser = ex11.Diagnoser(tree)
            # print(diagnoser.calculate_success_rate(records), end=', ')
            actual = cur_diagnoser.calculate_success_rate(records)
            expected = successes[i]
            assert actual == expected, \
                f"tree: {repr_tree(cur_diagnoser.root)}\n" \
                f"records from: {fn}\n" \
                f"num of symptoms: {i}\n" \
                f"expected: {expected}\n" \
                f"actual: {actual}"

            # if fn.endswith('big_data.txt') and i == 3:
            #     with open('data/big_diagnoser.dmp', 'wb') as f:
            #         pickle.dump(diagnoser, f)
            # if fn.endswith('medium_data.txt') and i == 6:
            #     with open('data/medium_diagnoser.dmp', 'wb') as f:
            #         pickle.dump(diagnoser, f)
        # print()

    out, err = capsys.readouterr()
    assert not out and not err, f"Don't print. out: '{out}', err: '{err}'"
