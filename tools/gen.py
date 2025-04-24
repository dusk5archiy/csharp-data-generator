import random
from datetime import datetime, timedelta

stu_ids = list(range(1001, 1501))
tch_ids = list(range(1501, 2001))
genders = list(range(0, 2))

stu_offset = 1000
tch_offset = 1500

sbj_ids = list(range(1, 11))

durations = [45, 60, 90, 120] 
count_range = list(range(3, 5))
slot_range = list(range(42))

generated_numbers = set()
generated_addr = set()

# =============================================================================
# Open name/surname.txt
surnames = []
male_first_names = []
female_first_names = []
street_names = []

with open("tools/name/surname.txt", "r", encoding = 'utf-8') as f:
    for line in f.readlines():
        surnames.append(line.strip())

with open("tools/name/male_first_name.txt", "r", encoding = 'utf-8') as f:
    for line in f.readlines():
        male_first_names.append(line.strip())

with open("tools/name/female_first_name.txt", "r", encoding = 'utf-8') as f:
    for line in f.readlines():
        female_first_names.append(line.strip())

with open("tools/name/street.txt", "r", encoding = 'utf-8') as f:
    for line in f.readlines():
        street_names.append(line.strip())

# =============================================================================
temp_subject_id = 0

def gen_sbj_id():
    global temp_subject_id
    temp_subject_id += 1
    return temp_subject_id

def gen_sbj_group(sbj_name, _from, _to, price):
    return [(gen_sbj_id(), sbj_name, x, price) for x in range(_from, _to + 1)]

subject_groups = [
    gen_sbj_group("Toán", 6, 9, 55000), 
    gen_sbj_group("Toán", 10, 12, 65000), 
    gen_sbj_group("Ngữ Văn", 6, 9, 50000), 
    gen_sbj_group("Ngữ Văn", 10, 12, 60000), 
    gen_sbj_group("Tiếng Anh", 6, 9, 50000), 
    gen_sbj_group("Tiếng Anh", 10, 12, 60000), 
    gen_sbj_group("Vật lí", 6, 9, 53000), 
    gen_sbj_group("Vật lí", 10, 12, 63000), 
    gen_sbj_group("Hóa học", 8, 9, 53000), 
    gen_sbj_group("Hóa học", 10, 12, 63000), 
    gen_sbj_group("Sinh học", 10, 12, 63000), 
]
g_sbj_rows = []

for sbj_group in subject_groups:
    for subject in sbj_group:
        g_sbj_rows.append(subject)

g_tch_sbj_rows = []

# =============================================================================
def get_grade_from_birthday(birthday):
    year = int(birthday.split("-")[0])
    return 2019 - year

# =============================================================================
def generate_phone_number():
    while True:
        phone_number = f"09"
        for i in range(8):
            phone_number += str(random.randint(0, 9))
        
        if phone_number not in generated_numbers:
            generated_numbers.add(phone_number)
            return phone_number

def generate_addr():
    while True:
        num = random.randint(1, 500)
        street_name = random.choice(street_names)
        addr = f"{num} {street_name}"
        if addr not in generated_addr:
            generated_addr.add(addr)
            return addr

def generate_birthday(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    result = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return f"{result.year}-{result.month}-{result.day}"

def generate_acc_rows():
    output_acc_rows = []

    output_acc_rows.append((0, "admin", "admin", 3))

    # for stu_id in stu_ids:
    #     name = f"stu{stu_id - stu_offset}"
    #     output_acc_rows.append((stu_id,name,name,1 ))
    #
    # for tch_id in tch_ids:
    #     name = f"tch{tch_id - tch_offset}"
    #     output_acc_rows.append((tch_id, name,name,2 ))

    return output_acc_rows

g_usr_rows = []
g_stu_rows = []
g_tch_rows = []
g_stu_sbj_rows = []

def generate_usr_rows():
    for stu_id in stu_ids:
        username = f"stu{stu_id - stu_offset}"
        password =  username
        acctype = 1
        name = ""
        gender = random.choice(genders)
        if gender == 0:
            name = random.choice(surnames) + " " + random.choice(male_first_names) + " " + random.choice(male_first_names)
        else:
            name = random.choice(surnames) + " " + random.choice(female_first_names) + " " + random.choice(female_first_names)

        birthday = generate_birthday("2007-1-1", "2013-12-31");
        phone_number = generate_phone_number()
        grade = get_grade_from_birthday(birthday)

        address = generate_addr()
        g_stu_rows.append((stu_id, username, password, acctype, name, gender, birthday, phone_number, address, grade))

        sbj_list = [x for x in g_sbj_rows if x[2] == grade]
        for subject in sbj_list:
            if random.random() < 0.75:
                count = random.choice(count_range)
                g_stu_sbj_rows.append((stu_id, subject[0], count))

    for tch_id in tch_ids:
        username = f"tch{tch_id - tch_offset}"
        password =  username
        acctype = 2
        name = ""
        gender = random.choice(genders)

        if gender == 0:
            name = random.choice(surnames) + " " + random.choice(male_first_names) + " " + random.choice(male_first_names)
        else:
            name = random.choice(surnames) + " " + random.choice(female_first_names) + " " + random.choice(female_first_names)

        birthday = generate_birthday("1980-1-1", "2003-12-31");
        phone_number = generate_phone_number()
        
        address = generate_addr()

        g_tch_rows.append((tch_id, username, password, acctype, name, gender, birthday, phone_number, address))

        subject_group = random.choice(subject_groups)
        for subject in subject_group:
            g_tch_sbj_rows.append((tch_id, subject[0]))


# def generate_tch_rows():
#     tch_data = []
#     for tch_id in tch_ids:
#         tch_data.append((tch_id,))
#
#     return tch_data

def generate_usr_intervals():
    data = []
    for id in stu_ids + tch_ids:
        for slot in slot_range:
            if random.random() < 0.2:
                data.append((id, slot // 6, slot % 6))
    return data

def generate_stu_sbj_rows():
    student_subject_data = []
    for stu_id in stu_ids:
        for sbj_id in sbj_ids:
            if random.random() < 0.5:
                count = random.choice(count_range)
                student_subject_data.append((stu_id, sbj_id, count))

    return student_subject_data

# =============================================================================
generate_usr_rows()

with open("data/admin.csv", "w", encoding = 'utf-8') as f:
    rows = generate_acc_rows()
    for data in rows:
        f.write(','.join(map(str, data)) + '\n')
with open("data/stu.csv", "w", encoding = 'utf-8') as f:
    for data in g_stu_rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/tch.csv", "w", encoding = 'utf-8') as f:
    for data in g_tch_rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/usr_avai_slot.csv", "w", encoding = 'utf-8') as f:
    rows = generate_usr_intervals()
    for data in rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/stu_sbj.csv", "w", encoding = 'utf-8') as f:
    for data in g_stu_sbj_rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/sbj.csv", "w", encoding = 'utf-8') as f:
    for data in g_sbj_rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/tch_sbj.csv", "w", encoding = 'utf-8') as f:
    for data in g_tch_sbj_rows:
        f.write(','.join(map(str, data)) + '\n')

with open("data/ctrct.csv", "w", encoding='utf-8') as f:
    pass

with open("data/ctrct_slot.csv", "w", encoding='utf-8') as f:
    pass

with open("data/id_counter.csv", "w", encoding='utf-8') as f:
    f.write("2001")

# =============================================================================


# EOF #
