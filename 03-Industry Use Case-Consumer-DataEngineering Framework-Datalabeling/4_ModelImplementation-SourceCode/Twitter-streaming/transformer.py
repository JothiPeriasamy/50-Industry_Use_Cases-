from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
from pyspark.streaming.kafka import KafkaUtils                                                                          
import os   
import json
import pandas as pd
from pyspark.sql import HiveContext
def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss
        #print('----------rddd-----------',rdd.take(2))
        hiveContext = HiveContext(sc)
        df = hiveContext.read.json(rdd)
        #df.printSchema()
        df.show(2)
        #df = ss.createDataFrame(rdd,schema=['id','created_at','source','favorited','retweet_count','text'])
        #df.show()                                                                                                       
        #df.write.saveAsTable(name='default.gh_raw', format='hive', mode='append')
        if "entities" in df.columns:
            df = df.withColumn("entities",df["entities"].cast('string'))
        if "extended_tweet" in df.columns:
            df = df.withColumn("extended_tweet",df["extended_tweet"].cast('string'))
        if "quoted_status" in df.columns:
            df = df.withColumn("quoted_status",df["quoted_status"].cast('string'))
        if "coordinates" in df.columns:
            df = df.withColumn("coordinates",df["coordinates"].cast('string'))
        if "geo" in df.columns:
            df = df.withColumn("geo",df["geo"].cast('string'))
        if "extended_entities" in df.columns:
            df = df.withColumn("extended_entities",df["extended_entities"].cast('string'))
        if "retweeted_status" in df.columns:
            df = df.withColumn("retweeted_status",df["retweeted_status"].cast('string'))
        if "display_text_range" in df.columns:
            df = df.withColumn("display_text_range",df["display_text_range"].cast('string'))
        if "place" in df.columns:
            df = df.withColumn("place",df["place"].cast('string'))
        if "quoted_status_id" in df.columns:
            df = df.withColumn("quoted_status_id",df["quoted_status_id"].cast('string'))
        if "quoted_status_permalink" in df.columns:
            df = df.withColumn("quoted_status_permalink",df["quoted_status_permalink"].cast('string'))
        if "user" in df.columns:
            df = df.withColumn("user",df["user"].cast('string'))
        if "withheld_in_countries" in df.columns:
            df = df.drop('withheld_in_countries')

        #print('-------------',df['user'])
        df.write.format('hive').mode("append").saveAsTable("default.twitter_data1")
try:                       
    #os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-0-8-assembly.jar pyspark-shell'                                                      
    sc = SparkContext(appName="twitter-stream")                                                                                     
    ssc = StreamingContext(sc, 30)                                                                                           
                                                                                                                            
    ss = SparkSession.builder.appName("twitter-streaming").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").config("set hive.serialization.extend.nesting.levels","true").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                   
    ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
    ks = KafkaUtils.createDirectStream(ssc, ['twitter'], {'metadata.broker.list': 'localhost:9092'})                           
    lines = ks.map(lambda x: x[1])                                                                                              
    #transform = lines.map(lambda tweet: (tweet, int(len(tweet.split())), int(len(tweet))))                              
    lines.foreachRDD(handle_rdd)
    
except BaseException as e:
    print('error - ',e)
                                                                                                                        
ssc.start()                                                                                                             
ssc.awaitTermination()