# Naive Bayes learner constants.

vocabulary_filepath = 'processed/vocabulary.txt'
training_metadata_filepath = 'processed/train-files.txt'
training_template_filepath = 'processed/[0].train.txt'
training_filepath_placeholder = '[0]'
test_filepath = 'processed/test.txt'
output_filepath = 'predictions.nb'
label_mappings = {
    'articles': 1.0,
    'corporate': 2.0,
    'enron_t_s': 3.0,
    'enron_travel_club': 4.0,
    'hea_nesa': 5.0,
    'personal': 6.0,
    'systems': 7.0,
    'tw_commercial_group': 8.0
}
