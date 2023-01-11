import boto3
 
# S3、DynamoDBテーブルへの接続準備
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("s3-to-dynamodb")
 
def lambda_handler(event, context):
 
    # S3情報をeventから取得
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
 
    # オブジェクト（CSVファイル）を取得して行ごとにデータを取得
    resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
    data = resp['Body'].read().decode("cp932")
    employees = data.split("\n")
 
    # 取得したデータの値を1つずつカンマで分けてテーブルに登録
    for emp in employees:
        print(emp)
        emp_data = emp.split(",")
 
        try:
            table.put_item(
                Item = {
                    "ID_Date"    : emp_data[0],
                    "Temperture" : emp_data[1],
                    "Humidity"   : emp_data[2],
                    "Discomfort" : emp_data[3]
                }
            )
        except Exception as e:
            print(e)