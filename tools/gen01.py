from dataclasses import dataclass, fields
from datetime import date, timedelta
import random
import os
import json
import shutil
from typing import Any
from datetime import datetime,date
import hashlib

surnames = []
male_first_names = []
female_first_names = []

with open("tools/name/surname.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        surnames.append(line.strip())

with open("tools/name/male_first_name.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        male_first_names.append(line.strip())

with open("tools/name/female_first_name.txt", "r", encoding='utf-8') as f:
    for line in f.readlines():
        female_first_names.append(line.strip())

def getRandName(gender):
    if gender == 0:
        name = random.choice(surnames) + " " + random.choice(male_first_names) + " " + random.choice(male_first_names)
    else:
        name = random.choice(surnames) + " " + random.choice(female_first_names) + " " + random.choice(female_first_names)

    return nstr(name)


topics = ["Vật lí", "Toán học", "Địa lí", "Công nghệ Sinh học", "Công nghệ Thông tin"]

def getRandTopic():
    return random.choice(topics)

def getRandTitle(article_id):
    titles =[ nstr(f"Bài báo khoa học số {article_id}"),
             nstr(f"Bài báo số {article_id}"),
             nstr(f"Bài báo nghiên cứu số {article_id}"),
             nstr(f"Giải pháp số {article_id}"),
             ]

    return random.choice(titles)

def hash_password(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature


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
        else:
            value_list.append(str(field_value))

    result =  ",".join(value_list)
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


TblIdCounter = []
TblUser = []
TblArticle = []


class UserRole:
    admin = "Admin"
    author = "Author"


class ArticleStatus:
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


@dataclass
class Article:
    id: int
    title: nstr
    userId: int
    date_: date
    abstract_: nstr
    content: nstr
    topic: nstr
    status: str



@dataclass
class IdCounter:
    name: str
    count: int


@dataclass
class User:
    id: int
    name: nstr
    bday: date
    email: str
    username: str
    password: str
    role: str


admin = User(
    id=1,
    name=nstr("Quản trị viên"),
    bday=date(2001, 1, 1),
    email="genemaileric@gmail.com",
    username="admin",
    password=hash_password("admin"),
    role=UserRole.admin,
)

TblUser.append(admin)


class NextId:
    user = 2
    article = 1


number_of_users = 300

for _ in range(number_of_users):
    user_id = NextId.user
    demo_id = 999 + user_id
    user = User(
        id=user_id,
        name=nstr(getRandName(random.randint(0, 1))),
        bday=date(1970, 1, 1) + timedelta(days=random.randint(1, 365 * 20)),
        email=f"user{user_id}@gmail.com",
        username=f"{demo_id}",
        password=hash_password(f"{demo_id}"),
        role=UserRole.author,
    )
    NextId.user += 1
    TblUser.append(user)


current_date = date.today() - timedelta(days=1000)

for _ in range(random.randint(250, 1000)):
    user_id = random.choice(TblUser[1:]).id
    article_id = NextId.article
    current_date += timedelta(days=1)
    article = Article(
        id=article_id,
        title=nstr(getRandTitle(article_id)),
        userId=user_id,
        date_= min(current_date, date.today()),
        abstract_=nstr(f"This is an abstract of article {article_id}, Lorem Ipsum {article_id}."),
        content=nstr(f"This is some content of article {article_id}, Lorem ipsum dolor sit amet {article_id}, consectetur adipiscing elit {article_id}. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua {article_id}."),
        topic=nstr(getRandTopic()),
        status=random.choice(
            [ArticleStatus.pending, ArticleStatus.approved, ArticleStatus.rejected]
        ),
    )

    NextId.article += 1
    TblArticle.append(article)

TblIdCounter = [
    IdCounter(name="User", count=NextId.user),
    IdCounter(name="Article", count=NextId.article),
]

if not os.path.exists("data"):
    os.makedirs("data")
else:
    for filename in os.listdir("data"):
        file_path = os.path.join("data", filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Remove file or symlink
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Remove directory

json_output("User", TblUser)
json_output("Article", TblArticle)
json_output("IdCounter", TblIdCounter)

print("Generated successfully!")
