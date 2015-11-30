count_mistakes_datasets = ['dataset-500.libsvm', 'dataset-1000.libsvm']
learning_curves_datasets = ['dataset-40.libsvm', 'dataset-80.libsvm', 'dataset-120.libsvm', 'dataset-160.libsvm', 'dataset-200.libsvm']
batch_performance_datasets = [['training-100.libsvm', 'testing-100.libsvm'],['training-500.libsvm', 'testing-500.libsvm'],['training-1000.libsvm', 'testing-1000.libsvm']]
count_mistakes_dimensions = [500, 1000]
learning_curves_dimensions = [40,80,120,160,200]
training_size = 5000
testing_size = 5000
perceptron_params_without_margin = [[0],[1]]
perceptron_params_with_margin = [[1],[1.5,0.25,0.03,0.005,0.001]]
winnow_params_without_margin = [[0],[1.1,1.01,1.005,1.0005,1.0001]]
winnow_params_with_margin = [[2.0,0.3,0.04,0.006,0.001],
                        [1.1,1.01,1.005,1.0005,1.0001]]
num_rounds = 20
instance_scale = [i*100 for i in range(501)]
survival_count = 100
batch_performance_n = 1000
