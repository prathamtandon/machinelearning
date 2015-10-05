from prob2 import ID3
from Queue import Queue

def get_predicted_label(dec_tree, record):
    cur = dec_tree
    while True:
        try:
            label = int(cur.key)
            return label
        except:
             branch = record[cur.key]
             found = False
             for child in cur.children:
                 for key in child:
                     if key == branch:
                         cur = child[key]
                         found = True
                 if found:
                     break

def test_entropy():
    training_examples = []
    attributes = ['age', 'prescription', 'astigmatic', 'tear rate']
    training_examples.append({'age':1,'prescription':1,'astigmatic':1,'tear rate':1, 'lenses':3})
    training_examples.append({'age':1,'prescription':1,'astigmatic':1,'tear rate':2, 'lenses':2})
    training_examples.append({'age':1,'prescription':2,'astigmatic':1,'tear rate':1, 'lenses':3})
    training_examples.append({'age':1,'prescription':2,'astigmatic':1,'tear rate':2, 'lenses':2})
    training_examples.append({'age':1,'prescription':2,'astigmatic':2,'tear rate':1, 'lenses':3})
    training_examples.append({'age':1,'prescription':2,'astigmatic':2,'tear rate':2, 'lenses':1})
    training_examples.append({'age':2,'prescription':1,'astigmatic':1,'tear rate':1, 'lenses':3})
    training_examples.append({'age':2,'prescription':1,'astigmatic':1,'tear rate':2, 'lenses':2})
    training_examples.append({'age':2,'prescription':1,'astigmatic':2,'tear rate':2, 'lenses':1})
    training_examples.append({'age':2,'prescription':2,'astigmatic':1,'tear rate':1, 'lenses':3})
    training_examples.append({'age':2,'prescription':2,'astigmatic':2,'tear rate':1, 'lenses':3})
    training_examples.append({'age':2,'prescription':2,'astigmatic':2,'tear rate':2, 'lenses':3})
    training_examples.append({'age':3,'prescription':1,'astigmatic':1,'tear rate':2, 'lenses':3})
    training_examples.append({'age':3,'prescription':1,'astigmatic':2,'tear rate':1, 'lenses':3})
    training_examples.append({'age':3,'prescription':1,'astigmatic':2,'tear rate':2, 'lenses':1})
    training_examples.append({'age':3,'prescription':2,'astigmatic':1,'tear rate':1, 'lenses':3})
    training_examples.append({'age':3,'prescription':2,'astigmatic':2,'tear rate':1, 'lenses':3})
    training_examples.append({'age':3,'prescription':2,'astigmatic':2,'tear rate':2, 'lenses':3})

    dec_tree = ID3(training_examples, 'lenses', attributes)

    assert(dec_tree.key == 'tear rate')

    test_examples = []
    test_examples.append({'age':1,'prescription':1,'astigmatic':2,'tear rate':1, 'lenses':3})
    test_examples.append({'age':1,'prescription':1,'astigmatic':2,'tear rate':2, 'lenses':1})
    test_examples.append({'age':2,'prescription':1,'astigmatic':2,'tear rate':1, 'lenses':3})
    test_examples.append({'age':2,'prescription':2,'astigmatic':1,'tear rate':2, 'lenses':2})
    test_examples.append({'age':3,'prescription':1,'astigmatic':1,'tear rate':1, 'lenses':3})
    test_examples.append({'age':3,'prescription':2,'astigmatic':1,'tear rate':2, 'lenses':2})

    correct = 0

    for test_example in test_examples:
        label = get_predicted_label(dec_tree, test_example)
        if label == test_example['lenses']:
            correct += 1

    accuracy = float(correct)/len(test_examples)
    assert(accuracy == float(5)/6)



