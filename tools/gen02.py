from dataclasses import dataclass, fields
from datetime import date, timedelta, datetime, time
import random
import os
import json
import shutil
import hashlib
from typing import Any

class nstr(str):
    pass

def conv(instance: Any) -> str:
    value_list = []
    for field in fields(instance):
        field_name = field.name
        field_value = getattr(instance, field_name)
        if field_value is None:
            value_list.append("NULL")
        elif isinstance(field_value, nstr):
            value_list.append(f"N'{field_value}'")
        elif isinstance(field_value, str):
            value_list.append(f"'{field_value}'")
        elif isinstance(field_value, date):
            value_list.append(f"'{field_value.year}-{field_value.month:02d}-{field_value.day:02d}'")
        elif isinstance(field_value, bool):
            value_list.append(str(field_value).upper())
        elif isinstance(field_value, datetime):
            value_list.append(f"'{field_value.year}-{field_value.month:02d}-{field_value.day:02d} {field_value.hour:02d}:{field_value.minute:02d}'")
        elif isinstance(field_value, time):
            value_list.append(f"'{field_value.hour:02d}:{field_value.minute:02d}'")
        else:
            value_list.append(str(field_value))
    
    result = ",".join(value_list)
    return result

def json_output(file_name, lst):
    with open(f"data/{file_name}.json", "w", encoding="utf-8", newline="") as f:
        f.write(
            "[" 
            + ",\n".join(
                json.dumps(conv(obj), ensure_ascii=False) for obj in lst
            )
            + "]"
        )

# Load names data for generating realistic data
surnames = []
male_first_names = []
female_first_names = []
street_names = []

