import boto3

with open('creds', 'r') as f:
    l = f.readlines()
    region_name = l[2].strip()
    aws_secret_access_key = l[1].strip()
    aws_access_key_id = l[0].strip()

try:
    db = boto3.client('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    print("Connected Successfully")
except Exception as e:
    print(f"Configure Again: {e}")

print("LIST OF TABLES")
tables = db.list_tables()['TableNames']
print(tables)

TABLE_NAME = "workers"
PRIMARY_KEY = "workers_id"

if TABLE_NAME not in tables:
    print("Creating Table...")
    table = db.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': PRIMARY_KEY,
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': PRIMARY_KEY,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table Created Successfully!")


table = boto3.resource('dynamodb').Table(TABLE_NAME)

print("ADDING ITEMS")
table.put_item(
    Item={
        PRIMARY_KEY: "1",
        'name': "xxxxxx"
    }
)

table.put_item(
    Item={
        PRIMARY_KEY: "2",
        'name': "yyyyy"
    }
)

print("GETTING ALL ITEMS")
res = table.scan()
for item in res["Items"]:
    print(item)


# print(table.item_count)

# res = table.get_item(
# 	Key={
# 		'emp_id':"2"
# 	}
# )


# print(res["Item"])


# table = db.Table("test")
# table.put_item(
# 	Item={
# 		'emp_id':"2",
# 		'name':"SIN_GREED",
# 		'age':"19"
# 	}
# )

# res = table.get_item(
# 	Key={
# 		'emp_id': "2"
# 	}
# )

# print(res['Item'])
