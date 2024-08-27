#!/usr/bin/env python3
""" changing school topics """


def update_topics(mongo_collection, name, topics):
    """ Python function that changes all topics
        of a school document based on the name
    """
    filter = {'name': name}
    mongo_collection.update_one(filter, {'$set' : {'topics' : topics}})
