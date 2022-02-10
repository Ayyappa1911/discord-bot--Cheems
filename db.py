#!/usr/bin/python

import sqlite3

class my_data_base:
  def __init__(self):
    self.conn  = sqlite3.connect('test.db');

    self.conn.execute('''CREATE TABLE DB
      ( NAME     TEXT   NOT NULL,
        MATTER   TEXT   NOT NULL );''');

  def add(self,name,message):
    self.conn.execute("INSERT INTO DB (NAME, MATTER) VALUES (%r,%r)" %(name,message));
    self.conn.commit
  
  def display(self,name):
    self.temp = self.conn.execute("SELECT name , matter from DB");
    self.lst = []
    for self.row in self.temp:
      if(self.row[0] == name):
        self.lst.append((self.row[1]))
    return self.lst

