# -*- coding: utf-8 -*-
"""
:Module: ``mmglue``
:Author: `Adrian Letchford <http://www.dradrian.com>`_
:Organisation: Loud News.
:Created On: Tue Dec 30 13:39:36 2014

Provides some "glue" between Endpoint models and messages
"""

# Import build in modules
import datetime
from google.appengine.ext import ndb
import logging

# Import external modules

# Import custom modules


#------------------------------------------------------------------------------
# Program Start
#------------------------------------------------------------------------------

def model_attrs(model):
    """Returns dictionary of model properties."""
    return model._properties
    
def model_instance_attrs(model):
    """Returns dictionary of model instance properties."""
    return model._values
    
def message_attrs(message):
    """Returns dictionary of message properties."""
    return message._Message__by_name
    
def message_instance_attrs(message):   
    """Returns dictionary of message instance properties."""
    
    # Get the attributes of the Message type
    attrs = message_attrs(type(message))
    
    # Get the attribute values of the message. The values are referenced
    # by number instead of by name.
    by_number = message._Message__tags
    
    # Have to get the message values by name
    
    by_name = {}

    # For each attribute
    for name, value in attrs.items():
        
        # Get it's number
        number = int(value.number)
        
        # If this attribute is present in the message
        if number in by_number:
            
            # Add it's name and value to the dictionary
            by_name[name] = by_number[number]
            
    return by_name
 

def parse_string(value):
    s =""
    for c in value:
        try:
            s += c.encode('ascii', errors='ignore')
        except:
            pass
    return s

 
def message_from_model(modeli, messageType):   
    # Automatically create a message from the model
    
    new_message = messageType()
    
    model_values = model_instance_attrs(modeli)
    message_fields = message_attrs(messageType)
    
    # for each of the model's atrributes
    for attr, value in model_values.iteritems():

        try:
            value = value.b_val
        except:
            pass
        
        # Skip any model attributes that cannot be found in the message object
        cond1 = attr in message_fields
        cond2 = type(value) is ndb.key.Key and attr+"_id" in message_fields
        if not (cond1 or cond2):
            continue
        
        easy_types = [int, long, datetime.datetime, bool]
        string_types = [unicode, str]
        
        
        if type(value) in easy_types:
            setattr(new_message, attr, value)
            
        elif type(value) in string_types:
            setattr(new_message, attr, parse_string(value))
            
        elif type(value) is ndb.key.Key:
            #print "Found a key"
            field = attr+"_id"
            #print field
            if field in message_fields:
                setattr(new_message, field, value.id())
            else:
            	pass
                # s = ("Couldn't match the model's key to a message field %s (%s) :" % (attr, str(type(value)))), value
                # logging.debug(s)
                
        elif value is None:
            # We don't want to do anything, just pass
            pass
        else:
        	pass
            # m = ("Unknown attribute type for %s (%s) :" % (attr, str(type(value)))), value
            # logging.debug('-'*80)
            # logging.debug(m)
            # logging.debug('-'*80)
            #raise Exception(m)
            
    # Add the model's ID
    if 'id' in message_fields:
        new_message.id = modeli.key.id()
    
    return new_message
    
    
    
    
def model_from_message(messagei, modelType, **kwargs): 
    """
    Skips any fields that end with '_id'.
    Skips the id field/attribute. Setting this on a model seems to load
    the original model from the database.
    """
    
    new_model = modelType(**kwargs)
    
    message_fields = message_instance_attrs(messagei)
    #model_attrs = model_attrs(modelType)
    
    
    
    # for each of the message's fields
    for field, value in message_fields.iteritems():
        
        if field == "id" or field.endswith("_id"):
            continue
        
        easy_types = [int, str, long, float, unicode, datetime.datetime]
        if type(value) in easy_types:
            #print field, value
            setattr(new_model, field, value)
            #print "set atrribute", field
           # print new_model
        elif value is None:
            # We don't want to do anything, just pass
            pass
        else:
            m = ("Unknown field type for %s (%s) :" % (field, str(type(value)))), value
            
            #print '-'*80
            #print m
            #print '-'*80     
    
    
    return new_model