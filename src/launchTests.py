from tests import testCases, test

for case in testCases.cases:
    try:
        test.launch_test(case)
    except:
        print('An error occurred!')
