import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist_data = input_data.read_data_sets('MNIST_data/',one_hot=True)

#print(tf.__version__)

def accuracy(v_xs,v_ys):
    global prediction
    y_pre = sess.run(prediction,feed_dict={xs:v_xs,ys:v_ys})
    correct_pre = tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pre,tf.float32))
    return sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})

def weight(shape):
    return tf.Variable(tf.truncated_normal(shape,stddev=0.1))

def biases(shape):
    return tf.Variable(tf.constant(0.1,shape=shape))

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

xs = tf.placeholder(tf.float32,[None,784])
ys = tf.placeholder(tf.float32,[None,10])
#drop = tf.placeholder(tf.float32)
x_image = tf.reshape(xs,[-1,28,28,1])

W_cv1 = weight([5,5,1,32])
b_cv1 = biases([32])
z_cv1 = tf.nn.relu(conv2d(x_image, W_cv1) + b_cv1)
z_po1 = max_pool_2x2(z_cv1)

W_cv2 = weight([5,5,32,64])
b_cv2 = biases([64])
z_cv2 = tf.nn.relu(conv2d(z_po1, W_cv2) + b_cv2)
z_po2 = max_pool_2x2(z_cv2)

W_fc1 = weight([7*7*64,1024])
b_fc1 = biases([1024])
x_fc1 = tf.reshape(z_po2,[-1,7*7*64])
z_fc1 = tf.nn.relu(tf.matmul(x_fc1, W_fc1) + b_fc1)
#z_fc1_drop = tf.nn.dropout(z_fc1,drop)

W_fc2 = weight([1024,10])
b_fc2 = biases([10])
prediction = tf.nn.softmax(tf.matmul(z_fc1, W_fc2) + b_fc2)
#z_fc2_drop = tf.nn.dropout(prediction,drop)

train = tf.train.AdamOptimizer(1e-4).minimize(tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),reduction_indices=[1])))
sess = tf.Session()
sess.run(tf.initialize_all_variables())

for i in range(1000):
    batch_xs,batch_ys = mnist_data.train.next_batch(100)
    sess.run(train,feed_dict={xs:batch_xs,ys:batch_ys})
    if i % 100 == 0:
        print(accuracy(mnist_data.test.images,mnist_data.test.labels))
