# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:09:42 2023

@author: Salman Khan
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
import bcrypt
import uuid

Base = declarative_base()

engine = create_engine('sqlite:///KnowledgeBase.db')

Session = sessionmaker(bind=engine)
session = Session()

class MaskTable(Base):
    __tablename__ = 'maskTable'
    mask = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    
    mapping_json = relationship('MappingJSON', back_populates='mask', cascade='all, delete-orphan', single_parent=True)

class ComponentTable(Base):
    __tablename__ = 'componentTable'
    # id = Column(Integer, primary_key=True)
    component = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    description = Column(String)
    
    mapping_json = relationship('MappingJSON', back_populates='component', cascade='all, delete-orphan', single_parent=True)
    exceptions = relationship('ExceptionTable', back_populates='component', cascade='all, delete-orphan', single_parent=True)

class MappingJSON(Base):
    __tablename__ = 'mappingJSON'
    # id = Column(Integer, primary_key=True)
    mask_index = Column(String, ForeignKey('maskTable.mask'))
    component_index = Column(String, ForeignKey('componentTable.component'))
    component_value = Column(Integer)

    mask = relationship('MaskTable', foreign_keys=[mask_index], back_populates='mapping_json')
    component = relationship('ComponentTable', foreign_keys=[component_index], back_populates='mapping_json')
    
    __table_args__ = (
        PrimaryKeyConstraint('mask_index','component_value'),
    )
    
    def __eq__(self, other):
        if isinstance(other, MappingJSON):
            return (
                self.mask_index == other.mask_index and
                self.component_index == other.component_index and
                self.component_value == other.component_value
            )
        return NotImplemented

class UserRole(Base):
    __tablename__ = 'rolesTable'
    RoleName = Column(String, primary_key=True)

    def __repr__(self):
        return f"<UserRole(name='{self.RoleName}')>"

class User(Base):
    __tablename__ = 'usersTable'
    id = Column(Integer, primary_key=True)
    FullName = Column(String)
    UserName = Column(String, unique=True)
    Email = Column(String, unique=True)
    Password = Column(String(60))
    Role = Column(String, ForeignKey('rolesTable.RoleName'))
    # Status = Column(String)

    role = relationship("UserRole")
    exception_Table = relationship('ExceptionTable', back_populates='user', cascade='all', single_parent=True)


    def __repr__(self):
        return f"<User(username='{self.UserName}', role_id={self.Role})>"

class ExceptionTable(Base):
    __tablename__ = 'exceptionTable'
    UserName = Column(String, ForeignKey('usersTable.UserName'))
    Timestamp = Column(String)
    Run = Column(String)
    Name_ID = Column(Integer) 
    Component = Column(String, ForeignKey('componentTable.component'))
    Token = Column(String)
    Mask_Token = Column(String)
    Component_index = Column(Integer)
    MapCreation_Index = Column(Integer, ForeignKey('mapCreationTable.ID'))
    
    
    user = relationship('User', foreign_keys=[UserName], back_populates='exception_Table')
    component = relationship('ComponentTable', foreign_keys=[Component], back_populates='exceptions')
    mask_index = relationship('MapCreationTable', foreign_keys=[MapCreation_Index], back_populates='map_creation')

    __table_args__ = (
        PrimaryKeyConstraint('UserName','Timestamp','Run', 'Name_ID', 'Component', 'Component_index'),
    )

class MapCreationTable(Base):
    __tablename__ = 'mapCreationTable'
    ID = Column(String, primary_key = True, default = lambda: uuid.uuid4().hex) 
    Name_Input = Column(String)
    Mask = Column(String)
    
    map_creation = relationship('ExceptionTable', back_populates='mask_index', cascade='all', single_parent=True)

class ClueTable(Base):
    __tablename__ = 'clueTable'
    component_desc = Column(String, primary_key=True)
    token = Column(String)
    

Base.metadata.create_all(engine)
# Base.metadata.create_all(engine)

# new_roles = [
#     UserRole(RoleName='Admin'),
#     UserRole(RoleName='Committee Member'),
#     UserRole(RoleName='General User')
# ]

# admin_role = session.query(UserRole).filter_by(RoleName='Admin').one_or_none()
# committee_role = session.query(UserRole).filter_by(RoleName='Committee Member').one_or_none()
# general_user_role = session.query(UserRole).filter_by(RoleName='General User').one_or_none()

# new_users = [
#     User(FullName='Admin', UserName='admin', Email='admin@gmail.com', Password='123', Role=admin_role.RoleName),
#     User(FullName='Committee Member 1', UserName='committee1', Email='committee1@gmail.com', Password='123', Role=committee_role.RoleName),
#     User(FullName='Committee Member 2', UserName='committee2', Email='committee2@gmail.com', Password='123', Role=committee_role.RoleName),
#     User(FullName='General', UserName='general', Email='general@gmail.com', Password='123', Role=general_user_role.RoleName)
# ]


# # # # # new_user = User(FullName='Admin', UserName='admin', Email='admin@gmail.com', Password='123', Status='Active', Role=admin_role.RoleName)
# # session.add_all(new_roles)
# session.add_all(new_users)
# session.commit()

# def hash_password(password):
#     """ Hash a password using bcrypt """
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode(), salt)

# def update_passwords():
#     try:
#         # Fetch all users
#         users = session.query(User).all()
#         for user in users:
#             # Hash each user's password
#             hashed_password = hash_password(user.Password)
#             user.Password = hashed_password
#             session.add(user)

#         # Commit changes
#         session.commit()
#         print("Passwords updated successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         session.rollback()

# # # Call the function to update passwords
# update_passwords()

# # # Close the session
# session.close()

# components = [
#     ComponentTable(component="USAD_SNO", description="Street Number"),
#     ComponentTable(component="USAD_SNM", description="Street Name"),
#     ComponentTable(component="USAD_SFX", description="Street Suffix"),
#     ComponentTable(component="USAD_ANM", description="Secondary Name Name"),
#     ComponentTable(component="USAD_ANO", description="Secondary Name Number"),
#     ComponentTable(component="USAD_CTY", description="City Name"),
#     ComponentTable(component="USAD_STA", description="State Name"),
#     ComponentTable(component="USAD_ZIP", description="Zip Code"),
#     ComponentTable(component="USAD_SPR", description="Street Pre-Directional"),
#     ComponentTable(component="USAD_BNM", description="Box Name"),
#     ComponentTable(component="USAD_BNO", description="Box Number"),
#     ComponentTable(component="USAD_SPT", description="Street Post-Directional"),
#     ComponentTable(component="USAD_ZP4", description="Zip 4 Code"),
#     ComponentTable(component="USAD_RNM", description="Route Name"),
#     ComponentTable(component="USAD_RNO", description="Route Number"),
#     ComponentTable(component="USAD_ORG", description="Organization Name"),
#     ComponentTable(component="USAD_MGN", description="Military Rd Number"),
#     ComponentTable(component="USAD_MDG", description="Military Rd Name"),
#     ComponentTable(component="USAD_HNO", description="Highway Number"),
#     ComponentTable(component="USAD_HNM", description="Highway Name"),
#     ComponentTable(component="USAD_NA", description="Not Selected")
# ]

# session.add_all(components)
# session.commit()