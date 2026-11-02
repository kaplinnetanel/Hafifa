from sqlalchemy import create_engine,text,select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,Session

engine = create_engine("sqlite:///test.db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

print("Tables created!")



with Session(engine) as session:
    user = User(name = "netanel", age = 25)

    session.add(user)
    session.commit()

    print(user.id)

    stmt = select(User).where(User.id == 2)
    users = session.scalars(stmt).all()

    for user in users:
        print(user.id, user.name, user.age)

    