from unittest import TestCase
from handler import property
import json

class PropertyAPITest(TestCase):
    """ TestCase's Api property """

    def test_api_get_status(self):
        """ verify code status in the response api """
        event = {"multiValueQueryStringParameters": None}
        context = {}
        response = property(event, context)
        self.assertEqual(response["statusCode"], 200)
    
    def test_api_get_result(self):
        """ verify data result in the response api """
        event = {"multiValueQueryStringParameters": None}
        context = {}
        response = property(event, context)
        self.assertNotEqual(len(json.loads(response["body"])), 0)
    
    def test_api_get_result_filter_status(self):
        """ verify code status in the response api when recive filters """
        event = {"multiValueQueryStringParameters": {
            "year" : [2011],
            "status": ["en_venta"],
            "city": ["bogota"]
        }}
        context = {}
        response = property(event, context)
        self.assertEqual(response["statusCode"], 200)

    def test_api_get_result_filter_result(self):
        """ verify data result in the response api when recive filters """
        event = {"multiValueQueryStringParameters": {
            "year" : [2011],
            "status": ["en_venta"],
            "city": ["bogota"]
        }}
        context = {}
        response = property(event, context)
        self.assertEqual(len(json.loads(response["body"])), 1)

    def test_api_get_filters_wrong_status(self):
        """ verify code status in the response api when recive filters invalid """
        event = {"multiValueQueryStringParameters": {
            "year" : ["adsadadad"]
        }}
        context = {}
        response = property(event, context)
        self.assertEqual(response["statusCode"], 400)
    
