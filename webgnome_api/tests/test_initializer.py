"""
Functional tests for the Gnome Initializer object Web API
"""
from base import FunctionalTestBase


class InitializerBase(FunctionalTestBase):
    '''
        Tests out the Gnome Initializer object API
    '''
    req_data = {'obj_type': u'gnome.spill.elements.InitWindages',
                'json_': u'webapi',
                'windage_range': (0.01, 0.04),
                'windage_persist': 900,
                }
    fields_to_check = ('id', 'obj_type')

    def test_get_no_id(self):
        resp = self.testapp.get('/initializer')

        assert 'obj_type' in self.req_data
        obj_type = self.req_data['obj_type'].split('.')[-1]

        assert (obj_type, obj_type) in [(name, obj['obj_type'].split('.')[-1])
                                        for name, obj
                                        in resp.json_body.iteritems()]

    def test_get_invalid_id(self):
        obj_id = 0xdeadbeef
        self.testapp.get('/initializer/{0}'.format(obj_id), status=404)

    def test_get_valid_id(self):
        # 1. create the object by performing a put with no id
        # 2. get the valid id from the response
        # 3. perform an additional get of the object with a valid id
        # 4. check that our new JSON response matches the one from the create
        resp1 = self.testapp.put_json('/initializer', params=self.req_data)

        obj_id = resp1.json_body['id']
        resp2 = self.testapp.get('/initializer/{0}'.format(obj_id))

        for k in self.fields_to_check:
            assert resp2.json_body[k] == resp1.json_body[k]

    def test_put_no_payload(self):
        self.testapp.put_json('/initializer', status=400)

    def test_put_no_id(self):
        resp = self.testapp.put_json('/initializer', params=self.req_data)

        for k in self.fields_to_check:
            assert k in resp.json_body

    def test_put_invalid_id(self):
        obj_id = 0xdeadbeef
        resp = self.testapp.put_json('/initializer/{0}'.format(obj_id),
                                     params=self.req_data)

        for k in self.fields_to_check:
            assert k in resp.json_body

    def test_put_valid_id(self):
        # 1. create the object by performing a put with no id
        # 2. get the valid id from the response
        # 3. update the properties in the JSON response
        # 4. update the object by performing a put with a valid id
        # 5. check that our new properties are in the new JSON response
        resp = self.testapp.put_json('/initializer', params=self.req_data)

        obj_id = resp.json_body['id']
        req_data = resp.json_body
        self.perform_updates(req_data)

        resp = self.testapp.put_json('/initializer/{0}'.format(obj_id),
                                     params=req_data)
        self.check_updates(resp.json_body)

    def perform_updates(self, json_obj):
        '''
            We can overload this function when subclassing our tests
            for new object types.
        '''
        pass

    def check_updates(self, json_obj):
        '''
            We can overload this function when subclassing our tests
            for new object types.
        '''
        pass


class InitWindagesTests(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitWindages',
                'json_': u'webapi',
                'windage_range': (0.01, 0.04),
                'windage_persist': 900,
                }
    fields_to_check = ('id', 'obj_type', 'windage_range', 'windage_persist')

    def perform_updates(self, json_obj):
        super(InitWindagesTests, self).perform_updates(json_obj)

        json_obj['windage_range'] = (0.1, 0.4)
        json_obj['windage_persist'] = 1000

    def check_updates(self, json_obj):
        super(InitWindagesTests, self).check_updates(json_obj)

        assert json_obj['windage_range'] == [0.1, 0.4]
        assert json_obj['windage_persist'] == 1000


class InitMassComponentsFromOilPropsTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitMassComponentsFromOilProps',
                'json_': u'webapi',
                }


class InitHalfLivesFromOilPropsTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitHalfLivesFromOilProps',
                'json_': u'webapi',
                }


class InitMassFromTotalMassTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitMassFromTotalMass',
                'json_': u'webapi',
                }


class InitMassFromVolumeTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitMassFromVolume',
                'json_': u'webapi',
                }


class InitMassFromPlumeTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitMassFromPlume',
                'json_': u'webapi',
                }


class InitRiseVelFromDistTest(InitializerBase):
    req_data = {
                'obj_type': u'gnome.spill.elements.InitRiseVelFromDist',
                'json_': u'webapi',
                }
