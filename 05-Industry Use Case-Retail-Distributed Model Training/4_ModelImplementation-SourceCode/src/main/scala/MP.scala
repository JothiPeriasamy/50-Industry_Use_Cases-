/*
    Step #1 :  Important Required Libraries
*/
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import org.apache.spark.ml.feature.{HashingTF, Tokenizer}
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder}
import org.apache.spark.sql.SparkSession
object MP extends App{


  val vAR_spark = SparkSession.builder
    .master("local[*]")
    .appName("Distributed Training_Model Parallelism-Cross Validator")
    .getOrCreate()
  /*
      Step #2 :  Import Training Data
   */
  val vAR_crossvalid_csv_df = vAR_spark.read
    .option("header",true)
    .option("inferSchema","true")
    .csv("hdfs://localhost:9820/test/DS.AI_CrossValid_data.csv")


  val vAR_training = vAR_crossvalid_csv_df.filter( "label is not null")
  val vAR_test = vAR_crossvalid_csv_df.filter( "label is null").select("id","text")

  /*
    Step #3 :  Pre-processing Training Data
 */
  //A tokenizer that converts the input string to lowercase and then splits it by white spaces.
  //Tokenization is the process of taking text (such as a sentence) and breaking it into individual terms (usually words).
  val vAR_tokenizer = new Tokenizer()
    .setInputCol("text")
    .setOutputCol("words")
  val vAR_tokenized = vAR_tokenizer.transform(vAR_training)

  //HashingTF converts documents to vectors of fixed size.
  val vAR_hashingTF = new HashingTF()
    .setInputCol(vAR_tokenizer.getOutputCol)
    .setOutputCol("features")

  val vAR_lr = new LogisticRegression()
    .setMaxIter(10)

  // Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
  val vAR_pipeline = new Pipeline()
    .setStages(Array(vAR_tokenizer, vAR_hashingTF, vAR_lr))

  // this grid will have 3 x 2 = 6 parameter settings for CrossValidator to choose from.
  val vAR_paramGrid = new ParamGridBuilder()
    .addGrid(vAR_hashingTF.numFeatures, Array(10, 100, 1000))  // 3 rows
    .addGrid(vAR_lr.regParam, Array(0.1, 0.01))  // 2 cols
    .build()    // refers 3 X 2 matrix combination of parameter sets

  val vAR_cv = new CrossValidator()
    .setEstimator(vAR_pipeline)
    .setEvaluator(new BinaryClassificationEvaluator)
    .setEstimatorParamMaps(vAR_paramGrid)
    .setNumFolds(5)  // Use 3+ in practice// generates 4 dataset pairs of training,test
    .setParallelism(3)  // Evaluate up to 3 parameter settings in parallel

  /*
    Step #4 : Train Data
 */
  // n cross-validation, and choose the best set of parameters.
  val vAR_cvModel = vAR_cv.fit(vAR_training)
  /*
    Step #5 : Predict on Test Data
 */
  val vAR_prediction = vAR_cvModel.transform(vAR_test)
  vAR_prediction.show()




  System.in.read
  //spark.stop()

}
