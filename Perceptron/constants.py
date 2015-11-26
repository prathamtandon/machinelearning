count_mistakes_datasets = ['dataset-500.libsvm', 'dataset-1000.libsvm']
count_mistakes_dimensions = [500, 1000]
training_size = 5000
testing_size = 5000
perceptron_params_without_margin = [[0],[1]]
perceptron_params_with_margin = [[1],[1.5,0.25,0.03,0.005,0.001]]
winnow_params_without_margin = [[0],[1.1,1.01,1.005,1.0005,1.0001]]
winnow_params_with_margin = [[2.0,0.3,0.04,0.006,0.001],
                        [1.1,1.01,1.005,1.0005,1.0001]]
num_rounds = 20
