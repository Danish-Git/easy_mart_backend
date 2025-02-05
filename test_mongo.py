from mongoengine import connect
from mongoengine import Document, StringField

try:
    connect(
        db='easy_mart',
        username='EasyMart',
        password='Qazwsx098712',
        host='147.93.96.233',
        port=27017,
        authentication_source='admin'  # Try changing this to 'easy_mart' if it fails
    )
    print("Connected to MongoDB successfully!")
    
    # Simple query to verify
    class User(Document):
        phone = StringField(required=True)
        otp = StringField()

    user = User.objects.first()
    print(f"Sample user found: {user.phone if user else 'No users found.'}")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
