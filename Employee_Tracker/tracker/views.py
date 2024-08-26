from django.shortcuts import render
from .models import user_data
from .serializers import user_serializer,employee_data_serializer
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from sqlalchemy import create_engine
from rest_framework.decorators import api_view
import pandas as pd
from io import BytesIO
import hashlib
from .models import employee_details,mark_attendance_report,GeofencedArea,user_data
# import face_recognition
import math
# Create your views here.

Comapny_details = {
    'name':'Pharmagretech.LTD',
    'latitude':'',
    'longitude':'',
    'radius':'120'
}


class User_Registration(APIView):
    def hash_password(self,password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    def post(self,request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_name = data.get('username')
        try:
            user_check = user_data.objects.get(username=user_name)
            if user_check:
                return Response('username not available try another')
        except:
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password == confirm_password:
                pass_hash = self.hash_password(password)
                confirm_hash = pass_hash
                mobile_number = data.get('mobile_number')
                email_id = data.get('email')
                instance = user_data(first_name=first_name,last_name=last_name,username=user_name,email_id=email_id,password=pass_hash,confirm_password=confirm_hash,mobile_number=mobile_number)
                instance.save()
                return Response('user registered sucessfully')
            else:
                return Response('password doesnot match please try again')

class get_user_data(APIView):
    def get(self,request):
        db_data = user_data.objects.all()
        serializer = user_serializer(db_data,many=True)
        return Response(serializer.data)


class User_Login(APIView):
    def hash_password(self,password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    def post(self,request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            username_check = user_data.objects.get(username=username)
            if username_check:
                try:
                    hash_pass = self.hash_password(password)
                    password_check = user_data.objects.get(username=username,password=hash_pass)
                    if password_check:
                        return Response('user logged in sucessfully')
                    else:
                        return Response('password is incorrect')
                except:
                    return Response('Password is incorrect')
            else:
                return Response('Username does not match')
        except:
            return Response('Username does not match')
        

@api_view(['POST'])
def Upload_employee_details(request):
    uploaded_file = request.FILES.get('file')
    try:
        df_csv = pd.read_excel(BytesIO(uploaded_file.read()))
        print(df_csv)
        df_csv.columns = df_csv.columns.str.strip()
        df_csv.columns = df_csv.columns.str.strip().str.replace('-', '').str.replace(r'\s+', ' ', regex=True).str.replace(' ', '_')
        DATABASE_URI = 'sqlite:///db.sqlite3'

        engine = create_engine(DATABASE_URI)

        table_name = 'tracker_employee_details'
        df_csv.to_sql(table_name, con=engine, if_exists='append', index=False)

        engine.dispose()
        return Response('Employess Logged Sucessfully')
    except Exception as e:
        return Response({'error': str(e)}, status=400)
                
class Mark_attendance(APIView):
    def haversine_distance(self,lat1, lon1, lat2, lon2):
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
    
    def set_company_geolocation(self):
        instance = GeofencedArea(name=Comapny_details['name'],latitude=Comapny_details['latitude'],longitude=Comapny_details['longitude'],radius=Comapny_details['radius'])
        instance.save()

    def post(self,request):
        self.set_company_geolocation()
        data = request.data
        user_lat = float(data.get('latitude'))
        user_lon = float(data.get('longitude'))
        geofenced_area = GeofencedArea.objects.last()
        distance = self.haversine_distance(user_lat, user_lon, geofenced_area.latitude, geofenced_area.longitude)
        
        if distance <= geofenced_area.radius:
            employee_id = data.get('employee_id')
            employee_photo = data.get('employee_photo')
            mark = data.get('mark')
            employee_exists = employee_details.objects.get(employee_photo=employee_photo,employee_id=employee_id)
            try:
                if employee_exists:
                    if mark:
                        instance = mark_attendance_report(employee_id=employee_id,employee_photo=employee_photo,mark=mark)
                        instance.save()
                        return Response('Attendance Marked Sucessfully')
                    else:
                        return Response('please mark the attandance')
            except:
                return Response('Employee data not available please try again')
        else:
            return Response('Sorry but you are out of the office area')
        
class Declare_Geofenced_area(APIView):
    def post(self,request):
        data = request.data
        company_name = data.get('company_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius')
        instance = GeofencedArea(name=company_name,latitude=latitude,longitude=longitude,radius=radius)
        instance.save()
        return Response('Area Marked Sucessfully')

# @api_view(['POST'])
# def upload_images(request):
#     images = request.FILES.getlist('images')
#     def encode_face(image_path):
#         image = face_recognition.load_image_file(image_path)
#         encodings = face_recognition.face_encodings(image)
#         if encodings:
#             return encodings[0]
#         else:
#             raise ValueError("No face found in the image.")
#     for image in images:
#         filename = image.name
#         name_without_extension = filename.rsplit('.', 1)[0]
#         if name_without_extension.startswith("EMP_"):
#             employee_id = name_without_extension[4:]
#             face_recognition_encoding = encode_face(image)
#             face_instance = employee_details.objects.get(employee_id=employee_id)
#             if face_instance:
#                 face_instance.employee_image_encodeing = face_recognition_encoding
#                 face_instance.save()
#             else:
#                 return Response(f"Employee with employee id {employee_id} does not exists")
#         else:
#             employee_id = None
#             print(f"Processing image for employee ID: {employee_id}")
#             pass

#     return Response("Images uploaded successfully")