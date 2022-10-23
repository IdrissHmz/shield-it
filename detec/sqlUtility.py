from sqlalchemy import create_engine

import pymysql
import psycopg2
from sqlalchemy.types import Text,VARCHAR
import pandas as pd




          

 
def persistDataFrameToMySql(df):

    tableName   = "burnout_test_persistance"
    sqlEngine       = create_engine('mysql+pymysql://root:123@192.168.1.9:3306/testdb', pool_recycle=3600)

    dbConnection    = sqlEngine.connect()

    try:

        frame           = df.to_sql(tableName, dbConnection, if_exists='fail', dtype={'employee_id': VARCHAR(df.index.get_level_values('employee_id').str.len().max())});

    except ValueError as vx:

        print(vx)

    except Exception as ex:   

        print(ex)

    else:

        print("Table %s created successfully."%tableName);   

    finally:

        dbConnection.close()




def loadDataFrameFromPostgres():

    #sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    alchemyEngine   = create_engine('postgresql+psycopg2://postgres:1234@db', pool_recycle=3600);

    dbConnection    = alchemyEngine.connect()

    frame           = pd.read_sql("select * from filtered_mini", dbConnection);

    

    #pd.set_option('display.expand_frame_repr', False)

    

    

    dbConnection.close()

    return frame


def populatePostgress():

    conn = psycopg2.connect(database="postgres",
                            user='postgres', password='admin', 
                            host='127.0.0.1', port='5432'
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    
    sql = '''CREATE TABLE EMAILS( id int,file varchar(30),message_id varchar(30),date varchar(30),from_email varchar(30)\
    ,to_email varchar(30),body varchar(255),subject varchar(30)\
    ,cc varchar(30),bcc varchar(30),if_forwarded varchar(30),employee varchar(30));'''
    
    #,X-Folder varchar(30),X-From varchar(30),X-To varchar(30)
    cursor.execute(sql)
    
    sql2 = '''COPY emails(id,file,message_id,date,from_email,to_email,body,subject,cc,bcc,if_forwarded,employee)
    FROM '/filtered.csv'
    DELIMITER '|'
    CSV HEADER;'''
    
    cursor.execute(sql2)
    
    sql3 = '''select * from details;'''
    cursor.execute(sql3)
    for i in cursor.fetchall():
        print(i)
    
    conn.commit()
    conn.close()

#print(loadDataFrameFromPostgres())