from dataclasses import dataclass, fields
from datetime import date, timedelta
import random
import os
import json
import shutil
from typing import Any
from datetime import datetime,date

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
    name=nstr("admin"),
    bday=date(2001, 1, 1),
    email="genemaileric@gmail.com",
    username="admin",
    password="admin",
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
        name=nstr(f"User {demo_id}"),
        bday=date(1970, 1, 1) + timedelta(days=random.randint(1, 365 * 20)),
        email=f"user{user_id}@gmail.com",
        username=f"{demo_id}",
        password=f"{demo_id}",
        role=UserRole.author,
    )
    NextId.user += 1
    TblUser.append(user)

    for _ in range(random.randint(1, 200)):
        article_id = NextId.article
        article = Article(
            id=article_id,
            title=nstr(f"The Article {article_id}"),
            userId=user_id,
            date_=date.today(),
            abstract_=nstr(f"This is an abstract of article {article_id}"),
            content=nstr(f"This is some content of article {article_id}"),
            topic=nstr("Science"),
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
