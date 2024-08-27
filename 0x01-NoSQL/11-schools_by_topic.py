#!/usr/bin/env python3
""" finding documents with specific topic """


def schools_by_topic(mongo_collection, topic):
    """ function that returns the list of school
        having a specific topic
    """
    list_topics = []

    list_topics.extend(mongo_collection.find({'topics' : topic}))
    return list_topics
