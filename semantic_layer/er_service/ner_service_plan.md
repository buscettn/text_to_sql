# Overview
Plan is to build a named entity resolution service.
To recognise "bank" labels.

# Model
Backbone is GLiNER, GLiNER will be fine tuned on entities.
Base model used for fine tuning will be urchade/gliner_multi-v2.1

# Entities and fine tuning
Named entities will have an id and a name. The list of entities to be fine tuned is in /data/semantic_input/entities/mfi_entities.csv. The relevant columns in this file is NAME. Strip the names before using, but no need for any other manipulation. All these entities should be labeld as "bank".

In /data/semantic_input/entities/example_sentences.txt are example sentences to be used with the entities. Every line of the file is a sentence/question and has a placeholder {entity}. This placeholder is to be replaced with an entity name from the mfi_entities.csv file. Every line of the file in combination with a random entity will be a training example for the fine tuning process. This potentially equals number of sentences * number of entities samples - so limit the dataset to 10000 examples.

In /data/semantic_input/entities/negative_sentences.txt are examples sentences and questions without any entities (negative samples). These should be used to train the model to not recognise entities where there are none. Every line of the file is a sentence/question.

First step is to generate the training data, which will be stored in /data/semantic_input/entities/train. Store it in whatever format is most comfortable.
This step is in a separte file. The training data is limited to 10000 and should have a certain split between positive and negative examples. This is defined by a ratio (ratio = 10% negative examples). When the number of positive or negative examples is too low to fit a total of 10000, reduce number of total samples so that it fits the lower number automatically.
Example I: 100 negative samples is too low -> only 1000 samples in total dataset with 900 positive samples.
Example II: if I have 500 negative samples, should I generate exactly 4500 positive samples to maintain the 1:9 ratio (total 5000).

Then the fine tuning will be performed using the training data and the base model. This step is also a separate file. For testing set the fine tuning parameters to be very very short and the training set limited to 20 samples (parameterized). Remember that the entities comprise of several words, this might be relevant for labeling.

# File Location
All python files will be stored in /semantic_layer/er_service.
The original model and the fine tuned model shall be stored in /data/gliner/models.

# Inference
Inference will be performed using the fine tuned model and a text query. The extracted entities will be returned as a list of entitiy names. This inference should be a query_liner.py which should run through the CLI.

# Code guidelines
Keep the code simple and focus on readability and extendability. We might want to add more lables in the future (keep that in mind). Include comments where necessary for understanding.

# Additional considerations for fine tuning
Offset Calculation: Instead of searching for the string after replacement, the script should calculate the offset during the replacement of the {entity} placeholder. For example, if the template is Show me data for {entity}, the start offset is the index of {entity} in the template, and the end offset is start + len(entity_name).
Handling Multi-word Entities: Ensure that the tokenization (handled by the GLiNER backbone) respects the boundaries of these multi-word spans. GLiNER is generally good at this, but we should verify that our training data doesn't accidentally truncate trailing punctuation if it's not part of the entity name.