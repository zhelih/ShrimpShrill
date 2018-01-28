#!flask/bin/python
from flask import Flask, jsonify, request, abort, Response
import json

app = Flask(__name__)

class Location:
    def __init__(self):
        self.m_state    = None
        self.m_city     = None
        self.m_street   = None
        self.m_building = None
        
        self.m_latitude  = None
        self.m_longitude = None
    
    def state(self):
        return self.m_state
    
    def city(self):
        return self.m_city
        
    def street(self):
        return self.m_street
        
    def building(self):
        return self.m_building;
        
    def latitude(self):
        return self.m_latitude
        
    def longitude(self):
        return self.m_longitude
        
class Pending:
    last_id = 0
    
    def __init__(self):
        Pending.last_id += 1
        self.m_id       = Pending.last_id
        self.m_user     = None
        self.m_text     = None
        self.m_link     = None
        self.m_date     = None
        self.m_location = None
        self.m_source   = None # 0: Twitter-based, 1: Self-reported
        
    def user(self):
        return self.m_user
        
    def text(self):
        return self.m_text
        
    def link(self):
        return self.m_text
        
    def date(self):
        return self.m_date
        
    def location(self):
        return self.m_location
        
    def source(self):
        return self.m_source
        
    def dictify(self):
        resp = {
            'id'    : self.m_id,
            'user'  : self.user(),
            'date'  : self.date(),
            'source': self.source()
        }
        
        if self.text():
            resp['text'] = self.text()
            
        if self.link():
            resp['link'] = self.link()
            
        if self.location():
            location = self.location()
            resp_loc = {}
            if location.state():
                resp_loc['state'] = location.state()
            if location.city():
                resp_loc['city'] = location.city()
            if location.street():
                resp_loc['street'] = location.street()
            if location.building():
                resp_loc['building'] = location.building()
            if location.latitude():
                resp_loc['latitude'] = location.latitude()
            if location.longitude():
                resp_loc['longitude'] = location.longitude()
            resp['location'] = resp_loc
            
        return resp;
        
class Emergency:
    last_id = 0
    
    def __init__(self, based_on):
        Emergency.last_id += 1
        self.m_id       = Emergency.last_id
        self.m_pending  = based_on
        self.m_location = None
        self.m_level    = None # 0: Green, 1: Yellow, 2: Red
        self.m_approved = None
        self.m_approver = None # 0: Auto-approved, 1: User-approved, 2: Self-approved
        
    def user(self):
        return self.m_pending.user()
    
    def text(self):
        return self.m_pending.user()
        
    def link(self):
        return self.m_pending.link()

    def date(self):
        return self.m_pending.date()
        
    def location(self):
        if self.m_location:
            return self.m_location
        return self.m_pending.location()
        
    def level(self):
        return self.m_level
        
    def approvedOn(self):
        return self.m_approved

    def approvedBy(self):
        return self.m_approver
        
    def dictify(self):
        resp = {
            'id': self.m_id,
            'level': self.m_level,
            'approved': self.approvedOn(),
            'approver': self.approvedBy(),
            'initial' : self.m_pending.dictify()
        }
        
        if self.location():
            location = self.location()
            resp_loc = {}
            if location.state():
                resp_loc['state'] = location.state()
            if location.city():
                resp_loc['city'] = location.city()
            if location.street():
                resp_loc['street'] = location.street()
            if location.building():
                resp_loc['building'] = location.building()
            if location.latitude():
                resp_loc['latitude'] = location.latitude()
            if location.longitude():
                resp_loc['longitude'] = location.longitude()
            resp['location'] = resp_loc
        
        return resp
        
g_pending = []
g_waiting_pending = {}
g_emergencies = []

@app.route('/ers/post_new', methods=['POST'])
def add_pending():
    if not request.json:
        abort(400)
    
    pending = Pending()
    pending.m_user   = request.json['user']
    pending.m_date   = request.json['date']
    pending.m_source = request.json['source']
    
    pending.m_text = request.json.get('text', None)
    pending.m_link = request.json.get('link', None)
    
    print request.json
    if request.json.get('location', None):
        location = Location()
        loc_json = request.json['location']
        location.m_state     = loc_json.get('state', None)
        location.m_city      = loc_json.get('city', None)
        location.m_street    = loc_json.get('street', None)
        location.m_building  = loc_json.get('building', None)
        location.m_latitude  = loc_json.get('latitude', None)
        location.m_longitude = loc_json.get('longitude', None)
        pending.m_location = location
        
    g_pending.append(pending)
    return jsonify(pending.dictify()), 201
    
@app.route('/ers/pending/<int:pending_id>', methods=['GET'])
def get_pending(pending_id):
    pending = [pending for pending in g_pending if pending.m_id == pending_id]
    if not pending:
        abort(404)
    pending = pending[0]
        
    return jsonify(pending.dictify()), 201
    
@app.route('/ers/next_pending', methods=['POST'])
def get_next_pending():
    global g_pending
    if not g_pending:
        return jsonify({'ok':False, 'desc':'Pending queue is empty'}), 201
    pending = g_pending[0]
    g_pending = g_pending[1:]
    g_waiting_pending[pending.m_id] = pending
    
    return jsonify(pending.dictify()), 201
    
@app.route('/ers/approve/<int:pending_id>', methods=['POST'])
def approve_pending(pending_id):
    global g_pending
    global g_waiting_pending
    global g_emergencies
    pending = g_waiting_pending.get(pending_id, None)
    if not pending:
        return jsonify({'ok': False, 'desc':'Wrong pending id'}), 201
    
    del g_waiting_pending[pending_id]
    emergency = Emergency(pending)
    
    if request.json.get('location', None):
        loc_json = request.json['location']
        location = Location()
        location.m_state     = loc_json.get('state', None)
        location.m_city      = loc_json.get('city', None)
        location.m_street    = loc_json.get('street', None)
        location.m_building  = loc_json.get('building', None)
        location.m_latitude  = loc_json.get('latitude', None)
        location.m_longitude = loc_json.get('longitude', None)
        emergency.m_location = location
        
    emergency.m_level = request.json['level']
    emergency.m_approved = request.json['approved']
    emergency.m_approver = 1
    
    g_emergencies.append(emergency)
    
    return jsonify(emergency.dictify()), 201
    
@app.route('/ers/get_geodata', methods=['GET'])
def get_geodata():
    global g_emergencies
    resp = {"type":"FeatureCollection"}
    resp["features"] = [
        {
            "type": "Feature",
            "geometry": {
                "type":"Point",
                "coordinates": [
                    emergency.location().longitude(),
                    emergency.location().latitude()
                ]
            },
            "properties": {
                "level": emergency.level(),
                "approver": emergency.approvedBy(),
                "approved": emergency.approvedOn()
            }
        } for emergency in g_emergencies if emergency.location()
    ]
    
    return "{}".format(json.dumps(resp)), 201

if __name__ == '__main__':
    app.run(debug=True)

