from flask import Flask
from flask_restplus import Resource, Api,fields

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app, version='1.0', title='Message API',
    description='A simple message API',
)
ns = api.namespace('message', description='Message Operations')

message = api.model('Message', {
    'id': fields.Integer(readOnly=True, description='The message unique identifier'),
    'content': fields.String(required=True, description='The message content'),
    'isPalindrome': fields.Boolean(description= "True is the content is palindrome, otherwise false.")
})

# @api.route('/hello')                   #  Create a URL route to this resource
# class HelloWorld(Resource):            #  Create a RESTful resource
#     def get(self):                     #  Create GET endpoint
#         return {'hello': 'world'}

class Message(object):
    def __init__(self):
        self.counter = 0
        self.messages = []
    def isPalindrome(self, message):
        i = 0
        j = len(message)-1
        print(message)
        while(i < j):
            if not message[i] == message[j]:
                return False
            i+=1
            j-=1
        return True
    def get(self, id):
        for message in self.messages:
            if message['id'] == id:
                return message
        api.abort(404, "Message {} doesn't exist".format(id))

    def create(self, data):
        message = data
        message['id'] = self.counter = self.counter + 1
        message['isPalindrome'] = self.isPalindrome(message['content'])
        self.messages.append(message)
        return message

    def update(self, id, data):
        message = self.get(id)
        message.update(data)
        message['isPalindrome'] = self.isPalindrome(message['content'])
        return message

    def delete(self, id):
        message = self.get(id)
        self.messages.remove(message)

Message = Message()

@ns.route('/')
class MessageList(Resource):
    '''Shows a list of all messages, and lets you POST to add new messages'''
    @ns.doc('list_messages')
    @ns.marshal_list_with(message)
    def get(self):
        '''List all messages'''
        return Message.messages

@ns.route('/submit_message')
class CreateMessage(Resource):
    @ns.doc('post_message')
    @ns.expect(message)
    @ns.marshal_with(message, code=201)
    def post(self):
        '''Post a new message'''
        return Message.create(api.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Message not found')
@ns.param('id', 'The message identifier')
class SingleMessage(Resource):
    '''Show a single message and lets you delete them'''
    @ns.doc('get_message')
    @ns.marshal_with(message)
    def get(self, id):
        '''Fetch a given resource'''
        return Message.get(id)

    @ns.doc('delete_message')
    @ns.response(204, 'Message deleted')
    def delete(self, id):
        '''Delete a message given its identifier'''
        Message.delete(id)
        return '', 204

    @ns.expect(message)
    @ns.marshal_with(message)
    def put(self, id):
        '''Update a message given its identifier'''
        return Message.update(id, api.payload)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80,debug=True)                #  Start a development server