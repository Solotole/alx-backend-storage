#!/usr/bin/env python3
""" inserting a documennt in python """


def insert_school(mongo_collection, **kwargs):
    """ inserting new document """
    new_doc = mongo_collection.insert_one(kwargs)

    return new_doc.inserted_id