with open("tools/name/surname.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        surnames.append(line.strip())

with open("tools/name/male_first_name.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        male_first_names.append(line.strip())

with open("tools/name/female_first_name.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        female_first_names.append(line.strip())

with open("tools/name/street.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        street_names.append(line.strip())

# Set to prevent duplicate values
generated_numbers = set()

# Contract status constants
class ContractStatus:
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

shifts = [
    (7, 30, 9, 0),
    (9, 30, 11, 0),
    (13, 30, 15, 0),
    (15, 30, 17, 0),
    (17, 30, 19, 0),
    (19, 30, 21, 0),
]

# Define the data classes based on the class diagram
@dataclass
class Admin:
    id_: int
    tenDangNhap: str
    matKhau: str

@dataclass
class HocVien:
    id_: int
    tenDangNhap: str
    matKhau: str
    hoTen: nstr
    ngaySinh: date
    diaChi: nstr
    khoiLop: int

@dataclass
class GiaSu:
    id_: int
    tenDangNhap: str
    matKhau: str
    hoTen: nstr
    ngaySinh: date
    khuVuc: nstr

@dataclass
class KhoaHoc:
    id_: int
    tenKhoaHoc: nstr
    tenMonHoc: nstr
    khoiLop: int
    soBuoi: int
    hocPhi: int

@dataclass
class TGBHocVien:
    id_HocVien: int
    tdiemBatDau: time
    tdiemKetThuc: time

@dataclass
class TGBGiaSu:
    id_GiaSu: int
    tdiemBatDau: time
    tdiemKetThuc: time

@dataclass
class HopDong:
    id_: int
    id_HocVien: int
    id_GiaSu: int
    id_KhoaHoc: int
    trangThai: str

@dataclass
class TGBHopDong:
    id_HopDong: int
    tdiemBatDau: time
    tdiemKetThuc: time

@dataclass
class DayHoc:
    id_GiaSu: int
    id_KhoaHoc: int

@dataclass
class IdCounter:
    name: str
    count: int

# Lists to hold generated data
TblAdmin = []
TblHocVien = []
TblGiaSu = []
TblKhoaHoc = []
TblTGBHocVien = []
TblTGBGiaSu = []
TblHopDong = []
TblTGBHopDong = []
TblDayHoc = []
TblIdCounter = []

# Generate phone number function
def generate_phone_number():
    while True:
        phone_number = f"09"
        for i in range(8):
            phone_number += str(random.randint(0, 9))
        
        if phone_number not in generated_numbers:
            generated_numbers.add(phone_number)
            return phone_number

# Generate random address
def generate_address():
    num = random.randint(1, 500)
    street_name = random.choice(street_names)
    return f"{num} {street_name}"

# Generate random Vietnamese name
def generate_vietnamese_name(gender):
    if gender == 0:
        name = random.choice(surnames) + " " + random.choice(male_first_names) + " " + random.choice(male_first_names)
    else:
        name = random.choice(surnames) + " " + random.choice(female_first_names) + " " + random.choice(female_first_names)

    return nstr(name)

# Generate hashed password using SHA-256
def hash_password(password):
    # Create SHA-256 hash of password
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# ID counter class
class NextId:
    hocvien = 1001  # Starting student ID at 1001
    giasu = 2001    # Starting tutor ID at 2001
    khoahoc = 1
    hopdong = 1

# Calculate appropriate birth year based on grade level (for 2025)
def calculate_birth_year(grade):
    # In Vietnam, children typically start grade 1 at age 6
    # So in 2025, a 1st grader would typically be born in 2019
    return 2025 - (grade + 5)

# Generate Admin data
admin = Admin(
    id_=1,
    tenDangNhap="admin",
    matKhau=hash_password("admin")
)
TblAdmin.append(admin)

# Generate HocVien data
num_hoc_vien = 50
for _ in range(num_hoc_vien):
    hv_id = NextId.hocvien
    gender = random.randint(0, 1)
    name = generate_vietnamese_name(gender)
    
    # Generate a grade level first
    klop = random.randint(1, 12)
    
    # Calculate appropriate birth year based on grade level
    birth_year = calculate_birth_year(klop)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = date(birth_year, birth_month, birth_day)
    
    # Username is string version of ID
    username = str(hv_id)
    # Password is hashed username
    password = hash_password(username)
    
    hoc_vien = HocVien(
        id_=hv_id,
        tenDangNhap=username,
        matKhau=password,
        hoTen=name,
        ngaySinh=birth_date,
        diaChi=nstr(generate_address()),
        khoiLop=klop
    )
    
    # Generate time blocks for this student
    num_time_blocks = random.randint(1, 3)
    for _ in range(num_time_blocks):
        # Select a random shift from the shifts list
        shift = random.choice(shifts)
        start_hour, start_minute, end_hour, end_minute = shift
        
        # Create time objects without date
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
        
        time_block = TGBHocVien(
            id_HocVien=hv_id,
            tdiemBatDau=start_time,
            tdiemKetThuc=end_time
        )
        
        TblTGBHocVien.append(time_block)
    
    TblHocVien.append(hoc_vien)
    NextId.hocvien += 1

# Generate GiaSu data
num_gia_su = 30
for _ in range(num_gia_su):
    gs_id = NextId.giasu
    gender = random.randint(0, 1)
    name = generate_vietnamese_name(gender)
    
    birth_year = random.randint(1985, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = date(birth_year, birth_month, birth_day)
    
    areas = ["Quận Thanh Khê", "Quận Liên Chiểu", "Quận Ngũ Hành Sơn", "Quận Sơn Trà", "Quận Hải Châu", "Quận Liên Chiểu", "Quận Cẩm Lệ"]
    
    # Username is string version of ID
    username = str(gs_id)
    # Password is hashed username
    password = hash_password(username)
    
    gia_su = GiaSu(
        id_=gs_id,
        tenDangNhap=username,
        matKhau=password,
        hoTen=name,
        ngaySinh=birth_date,
        khuVuc=nstr(random.choice(areas))
    )
    
    # Generate time blocks for this tutor
    num_time_blocks = random.randint(2, 5)
    for _ in range(num_time_blocks):
        # Select a random shift from the shifts list
        shift = random.choice(shifts)
        start_hour, start_minute, end_hour, end_minute = shift
        
        # Create time objects without date
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
        
        time_block = TGBGiaSu(
            id_GiaSu=gs_id,
            tdiemBatDau=start_time,
            tdiemKetThuc=end_time
        )
        
        TblTGBGiaSu.append(time_block)
    
    TblGiaSu.append(gia_su)
    NextId.giasu += 1

# Generate KhoaHoc data
subjects = [
    "Toán", "Ngữ Văn", "Tiếng Anh", "Vật Lý", "Hóa Học", 
    "Sinh Học", "Lịch Sử", "Địa Lý", "Tin Học"
]

# Generate a range of fees from 300,000 to 400,000 with steps of 5,000
fee_options = list(range(300000, 400001, 5000))

num_khoa_hoc = 20
for _ in range(num_khoa_hoc):
    kh_id = NextId.khoahoc
    subject = random.choice(subjects)
    grade = random.randint(1, 12)
    # Adjust the number of sessions to be 3 or 4
    sessions = random.randint(3, 4)
    # Select a fee from the predefined range
    fee = random.choice(fee_options)
    
    khoa_hoc = KhoaHoc(
        id_=kh_id,
        tenKhoaHoc=nstr(f"{subject} {grade}"),
        tenMonHoc=nstr(subject),
        khoiLop=grade,
        soBuoi=sessions,
        hocPhi=fee
    )
    
    TblKhoaHoc.append(khoa_hoc)
    NextId.khoahoc += 1

# Generate DayHoc relationships
for gs in TblGiaSu:
    # Each tutor teaches 1-4 random courses
    num_courses = random.randint(1, 4)
    course_ids = random.sample([kh.id_ for kh in TblKhoaHoc], min(num_courses, len(TblKhoaHoc)))
    
    for kh_id in course_ids:
        day_hoc = DayHoc(
            id_GiaSu=gs.id_,
            id_KhoaHoc=kh_id
        )
        
        TblDayHoc.append(day_hoc)

# Generate HopDong and TGBHopDong
num_hop_dong = min(40, num_hoc_vien * num_gia_su // 3)  # Limit the number of contracts
statuses = [ContractStatus.PENDING, ContractStatus.CONFIRMED, ContractStatus.COMPLETED, ContractStatus.CANCELLED]

for _ in range(num_hop_dong):
    hd_id = NextId.hopdong
    
    # Randomly choose a student
    hv = random.choice(TblHocVien)
    
    # Find courses that match this student's grade level
    matching_courses = [kh for kh in TblKhoaHoc if kh.khoiLop == hv.khoiLop]
    
    # If no matching courses, skip this contract
    if not matching_courses:
        continue
        
    # Find tutors who teach courses for this student's grade
    valid_tutors = []
    for kh in matching_courses:
        for day_hoc in TblDayHoc:
            if day_hoc.id_KhoaHoc == kh.id_:
                valid_tutors.append((day_hoc.id_GiaSu, kh.id_))
    
    # If no valid tutors, skip this contract
    if not valid_tutors:
        continue
    
    # Choose a random tutor and the course they teach
    gs_id, kh_id = random.choice(valid_tutors)
    
    hop_dong = HopDong(
        id_=hd_id,
        id_HocVien=hv.id_,
        id_GiaSu=gs_id,
        id_KhoaHoc=kh_id,
        trangThai=random.choice(statuses)
    )
    
    # Get the number of sessions from the course
    course_sessions = 0
    for kh in TblKhoaHoc:
        if kh.id_ == kh_id:
            course_sessions = kh.soBuoi
            break
    
    # Generate exactly the number of time blocks specified in the course
    for i in range(course_sessions):
        # Generate time blocks for this contract using a random shift
        shift = random.choice(shifts)
        start_hour, start_minute, end_hour, end_minute = shift
        
        # Create time objects without date
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
        
        time_block = TGBHopDong(
            id_HopDong=hd_id,
            tdiemBatDau=start_time,
            tdiemKetThuc=end_time
        )
        
        TblTGBHopDong.append(time_block)
    
    TblHopDong.append(hop_dong)
    NextId.hopdong += 1

# Set up IdCounter
TblIdCounter = [
    IdCounter(name="HocVien", count=NextId.hocvien),
    IdCounter(name="GiaSu", count=NextId.giasu),
    IdCounter(name="KhoaHoc", count=NextId.khoahoc),
    IdCounter(name="HopDong", count=NextId.hopdong),
]

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Output data to JSON files
json_output("Admin", TblAdmin)
json_output("HocVien", TblHocVien)
json_output("GiaSu", TblGiaSu)
json_output("KhoaHoc", TblKhoaHoc)
json_output("TGBHocVien", TblTGBHocVien)
json_output("TGBGiaSu", TblTGBGiaSu)
json_output("HopDong", TblHopDong)
json_output("TGBHopDong", TblTGBHopDong)
json_output("DayHoc", TblDayHoc)
json_output("IdCounter", TblIdCounter)

print("Data generation completed successfully!")