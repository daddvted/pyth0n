import boto
import boto.s3.connection
from boto.s3.key import Key


def get_conn():
    # access_key = 'JCF0SIK9IWI8T342JHAK'
    # secret_key = 'asWSa7N6tdyQldFrCw4ByqfWnD9QdUtqe9JNeAcf'
    access_key = 'ZH5VXDGTB1I9XMVWGYC0'
    secret_key = 'BAaFsg9NMfvf5VzNI4ej5o5bjeouSq9iswq05IDn'

    conn = boto.connect_s3(aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                           host="ceph.ted.mighty", is_secure=False,
                           calling_format=boto.s3.connection.OrdinaryCallingFormat())
    return conn


def create_bucket(conn, bucket_name):
    bucket = conn.create_bucket(bucket_name)
    print(bucket)


def list_bucket(conn):
    for bucket in conn.get_all_buckets():
        print('{name}\t{created}'.format(name=bucket.name, created=bucket.creation_date))


if __name__ == '__main__':
    rgw_conn = get_conn()
    create_bucket(rgw_conn, 'car')
    list_bucket(rgw_conn)
    # apple = rgw_conn.get_bucket('apple')

    # k = Key(apple)

    # for key in apple.list():
    #     print(key.name)
    #     print(key.size)

        # k.key = key.name
        # print(k.get_contents_as_string())


    # k = Key(apple)
    # k.key = 'hello'
    # k.set_contents_from_string('world')

    # filename = 'admin.jpg'
    # k = Key(apple)
    # k.key = filename
    # k.set_contents_from_filename(filename)


