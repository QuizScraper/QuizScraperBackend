import os
ss.makedirs('~/.aws')
f = open('~/.aws/credentials', 'w')
f.write('[default]')
f.write('aws_access_key_id = ${AWS_ACCESS_KEY_ID}')
f.write('aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}')