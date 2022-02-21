#!/usr/bin/python

import sqlite3
from os import path

class my_data_base:
  def __init__(self):
    self.conn  = sqlite3.connect('test.db');

    if( path.exists('test.db') == False):
      self.conn.execute('''CREATE TABLE DB
        ( NAME     TEXT   NOT NULL,
          MATTER   TEXT   NOT NULL );''');
    else:
      self.conn.execute('''SELECT * from DB ''');

  def add(self,name,message):
    self.conn.execute("INSERT INTO DB (NAME, MATTER) VALUES (%r,%r)" %(name,message));
    self.conn.commit()

  def display(self,name):
    self.temp = self.conn.execute("SELECT name , matter from DB");
    self.lst = []
    for self.row in self.temp:
      if(self.row[0] == name):
        self.lst.append((self.row[1]))
    return self.lst
    self.conn.commit()

  def delete(self,name,no):
    self.temp = self.conn.execute("SELECT name , matter from DB");
    count = 0;
    for self.row in self.temp:
      if(self.row[0]==name):
        count += 1
      if(self.row[0] == name and count == no):
        self.conn.execute("DELETE FROM DB WHERE name== %r AND matter== %r " %(name,self.row[1]));
        break; 
      self.conn.commit()
   
  def clear(self,name):
    self.conn.execute("DELETE FROM DB WHERE name == %r" %(name));
    self.conn.commit()